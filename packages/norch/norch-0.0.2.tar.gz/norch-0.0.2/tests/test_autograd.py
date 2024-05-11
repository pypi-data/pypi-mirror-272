import unittest
import norch
from norch.utils import utils_unittests as utils
import torch
import os

class TestTensorAutograd(unittest.TestCase):
    def setUp(self):
        self.device = os.environ.get('device')
        if self.device is None or self.device != 'cuda':
            self.device = 'cpu'
        
    def test_addition(self):
        """
        Test autograd from addition two tensors: tensor1 + tensor2
        """
        norch_tensor1 = norch.Tensor([[[1, 2.5], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        norch_tensor2 = norch.Tensor([[[1, 1.], [1, 1.9]], [[1, 1], [1, 1]]], requires_grad=True).to(self.device)
        norch_result = (norch_tensor1 + norch_tensor2).sum()
        norch_result.backward()
        norch_tensor1_grad = utils.to_torch(norch_tensor1.grad)
        norch_tensor2_grad = utils.to_torch(norch_tensor2.grad)

        torch_tensor1 = torch.tensor([[[1, 2.5], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_tensor2 = torch.tensor([[[1, 1.], [1, 1.9]], [[1, 1], [1, 1]]], requires_grad=True).to(self.device)
        torch_result = (torch_tensor1 + torch_tensor2).sum()
        torch_result.backward()
        torch_tensor1_grad = torch_tensor1.grad
        torch_tensor2_grad = torch_tensor2.grad

        self.assertTrue(utils.compare_torch(norch_tensor1_grad, torch_tensor1_grad))
        self.assertTrue(utils.compare_torch(norch_tensor2_grad, torch_tensor2_grad))

    
    def test_subtraction(self):
        """
        Test autograd from subtraction two tensors: tensor1 - tensor2
        """
        norch_tensor1_sub = norch.Tensor([[[1, 2.5], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        norch_tensor2_sub = norch.Tensor([[[1, 1.], [1, 1.9]], [[1, 1], [1, 1]]], requires_grad=True).to(self.device)
        norch_result_sub = (norch_tensor1_sub - norch_tensor2_sub).sum()
        norch_result_sub.backward()
        norch_tensor1_grad_sub = utils.to_torch(norch_tensor1_sub.grad)
        norch_tensor2_grad_sub = utils.to_torch(norch_tensor2_sub.grad)

        torch_tensor1_sub = torch.tensor([[[1, 2.5], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_tensor2_sub = torch.tensor([[[1, 1.], [1, 1.9]], [[1, 1], [1, 1]]], requires_grad=True).to(self.device)
        torch_result_sub = (torch_tensor1_sub - torch_tensor2_sub).sum()
        torch_result_sub.backward()
        torch_tensor1_grad_sub = torch_tensor1_sub.grad
        torch_tensor2_grad_sub = torch_tensor2_sub.grad

        self.assertTrue(utils.compare_torch(norch_tensor1_grad_sub, torch_tensor1_grad_sub))
        self.assertTrue(utils.compare_torch(norch_tensor2_grad_sub, torch_tensor2_grad_sub))
        
    def test_division(self):
        """
        Test autograd from dividing two tensors: tensor1 / tensor2
        """
        norch_tensor1_div = norch.Tensor([[[2, 5.1], [6, -8]], [[10, 12], [14, 16]]], requires_grad=True).to(self.device)
        norch_tensor2_div = norch.Tensor([[[1, 1], [2, 2.2]], [[3, 3], [4, 4]]], requires_grad=True).to(self.device)
        norch_result_div = (norch_tensor1_div / norch_tensor2_div).sum()
        norch_result_div.backward()
        norch_tensor1_grad_div = utils.to_torch(norch_tensor1_div.grad)
        norch_tensor2_grad_div = utils.to_torch(norch_tensor2_div.grad)

        torch_tensor1_div = torch.tensor([[[2, 5.1], [6, -8]], [[10, 12], [14, 16]]], requires_grad=True).to(self.device)
        torch_tensor2_div = torch.tensor([[[1, 1], [2, 2.2]], [[3, 3], [4, 4]]], requires_grad=True).to(self.device)
        torch_result_div = (torch_tensor1_div / torch_tensor2_div).sum()
        torch_result_div.backward()
        torch_tensor1_grad_div = torch_tensor1_div.grad
        torch_tensor2_grad_div = torch_tensor2_div.grad

        self.assertTrue(utils.compare_torch(norch_tensor1_grad_div, torch_tensor1_grad_div))
        self.assertTrue(utils.compare_torch(norch_tensor2_grad_div, torch_tensor2_grad_div))
    
    
    def test_tensor_division_scalar(self):
        """
        Test autograd from dividing tensor by scalar: tensor / scalar
        """
        norch_tensor_div_scalar = norch.Tensor([[[2, 4.7], [6, 8]], [[10, 12], [14, 16]]], requires_grad=True).to(self.device)
        scalar = 2
        norch_result_div_scalar = (norch_tensor_div_scalar / scalar).sum()
        norch_result_div_scalar.backward()
        norch_tensor_grad_div_scalar = utils.to_torch(norch_tensor_div_scalar.grad)

        torch_tensor_div_scalar = torch.tensor([[[2, 4.7], [6, 8]], [[10, 12], [14, 16]]], requires_grad=True).to(self.device)
        torch_result_div_scalar = (torch_tensor_div_scalar / scalar).sum()
        torch_result_div_scalar.backward()
        torch_tensor_grad_div_scalar = torch_tensor_div_scalar.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_div_scalar, torch_tensor_grad_div_scalar))
    
    
    def test_scalar_division_tensor(self):
        """
        Test autograd from dividing scalar by tensor: scalar / tensor
        """
        scalar = 2
        norch_tensor_scalar_div = norch.Tensor([[[1, 2.23], [3, 4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        norch_result_scalar_div = (scalar / norch_tensor_scalar_div).sum()
        norch_result_scalar_div.backward()
        norch_tensor_grad_scalar_div = utils.to_torch(norch_tensor_scalar_div.grad)

        torch_tensor_scalar_div = torch.tensor([[[1, 2.23], [3, 4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_result_scalar_div = (scalar / torch_tensor_scalar_div).sum()
        torch_result_scalar_div.backward()
        torch_tensor_grad_scalar_div = torch_tensor_scalar_div.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_scalar_div, torch_tensor_grad_scalar_div))
    
    
    def test_power_scalar_tensor(self):
        """
        Test autograd from scalar raised to tensor: scalar ** tensor
        """
        scalar = 2
        norch_tensor_power_st = norch.Tensor([[[2, 3.21], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        norch_result_power_st = (scalar ** norch_tensor_power_st).sum()
        norch_result_power_st.backward()
        norch_tensor_grad_power_st = utils.to_torch(norch_tensor_power_st.grad)

        torch_tensor_power_st = torch.tensor([[[2, 3.21], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        torch_result_power_st = (scalar ** torch_tensor_power_st).sum()
        torch_result_power_st.backward()
        torch_tensor_grad_power_st = torch_tensor_power_st.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_power_st, torch_tensor_grad_power_st))
    
    def test_power_tensor_scalar(self):
        """
        Test autograd from tensor raised to scalar: tensor ** scalar
        """
        scalar = 2
        norch_tensor_power_ts = norch.Tensor([[[2, 3], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        norch_result_power_ts = (norch_tensor_power_ts ** scalar).sum()
        norch_result_power_ts.backward()
        norch_tensor_grad_power_ts = utils.to_torch(norch_tensor_power_ts.grad)

        torch_tensor_power_ts = torch.tensor([[[2, 3], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        torch_result_power_ts = (torch_tensor_power_ts ** scalar).sum()
        torch_result_power_ts.backward()
        torch_tensor_grad_power_ts = torch_tensor_power_ts.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_power_ts, torch_tensor_grad_power_ts))

    def test_matmul(self):
        """
        Test autograd from matrix multiplication: matmul(tensor1, tensor2)
        """
        norch_tensor1_matmul = norch.Tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        norch_tensor2_matmul = norch.Tensor([[[1.1, 3], [4, 5]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        norch_result_matmul = (norch_tensor1_matmul @ norch_tensor2_matmul).sum()
        norch_result_matmul.backward()
        norch_tensor1_grad_matmul = utils.to_torch(norch_tensor1_matmul.grad)
        norch_tensor2_grad_matmul = utils.to_torch(norch_tensor2_matmul.grad)

        torch_tensor1_matmul = torch.tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_tensor2_matmul = torch.tensor([[[1.1, 3], [4, 5]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        torch_result_matmul = (torch_tensor1_matmul @ torch_tensor2_matmul).sum()
        torch_result_matmul.backward()
        torch_tensor1_grad_matmul = torch_tensor1_matmul.grad
        torch_tensor2_grad_matmul = torch_tensor2_matmul.grad

        self.assertTrue(utils.compare_torch(norch_tensor1_grad_matmul, torch_tensor1_grad_matmul))
        self.assertTrue(utils.compare_torch(norch_tensor2_grad_matmul, torch_tensor2_grad_matmul))
    
    
    def test_elementwise_mul_scalar(self):
        """
        Test autograd from elementwise multiplication with scalar: scalar * tensor
        """
        scalar = 2
        norch_tensor_elemwise_mul_scalar = norch.Tensor([[[1.1, 2], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        norch_result_elemwise_mul_scalar = (scalar * norch_tensor_elemwise_mul_scalar).sum()
        norch_result_elemwise_mul_scalar.backward()
        norch_tensor_grad_elemwise_mul_scalar = utils.to_torch(norch_tensor_elemwise_mul_scalar.grad)

        torch_tensor_elemwise_mul_scalar = torch.tensor([[[1.1, 2], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_result_elemwise_mul_scalar = (scalar * torch_tensor_elemwise_mul_scalar).sum()
        torch_result_elemwise_mul_scalar.backward()
        torch_tensor_grad_elemwise_mul_scalar = torch_tensor_elemwise_mul_scalar.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_elemwise_mul_scalar, torch_tensor_grad_elemwise_mul_scalar))
    
    
    def test_elementwise_mul_tensor(self):
        """
        Test autograd from elementwise multiplication between two tensors: tensor1 * tensor2
        """
        norch_tensor1_elemwise_mul = norch.Tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        norch_tensor2_elemwise_mul = norch.Tensor([[[1.1, 3], [4, 5]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        norch_result_elemwise_mul = (norch_tensor1_elemwise_mul * norch_tensor2_elemwise_mul).sum()
        norch_result_elemwise_mul.backward()
        norch_tensor1_grad_elemwise_mul = utils.to_torch(norch_tensor1_elemwise_mul.grad)
        norch_tensor2_grad_elemwise_mul = utils.to_torch(norch_tensor2_elemwise_mul.grad)

        torch_tensor1_elemwise_mul = torch.tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_tensor2_elemwise_mul = torch.tensor([[[1.1, 3], [4, 5]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        torch_result_elemwise_mul = (torch_tensor1_elemwise_mul * torch_tensor2_elemwise_mul).sum()
        torch_result_elemwise_mul.backward()
        torch_tensor1_grad_elemwise_mul = torch_tensor1_elemwise_mul.grad
        torch_tensor2_grad_elemwise_mul = torch_tensor2_elemwise_mul.grad

        self.assertTrue(utils.compare_torch(norch_tensor1_grad_elemwise_mul, torch_tensor1_grad_elemwise_mul))
        self.assertTrue(utils.compare_torch(norch_tensor2_grad_elemwise_mul, torch_tensor2_grad_elemwise_mul))

    def test_sin_tensor(self):
        """
        Test autograd from sin operation: sin(tensor)
        """
        norch_sin_tensor = norch.Tensor([[[2, 3.21], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        norch_result_sin_tensor = (norch_sin_tensor.sin()).sum()
        norch_result_sin_tensor.backward()
        torch_result_sin_tensor_grad = utils.to_torch(norch_sin_tensor.grad)

        torch_sin_tensor = torch.tensor([[[2, 3.21], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        torch_expected_sin_tensor = (torch.sin(torch_sin_tensor)).sum()
        torch_expected_sin_tensor.backward()
        torch_expected_sin_tensor_grad = torch_sin_tensor.grad

        self.assertTrue(utils.compare_torch(torch_result_sin_tensor_grad, torch_expected_sin_tensor_grad))
    
    def test_cos_tensor(self):
        """
        Test autograd from cosine operation: cos(tensor)
        """
        norch_cos_tensor = norch.Tensor([[[2, 3.21], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        norch_result_cos_tensor = (norch_cos_tensor.sin()).sum()
        norch_result_cos_tensor.backward()
        torch_result_cos_tensor_grad = utils.to_torch(norch_cos_tensor.grad)

        torch_cos_tensor = torch.tensor([[[2, 3.21], [4, 2.1]], [[6, 7], [8, 9]]], requires_grad=True).to(self.device)
        torch_expected_cos_tensor = (torch.sin(torch_cos_tensor)).sum()
        torch_expected_cos_tensor.backward()
        torch_expected_cos_tensor_grad = torch_cos_tensor.grad

        self.assertTrue(utils.compare_torch(torch_result_cos_tensor_grad, torch_expected_cos_tensor_grad))
    
    
    def test_reshape(self):
        """
        Test autograd from reshaping a tensor: tensor.reshape(shape)
        """
        norch_tensor_reshape = norch.Tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        new_shape = [2, 4]
        norch_result_reshape = norch_tensor_reshape.reshape(new_shape).sum()
        norch_result_reshape.backward()
        norch_tensor_grad_reshape = utils.to_torch(norch_tensor_reshape.grad)

        torch_tensor_reshape = torch.tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_result_reshape = torch_tensor_reshape.reshape(new_shape).sum()
        torch_result_reshape.backward()
        torch_tensor_grad_reshape = torch_tensor_reshape.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_reshape, torch_tensor_grad_reshape))
    
    
    def test_transpose_axes(self):
        """
        Test autograd from transposing a tensor with specific axes: tensor.transpose(axis1, axis2)
        """
        norch_tensor_transpose = norch.Tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        axis1, axis2 = 0, 2
        norch_result_transpose = norch_tensor_transpose.transpose(axis1, axis2).sum()
        norch_result_transpose.backward()
        norch_tensor_grad_transpose = utils.to_torch(norch_tensor_transpose.grad)

        torch_tensor_transpose = torch.tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_result_transpose = torch_tensor_transpose.transpose(axis1, axis2).sum()
        torch_result_transpose.backward()
        torch_tensor_grad_transpose = torch_tensor_transpose.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_transpose, torch_tensor_grad_transpose))
    
    
    def test_T(self):
        """
        Test autograd from transposing a tensor using .T attribute
        """
        norch_tensor_T = norch.Tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        norch_result_T = norch_tensor_T.T.sum()
        norch_result_T.backward()
        norch_tensor_grad_T = utils.to_torch(norch_tensor_T.grad)

        torch_tensor_T = torch.tensor([[[1, 2.1], [3, -4]], [[5, 6], [7, 8]]], requires_grad=True).to(self.device)
        torch_result_T = torch_tensor_T.mT.sum()
        torch_result_T.backward()
        torch_tensor_grad_T = torch_tensor_T.grad

        self.assertTrue(utils.compare_torch(norch_tensor_grad_T, torch_tensor_grad_T))

    def test_reshape_then_matmul(self):
        """
        Test autograd from reshaping a tensor then performing matrix multiplication: matmul(tensor1.reshape(shape), tensor2)
        """
        norch_tensor1 = norch.Tensor([[1, 2.1], [3, -4], [5, 6], [7, 8]], requires_grad=True).to(self.device)
        norch_tensor2 = norch.Tensor([[1, 5.1], [0.1, -4], [0, 6], [7, 8]], requires_grad=True).to(self.device)

        new_shape = [2, 4]

        norch_result_reshape_matmul = (norch_tensor1.reshape(new_shape) @ norch_tensor2).sum()
        norch_result_reshape_matmul.backward()
        norch_tensor_grad_reshape_matmul1 = utils.to_torch(norch_tensor1.grad)
        norch_tensor_grad_reshape_matmul2 = utils.to_torch(norch_tensor2.grad)

        torch_tensor1 = torch.tensor([[1, 2.1], [3, -4], [5, 6], [7, 8]], dtype=torch.float32, requires_grad=True).to(self.device)
        torch_tensor2 = torch.tensor([[1, 5.1], [0.1, -4], [0, 6], [7, 8]], dtype=torch.float32, requires_grad=True).to(self.device)     
        
        torch_result_reshape_matmul = (torch_tensor1.reshape(new_shape) @ torch_tensor2).sum()
        torch_result_reshape_matmul.backward()
        torch_tensor_grad_reshape_matmul1 = torch_tensor1.grad
        torch_tensor_grad_reshape_matmul2 = torch_tensor2.grad
        
        self.assertTrue(utils.compare_torch(norch_tensor_grad_reshape_matmul1, torch_tensor_grad_reshape_matmul1))
        self.assertTrue(utils.compare_torch(norch_tensor_grad_reshape_matmul2, torch_tensor_grad_reshape_matmul2))


    def test_T_then_matmul(self):
        """
        Test autograd from transposing a tensor then performing matrix multiplication: matmul(tensor.T, tensor)
        """
        norch_tensor1 = norch.Tensor([[1, 2.1], [3, -4], [5, 6], [7, 8]], requires_grad=True)
        norch_tensor2 = norch.Tensor([[1, 5.1], [0.1, -4], [0, 6], [7, 8]], requires_grad=True)

        norch_result_T_matmul = (norch_tensor1.T @ norch_tensor2).sum()
        norch_result_T_matmul.backward()
        norch_tensor_grad_T_matmul1 = utils.to_torch(norch_tensor1.grad)
        norch_tensor_grad_T_matmult2 = utils.to_torch(norch_tensor2.grad)

        torch_tensor1 = torch.tensor([[1, 2.1], [3, -4], [5, 6], [7, 8]], dtype=torch.float32, requires_grad=True).to(self.device)
        torch_tensor2 = torch.tensor([[1, 5.1], [0.1, -4], [0, 6], [7, 8]], dtype=torch.float32, requires_grad=True).to(self.device)     
        
        torch_result_T_matmul = (torch_tensor1.T @ torch_tensor2).sum()
        torch_result_T_matmul.backward()
        torch_tensor_grad_T_matmul1 = torch_tensor1.grad
        torch_tensor_grad_T_matmul2 = torch_tensor2.grad
        
        self.assertTrue(utils.compare_torch(norch_tensor_grad_T_matmul1, torch_tensor_grad_T_matmul1))
        self.assertTrue(utils.compare_torch(norch_tensor_grad_T_matmult2, torch_tensor_grad_T_matmul2))

    def todo(self):
        """
        The code has a problem on the following operation
        tensor1.reshape(..) @ tensor1
        print(tensor1.grad)
        (also transpsoe and .T)
        """
        pass

    def test_transpose_axes_then_matmul(self):
        """
        Test autograd from transposing a tensor with specific axes then performing matrix multiplication: matmul(tensor.transpose(axis1, axis2), tensor)
        """
        norch_tensor1 = norch.Tensor([[1, 2.1], [3, -4], [5, 6], [7, 8]], requires_grad=True).to(self.device)
        norch_tensor2 = norch.Tensor([[1, 5.1], [0.1, -4], [0, 6], [7, 8]], requires_grad=True).to(self.device)

        norch_result_transpose_matmul = (norch_tensor1.transpose(0, 1) @ norch_tensor2).sum()
        norch_result_transpose_matmul.backward()
        norch_tensor_grad_transpose_matmul1 = utils.to_torch(norch_tensor1.grad)
        norch_tensor_grad_transpose_matmult2 = utils.to_torch(norch_tensor2.grad)

        torch_tensor1 = torch.tensor([[1, 2.1], [3, -4], [5, 6], [7, 8]], dtype=torch.float32, requires_grad=True).to(self.device)
        torch_tensor2 = torch.tensor([[1, 5.1], [0.1, -4], [0, 6], [7, 8]], dtype=torch.float32, requires_grad=True).to(self.device)  
        
        torch_result_transpose_matmul = (torch_tensor1.T @ torch_tensor2).sum()
        torch_result_transpose_matmul.backward()
        torch_tensor_grad_transpose_matmul1 = torch_tensor1.grad
        torch_tensor_grad_transpose_matmul2 = torch_tensor2.grad
        
        self.assertTrue(utils.compare_torch(norch_tensor_grad_transpose_matmul1, torch_tensor_grad_transpose_matmul1))
        self.assertTrue(utils.compare_torch(norch_tensor_grad_transpose_matmult2, torch_tensor_grad_transpose_matmul2))

if __name__ == '__main__':
    unittest.main()