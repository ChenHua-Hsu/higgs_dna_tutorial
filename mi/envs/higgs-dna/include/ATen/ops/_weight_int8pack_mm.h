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



#include <ATen/ops/_weight_int8pack_mm_ops.h>

namespace at {


// aten::_weight_int8pack_mm(Tensor self, Tensor mat2, Tensor scales) -> Tensor
inline at::Tensor _weight_int8pack_mm(const at::Tensor & self, const at::Tensor & mat2, const at::Tensor & scales) {
    return at::_ops::_weight_int8pack_mm::call(self, mat2, scales);
}

}
