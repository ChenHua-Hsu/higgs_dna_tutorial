#pragma once

// @generated by torchgen/gen.py from Function.h

#include <ATen/Context.h>
#include <ATen/DeviceGuard.h>
#include <ATen/TensorUtils.h>
#include <ATen/TracerMode.h>
#include <ATen/core/Generator.h>
#include <ATen/core/Reduction.h>
#include <ATen/core/Tensor.h>
#include <c10/core/Scalar.h>
#include <c10/core/Storage.h>
#include <c10/core/TensorOptions.h>
#include <c10/util/Deprecated.h>
#include <c10/util/Optional.h>



#include <ATen/ops/_fused_sgd_ops.h>

namespace at {


// aten::_fused_sgd_(Tensor(a!)[] self, Tensor(b!)[] grads, Tensor(c!)[] momentum_buffer_list, *, float weight_decay, float momentum, float lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None) -> ()
inline void _fused_sgd_(at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, double lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale={}, const c10::optional<at::Tensor> & found_inf={}) {
    return at::_ops::_fused_sgd_::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf);
}

// aten::_fused_sgd_.tensor_lr(Tensor(a!)[] self, Tensor(b!)[] grads, Tensor(c!)[] momentum_buffer_list, *, float weight_decay, float momentum, Tensor lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None) -> ()
inline void _fused_sgd_(at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, const at::Tensor & lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale={}, const c10::optional<at::Tensor> & found_inf={}) {
    return at::_ops::_fused_sgd__tensor_lr::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf);
}

// aten::_fused_sgd.out(Tensor[] self, Tensor(b!)[] grads, Tensor(c!)[] momentum_buffer_list, *, float weight_decay, float momentum, float lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None, Tensor(a!)[] out) -> ()
inline void _fused_sgd_out(at::TensorList out, at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, double lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale={}, const c10::optional<at::Tensor> & found_inf={}) {
    return at::_ops::_fused_sgd_out::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf, out);
}
// aten::_fused_sgd.out(Tensor[] self, Tensor(b!)[] grads, Tensor(c!)[] momentum_buffer_list, *, float weight_decay, float momentum, float lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None, Tensor(a!)[] out) -> ()
inline void _fused_sgd_outf(at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, double lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale, const c10::optional<at::Tensor> & found_inf, at::TensorList out) {
    return at::_ops::_fused_sgd_out::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf, out);
}

// aten::_fused_sgd(Tensor[] self, Tensor[] grads, Tensor[] momentum_buffer_list, *, float weight_decay, float momentum, float lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None) -> (Tensor[] self_out, Tensor[] grads_out, Tensor[] momentum_buffer_list_out)
inline ::std::tuple<::std::vector<at::Tensor>,::std::vector<at::Tensor>,::std::vector<at::Tensor>> _fused_sgd(at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, double lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale={}, const c10::optional<at::Tensor> & found_inf={}) {
    return at::_ops::_fused_sgd::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf);
}

// aten::_fused_sgd.tensor_lr_out(Tensor[] self, Tensor(b!)[] grads, Tensor(c!)[] momentum_buffer_list, *, float weight_decay, float momentum, Tensor lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None, Tensor(a!)[] out) -> ()
inline void _fused_sgd_out(at::TensorList out, at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, const at::Tensor & lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale={}, const c10::optional<at::Tensor> & found_inf={}) {
    return at::_ops::_fused_sgd_tensor_lr_out::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf, out);
}
// aten::_fused_sgd.tensor_lr_out(Tensor[] self, Tensor(b!)[] grads, Tensor(c!)[] momentum_buffer_list, *, float weight_decay, float momentum, Tensor lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None, Tensor(a!)[] out) -> ()
inline void _fused_sgd_outf(at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, const at::Tensor & lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale, const c10::optional<at::Tensor> & found_inf, at::TensorList out) {
    return at::_ops::_fused_sgd_tensor_lr_out::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf, out);
}

// aten::_fused_sgd.tensor_lr(Tensor[] self, Tensor[] grads, Tensor[] momentum_buffer_list, *, float weight_decay, float momentum, Tensor lr, float dampening, bool nesterov, bool maximize, bool is_first_step, Tensor? grad_scale=None, Tensor? found_inf=None) -> (Tensor[] self_out, Tensor[] grads_out, Tensor[] momentum_buffer_list_out)
inline ::std::tuple<::std::vector<at::Tensor>,::std::vector<at::Tensor>,::std::vector<at::Tensor>> _fused_sgd(at::TensorList self, at::TensorList grads, at::TensorList momentum_buffer_list, double weight_decay, double momentum, const at::Tensor & lr, double dampening, bool nesterov, bool maximize, bool is_first_step, const c10::optional<at::Tensor> & grad_scale={}, const c10::optional<at::Tensor> & found_inf={}) {
    return at::_ops::_fused_sgd_tensor_lr::call(self, grads, momentum_buffer_list, weight_decay, momentum, lr, dampening, nesterov, maximize, is_first_step, grad_scale, found_inf);
}

}
