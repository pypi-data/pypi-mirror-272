import ctypes
import os
from .autograd.functions import *

class CTensor(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(ctypes.c_float)),
        ('strides', ctypes.POINTER(ctypes.c_int)),
        ('shape', ctypes.POINTER(ctypes.c_int)),
        ('ndim', ctypes.c_int),
        ('size', ctypes.c_int),
        ('device', ctypes.c_char_p)
    ]

class Tensor:
    module_dir = os.path.dirname(os.path.abspath(__file__))
    _C = ctypes.CDLL(os.path.join(module_dir, "libtensor.so"))

    def __init__(self, data=None, device="cpu", requires_grad=False):

        if data != None:
            data, shape = self.flatten(data)
            self.data_ctype = (ctypes.c_float * len(data))(*data)
            self.shape_ctype = (ctypes.c_int * len(shape))(*shape)
            self.ndim_ctype = ctypes.c_int(len(shape))
            self.device_ctype = device.encode('utf-8')

            self.shape = shape
            self.ndim = len(shape)
            self.device = device

            self.numel = 1
            for s in self.shape:
                self.numel *= s

            self.requires_grad = requires_grad
            self.grad = None
            self.grad_fn = None

            Tensor._C.create_tensor.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_char_p]
            Tensor._C.create_tensor.restype = ctypes.POINTER(CTensor)
            

            self.tensor = Tensor._C.create_tensor(
                self.data_ctype,
                self.shape_ctype,
                self.ndim_ctype,
                self.device_ctype
            )
        
        else:
            self.tensor = None,
            self.shape = None,
            self.ndim = None,
            self.device = device
            self.requires_grad = None
            self.grad = None
            self.grad_fn = None

    def flatten(self, nested_list):
        def flatten_recursively(nested_list):
            flat_data = []
            shape = []
            if isinstance(nested_list, list):
                for sublist in nested_list:
                    inner_data, inner_shape = flatten_recursively(sublist)
                    flat_data.extend(inner_data)
                shape.append(len(nested_list))
                shape.extend(inner_shape)
            else:
                flat_data.append(nested_list)
            return flat_data, shape
        
        flat_data, shape = flatten_recursively(nested_list)
        return flat_data, shape
    
    def ones_like(self):
        
        Tensor._C.ones_like_tensor.argtypes = [ctypes.POINTER(CTensor)]
        Tensor._C.ones_like_tensor.restype = ctypes.POINTER(CTensor)
        Tensor._C.ones_like_tensor(self.tensor)   

        result_tensor_ptr = Tensor._C.ones_like_tensor(self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel
        
        return result_data
    
    def zeros_like(self):
        
        Tensor._C.zeros_like_tensor.argtypes = [ctypes.POINTER(CTensor)]
        Tensor._C.zeros_like_tensor.restype = ctypes.POINTER(CTensor)
        Tensor._C.zeros_like_tensor(self.tensor)   

        result_tensor_ptr = Tensor._C.zeros_like_tensor(self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        return result_data
    
    def reshape(self, new_shape):

        new_shape_ctype = (ctypes.c_int * len(new_shape))(*new_shape)
        new_ndim_ctype = ctypes.c_int(len(new_shape))
        
        Tensor._C.reshape_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        Tensor._C.reshape_tensor.restype = ctypes.POINTER(CTensor)
        result_tensor_ptr = Tensor._C.reshape_tensor(self.tensor, new_shape_ctype, new_ndim_ctype)   

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = new_shape.copy()
        result_data.ndim = len(new_shape)
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = ReshapeBackward(self)

        return result_data
    
    def to(self, device):
        self.device = device
        self.device_ctype = self.device.encode('utf-8')

        Tensor._C.to_device.argtypes = [ctypes.POINTER(CTensor), ctypes.c_char_p]
        Tensor._C.to_device.restype = None
        Tensor._C.to_device(self.tensor, self.device_ctype)

        return self
    
    def backward(self, gradient=None):
        if not self.requires_grad:
            return
                
        if gradient is None:
            if self.shape == [1]:
                gradient = Tensor([1])
            else:
                raise RuntimeError("Gradient argument must be specified for non-scalar tensors.")


        stack = [(self, gradient)]
        visited = set()
    
        while stack:
            tensor, grad = stack.pop()
            
            if tensor.grad is None:
                tensor.grad = grad
            else:
                tensor.grad += grad

            # Propagate gradients to inputs if not a leaf tensor
            if tensor.grad_fn is not None:
                grads = tensor.grad_fn.backward(grad)
                for tensor, grad in zip(tensor.grad_fn.input, grads):
                    if isinstance(tensor, Tensor) and tensor not in visited:
                        stack.append((tensor, grad))
                        visited.add(tensor)

    def zero_grad(self):
        self.grad = None

    def detach(self):
        self.grad = None
        self.grad_fn = None

    def __getitem__(self, indices):
        if isinstance(indices, int):
            indices = [indices]
        if len(indices) != self.ndim:
            raise ValueError("Number of indices must match the number of dimensions")
        
        Tensor._C.get_item.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(ctypes.c_int)]
        Tensor._C.get_item.restype = ctypes.c_float
                                           
        indices = (ctypes.c_int * len(indices))(*indices)
        value = Tensor._C.get_item(self.tensor, indices)  

        return value 
    
    def __str__(self):
        def print_recursively(tensor, depth, index):
            if depth == tensor.ndim - 1:
                result = ""
                for i in range(tensor.shape[-1]):
                    index[-1] = i
                    result += str(tensor[tuple(index)]) + ", "
                return result.strip()
            else:
                result = ""
                if depth > 0:
                    result += "\n" + " " * ((depth - 1) * 4)
                for i in range(tensor.shape[depth]):
                    index[depth] = i
                    result += "["
                    result += print_recursively(tensor, depth + 1, index) + "],"
                    if i < tensor.shape[depth] - 1:
                        result += "\n" + " " * (depth * 4)
                return result.strip(",")

        index = [0] * self.ndim
        result = "tensor(["
        result += print_recursively(self, 0, index)
        result += f"""], device="{self.device}", requires_grad={self.requires_grad})"""
        return result

    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = other * self.ones_like()
        
        if self.shape != other.shape:
            raise ValueError("Tensors must have the same shape for addition")
        
        Tensor._C.add_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
        Tensor._C.add_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.add_tensor(self.tensor, other.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad or other.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = AddBackward(self, other)

        return result_data
    
    def __radd__(self, other):
        if isinstance(other, (int, float)):
            other = other * self.ones_like()
        
        if self.shape != other.shape:
            raise ValueError("Tensors must have the same shape for addition")
        
        Tensor._C.add_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
        Tensor._C.add_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.add_tensor(other.tensor, self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad or other.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = AddBackward(other, self)

        return result_data
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = other * self.ones_like()

        if self.shape != other.shape:
            raise ValueError("Tensors must have the same shape for subtraction")
        
        Tensor._C.sub_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
        Tensor._C.sub_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.sub_tensor(self.tensor, other.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad or other.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = SubBackward(self, other)

        return result_data
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            other = other * self.ones_like()

        if self.shape != other.shape:
            raise ValueError("Tensors must have the same shape for subtraction")
        
        Tensor._C.sub_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
        Tensor._C.sub_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.sub_tensor(other.tensor, self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad or other.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = SubBackward(other, self)

        return result_data
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result_data = Tensor()
            result_data.shape = self.shape.copy()
            result_data.ndim = self.ndim
            result_data.device = self.device
            result_data.numel = self.numel

            Tensor._C.scalar_mul_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.c_float]
            Tensor._C.scalar_mul_tensor.restype = ctypes.POINTER(CTensor)

            result_data.tensor = Tensor._C.scalar_mul_tensor(self.tensor, ctypes.c_float(other))

            result_data.requires_grad = self.requires_grad
            if result_data.requires_grad:
                result_data.grad_fn = ScalarMulBackward(self, other)

            return result_data
        elif isinstance(other, Tensor):
            if self.shape != other.shape:
                raise ValueError("Tensors must have the same shape for element-wise multiplication")

            Tensor._C.elementwise_mul_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
            Tensor._C.elementwise_mul_tensor.restype = ctypes.POINTER(CTensor)

            result_tensor_ptr = Tensor._C.elementwise_mul_tensor(self.tensor, other.tensor)

            result_data = Tensor()
            result_data.tensor = result_tensor_ptr
            result_data.shape = self.shape.copy()
            result_data.ndim = self.ndim
            result_data.device = self.device
            result_data.numel = self.numel

            result_data.requires_grad = self.requires_grad or other.requires_grad
            if result_data.requires_grad:
                result_data.grad_fn = ElementwiseMulBackward(self, other)

            return result_data
        else:
            raise TypeError("Unsupported operand type(s) for *: '{}' and '{}'".format(type(self), type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return self.__mul__(-1)  

    def __pos__(self):
        return self  
    
    def __matmul__(self, other):
        if self.ndim < 3 and other.ndim == 3:
            #broadcasted 2D x 3D matmul

            Tensor._C.broadcasted_batched_matmul_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
            Tensor._C.broadcasted_batched_matmul_tensor.restype = ctypes.POINTER(CTensor)
            
            result_tensor_ptr = Tensor._C.broadcasted_batched_matmul_tensor(self.tensor, other.tensor)

            result_data = Tensor()
            result_data.tensor = result_tensor_ptr
            result_data.shape = [other.shape[0], self.shape[0], other.shape[2]]
            result_data.ndim = 3
            result_data.device = self.device
            result_data.numel = 1
            for s in result_data.shape:
                result_data.numel *= s


        elif self.ndim == 3 and other.ndim == 3:
            #broadcasted 3D x 3D matmul

            Tensor._C.batched_matmul_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
            Tensor._C.batched_matmul_tensor.restype = ctypes.POINTER(CTensor)
            
            result_tensor_ptr = Tensor._C.batched_matmul_tensor(self.tensor, other.tensor)

            result_data = Tensor()
            result_data.tensor = result_tensor_ptr
            result_data.shape = [other.shape[0], self.shape[1], other.shape[2]]
            result_data.ndim = 3
            result_data.device = self.device
            result_data.numel = 1
            for s in result_data.shape:
                result_data.numel *= s
        else:
            #2D matmul
            if self.ndim != 2 or other.ndim != 2:
                raise ValueError("Matrix multiplication requires 2D tensors")

            if self.shape[1] != other.shape[0]:
                raise ValueError("Incompatible shapes for matrix multiplication")

            Tensor._C.matmul_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
            Tensor._C.matmul_tensor.restype = ctypes.POINTER(CTensor)

            result_tensor_ptr = Tensor._C.matmul_tensor(self.tensor, other.tensor)

            result_data = Tensor()
            result_data.tensor = result_tensor_ptr
            result_data.shape = [self.shape[0], other.shape[1]]
            result_data.ndim = 2
            result_data.device = self.device
            result_data.numel = 1
            for s in result_data.shape:
                result_data.numel *= s

        result_data.requires_grad = self.requires_grad or other.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = MatmulBackward(self, other)

        return result_data

    def __pow__(self, other):
        other = float(other)
        Tensor._C.tensor_pow_scalar.argtypes = [ctypes.POINTER(CTensor), ctypes.c_float]
        Tensor._C.tensor_pow_scalar.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.tensor_pow_scalar(self.tensor, ctypes.c_float(other))

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = PowBackward(self, other)
        
        return result_data
    
    def __rpow__(self, other):
        other = float(other)
        Tensor._C.scalar_pow_tensor.argtypes = [ctypes.c_float, ctypes.POINTER(CTensor)]
        Tensor._C.scalar_pow_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.scalar_pow_tensor(ctypes.c_float(other), self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = PowBackward(other, self)

        return result_data

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = float(other)
            Tensor._C.tensor_div_scalar.argtypes = [ctypes.POINTER(CTensor), ctypes.c_float]
            Tensor._C.tensor_div_scalar.restype = ctypes.POINTER(CTensor)

            result_tensor_ptr = Tensor._C.tensor_div_scalar(self.tensor, ctypes.c_float(other))

            result_data = Tensor()
            result_data.tensor = result_tensor_ptr
            result_data.shape = self.shape.copy()
            result_data.ndim = self.ndim
            result_data.device = self.device
            result_data.numel = self.numel
            
            result_data.requires_grad = self.requires_grad
            if result_data.requires_grad:
                result_data.grad_fn = DivisionBackward(self, other)
        
        elif isinstance(self, Tensor) and isinstance(other, Tensor):
            Tensor._C.tensor_div_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.POINTER(CTensor)]
            Tensor._C.tensor_div_tensor.restype = ctypes.POINTER(CTensor)

            result_tensor_ptr = Tensor._C.tensor_div_tensor(self.tensor, other.tensor)

            result_data = Tensor()
            result_data.tensor = result_tensor_ptr
            result_data.shape = self.shape.copy()
            result_data.ndim = self.ndim
            result_data.device = self.device
            result_data.numel = self.numel

            result_data.requires_grad = self.requires_grad or other.requires_grad
            if result_data.requires_grad:
                result_data.grad_fn = DivisionBackward(self, other)

        return result_data
        
        
    
    def __rtruediv__(self, other):
        other = float(other)

        Tensor._C.scalar_div_tensor.argtypes = [ctypes.c_float, ctypes.POINTER(CTensor)]
        Tensor._C.scalar_div_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.scalar_div_tensor(ctypes.c_float(other), self.tensor)        

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = DivisionBackward(other, self)

        return result_data

    
    def log(self):
        Tensor._C.log_tensor.argtypes = [ctypes.POINTER(CTensor)]
        Tensor._C.log_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.log_tensor(self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = LogBackward(self)

        return result_data
    
    def sum(self):
        Tensor._C.sum_tensor.argtypes = [ctypes.POINTER(CTensor)]
        Tensor._C.sum_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.sum_tensor(self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = [1]
        result_data.ndim = 1
        result_data.device = self.device
        result_data.numel = 1

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = SumBackward(self)

        return result_data
    
    def sin(self):
        Tensor._C.sin_tensor.argtypes = [ctypes.POINTER(CTensor)]
        Tensor._C.sin_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.sin_tensor(self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = SinBackward(self)
        
        return result_data
    
    def cos(self):
        Tensor._C.cos_tensor.argtypes = [ctypes.POINTER(CTensor)]
        Tensor._C.cos_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.cos_tensor(self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = CosBackward(self)
        
        return result_data
    

    
    def transpose(self, axis1, axis2):
        if axis1 < 0:
            axis1 = self.ndim + axis1
        if axis2 < 0:
            axis2 = self.ndim + axis2

        Tensor._C.transpose_axes_tensor.argtypes = [ctypes.POINTER(CTensor), ctypes.c_int, ctypes.c_int]
        Tensor._C.transpose_axes_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.transpose_axes_tensor(self.tensor, axis1, axis2)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()
        result_data.shape[axis1] = self.shape[axis2]
        result_data.shape[axis2] = self.shape[axis1]
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = TransposeBackward(self, axis1, axis2)

        return result_data
    
    @property
    def T(self):
        Tensor._C.transpose_tensor.argtypes = [ctypes.POINTER(CTensor)]
        Tensor._C.transpose_tensor.restype = ctypes.POINTER(CTensor)

        result_tensor_ptr = Tensor._C.transpose_tensor(self.tensor)

        result_data = Tensor()
        result_data.tensor = result_tensor_ptr
        result_data.shape = self.shape.copy()[::-1]
        result_data.ndim = self.ndim
        result_data.device = self.device
        result_data.numel = self.numel

        result_data.requires_grad = self.requires_grad
        if result_data.requires_grad:
            result_data.grad_fn = TBackward(self)

        return result_data
    
    def detach(self):
        self.grad = None
        self.grad_fn = None

        return self        