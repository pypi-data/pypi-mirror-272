use std::{iter::zip, ops::Mul};

use candle_core::{
    quantized::{QMatMul, QTensor},
    DType, Module, Result, Tensor,
};
use candle_nn::{init, Dropout, Linear, VarBuilder};
use either::Either;

use crate::{
    apply_scalings_to_x, get_maybe_topk_scalings, LinearLayerLike, LoraConfig, LoraLinearConfig,
    Merge, Ordering,
};

#[derive(Debug)]
pub struct QLoraLinear {
    old: QMatMul,
    a_adapters: Either<Vec<Linear>, (Tensor, Vec<Linear>)>,
    b_adapters: Either<Vec<Linear>, (Tensor, Vec<Linear>)>,
    scale_adapters: Vec<f64>,
    dropout_adapters: Vec<Option<Dropout>>,
    layer_n: usize,
    merged: bool,
}

/// Specialized QLoRA for no bias
impl QLoraLinear {
    pub fn new(
        old: QMatMul,
        linear_config: &LoraLinearConfig,
        config: &[(String, LoraConfig)],
        vb: &VarBuilder,
        ordering: &Ordering,
        prefix: String,
        count: &mut usize,
    ) -> Result<Self> {
        let target_modules = &config[0].1.target_modules;
        for (_, cfg) in config {
            if &cfg.target_modules != target_modules {
                candle_core::bail!("Expected all target modules to be the same.");
            }
        }

        let module = prefix.split('.').last().unwrap();
        if !target_modules.contains(module) {
            return Ok(Self {
                old,
                a_adapters: Either::Left(vec![]),
                b_adapters: Either::Left(vec![]),
                scale_adapters: vec![],
                dropout_adapters: vec![],
                layer_n: usize::MAX,
                merged: false,
            });
        }

        *count += 1;

        let mut a_adapters = Vec::with_capacity(config.len());
        let mut b_adapters = Vec::with_capacity(config.len());
        let mut scale_adapters = Vec::with_capacity(config.len());
        let mut dropout_adapters = Vec::with_capacity(config.len());
        let vb = vb.pp(prefix.clone());
        let a_vb = vb.pp("lora_A".to_string());
        let b_vb = vb.pp("lora_B".to_string());
        let mut state = None;
        let mut all_same = true;
        for (name, cfg) in config.iter() {
            let a_pp = a_vb.pp(name);
            assert!(a_pp.contains_tensor("weight"));
            let a = a_pp
                .get_with_hints(
                    (cfg.rank, linear_config.in_features),
                    "weight",
                    init::DEFAULT_KAIMING_NORMAL,
                )?
                .to_dtype(DType::F32)?;
            let b_pp = b_vb.pp(name);
            assert!(b_pp.contains_tensor("weight"));
            let b = b_pp
                .get_with_hints((linear_config.out_features, cfg.rank), "weight", init::ZERO)?
                .to_dtype(DType::F32)?;
            a_adapters.push(Linear::new(a, None));
            b_adapters.push(Linear::new(b, None));
            scale_adapters.push(if cfg.rank > 0 {
                cfg.alpha / cfg.rank as f64
            } else {
                1.0
            });
            dropout_adapters.push(cfg.dropout.map(Dropout::new));
            if state.is_some_and(|x| {
                x == (
                    cfg.rank,
                    linear_config.in_features,
                    linear_config.out_features,
                    cfg.alpha,
                    cfg.dropout,
                )
            }) || state.is_none()
            {
                state = Some((
                    cfg.rank,
                    linear_config.in_features,
                    linear_config.out_features,
                    cfg.alpha,
                    cfg.dropout,
                ));
            } else {
                all_same = false;
            }
        }
        let layer = *ordering.layers.get(&prefix).unwrap();

        if all_same {
            let a_adapters_stack = Tensor::cat(
                &a_adapters
                    .iter()
                    .map(|x| x.weight().unsqueeze(0))
                    .collect::<Result<Vec<_>>>()?,
                0,
            )?;
            let b_adapters_stack = Tensor::cat(
                &b_adapters
                    .iter()
                    .map(|x| x.weight().unsqueeze(0))
                    .collect::<Result<Vec<_>>>()?,
                0,
            )?;
            let scale_adapters_t = Tensor::from_vec(
                scale_adapters.clone(),
                (scale_adapters.len(), 1, 1),
                a_adapters_stack.device(),
            )?
            .to_dtype(a_adapters_stack.dtype())?;
            let a_adapters_stack = a_adapters_stack.broadcast_mul(&scale_adapters_t)?;
            Ok(QLoraLinear {
                old,
                a_adapters: Either::Right((a_adapters_stack.clone(), a_adapters)),
                b_adapters: Either::Right((b_adapters_stack.clone(), b_adapters)),
                scale_adapters,
                dropout_adapters,
                layer_n: layer,
                merged: false,
            })
        } else {
            Ok(QLoraLinear {
                old,
                a_adapters: Either::Left(a_adapters),
                b_adapters: Either::Left(b_adapters),
                scale_adapters,
                dropout_adapters,
                layer_n: layer,
                merged: false,
            })
        }
    }
}

impl Merge for QLoraLinear {
    fn get_delta_weight(&self, adapter: usize) -> Result<Tensor> {
        match (&self.a_adapters, &self.b_adapters) {
            (Either::Left(a), Either::Left(b)) | (Either::Right((_, a)), Either::Right((_, b))) => {
                let w_a = a[adapter].weight();
                let w_b = b[adapter].weight();

                w_b.matmul(w_a)? * self.scale_adapters[adapter]
            }
            _ => unreachable!("Both adapters must be Either::Left or Either::Right."),
        }
    }

    fn merge_weights(&mut self) -> Result<()> {
        let (mut w_base_layer, dtype) = match &self.old {
            QMatMul::QTensor(q) => (q.dequantize(&q.device())?, q.dtype()),
            QMatMul::Tensor(_) | QMatMul::TensorF16(_) => unreachable!(),
        };
        for adapter in 0..self.scale_adapters.len() {
            w_base_layer = (w_base_layer + self.get_delta_weight(adapter))?;
        }
        let new_w = QTensor::quantize(&w_base_layer, dtype)?;
        self.old = QMatMul::from_qtensor(new_w)?;
        self.merged = true;
        Ok(())
    }
}

impl LinearLayerLike for QLoraLinear {
    fn bias(&self) -> Option<&Tensor> {
        None
    }
    fn weight(&self) -> &Tensor {
        unimplemented!()
    }
    fn inner(&mut self) -> &mut QMatMul {
        &mut self.old
    }
    fn is_quant(&self) -> bool {
        true
    }
    fn lora_forward(
        &self,
        input: &Tensor,
        scalings: Option<Tensor>,
        global_scaling_weight: f64,
        is_scaling_pass: Option<f64>,
    ) -> Result<Tensor> {
        //No fan_in_fan_out so no weight.transpose(0,1)
        let mut result = self.old.forward(input)?;
        if self.merged {
            return Ok(result);
        }
        let scalings = scalings.unwrap();

        if self
            .a_adapters
            .as_ref()
            .left()
            .is_some_and(|x| x.is_empty())
            || (is_scaling_pass.is_some_and(|x| x == 0.))
        {
            return Ok(result);
        }
        let scalings = get_maybe_topk_scalings(scalings, self.layer_n)?;
        if self.a_adapters.is_left() || scalings.dims3()?.1 != 1 {
            let a_adapters = if self.a_adapters.is_right() {
                self.a_adapters.as_ref().unwrap_right().1.clone()
            } else {
                self.a_adapters.as_ref().unwrap_left().clone()
            };
            let b_adapters = if self.b_adapters.is_right() {
                self.b_adapters.as_ref().unwrap_right().1.clone()
            } else {
                self.b_adapters.as_ref().unwrap_left().clone()
            };
            for (i, (adapter_a, (adapter_b, (adapter_scale, adapter_dropout)))) in zip(
                a_adapters,
                zip(
                    b_adapters,
                    zip(&self.scale_adapters, self.dropout_adapters.iter()),
                ),
            )
            .enumerate()
            {
                let mut input_new = apply_scalings_to_x(input.clone(), &scalings, i)?;

                input_new = if let Some(ref dropout) = adapter_dropout {
                    dropout.forward(&input_new, true)?
                } else {
                    input_new.clone()
                };
                let res = adapter_b
                    .forward(&adapter_a.forward(&input_new)?)?
                    .mul(*adapter_scale)?
                    .mul(global_scaling_weight)?;
                result = (result + res)?;
            }
            Ok(result)
        } else {
            let adapter_a = &self.a_adapters.as_ref().unwrap_right().0;
            let adapter_b = &self.b_adapters.as_ref().unwrap_right().0;
            let adapter_scales = &self.scale_adapters;
            let n_adapters = adapter_scales.len();
            let dropout = &self.dropout_adapters[0];
            let scalings = scalings
                .squeeze(0)?
                .squeeze(0)?
                .unsqueeze(1)?
                .unsqueeze(1)?;
            let adapter_a = adapter_a
                .broadcast_mul(&scalings)?
                .mul(global_scaling_weight)?;

            let input = if let Some(ref d) = dropout {
                d.forward(input, true)?
            } else {
                input.clone()
            };
            let (b, s, h) = input.dims3()?;
            let input = input.reshape((b * s, h))?;
            let out = adapter_a.broadcast_matmul(&input.t()?)?;
            let out = adapter_b.broadcast_matmul(&out)?;
            let o_h = out.dims()[1];
            let out = out.reshape((n_adapters, b, s, o_h))?;
            let out = out.sum(0)?;
            out + result
        }
    }
}
