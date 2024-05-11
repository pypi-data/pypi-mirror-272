# PyNorch
Recreating PyTorch from scratch (C/C++, CUDA and Python, with GPU support and automatic differentiation!)

# 1 - About
**PyNorch** is a deep learning framework constructed using C/C++, CUDA and Python. This is a personal project with educational purpose only! `Norch` means **NOT** PyTorch, and we have **NO** claims to rivaling the already established PyTorch. The main objective of **PyNorch** was to give a brief understanding of how a deep learning framework works internally. It implements the Tensor object, GPU support and an automatic differentiation system. 

# 2 - Installation
Install this package from PyPi

```css
$ pip install norch
```

or from cloning this repository
```css
$ sudo apt install nvidia-cuda-toolkit
$ git clone https://github.com/lucasdelimanogueira/PyNorch.git
$ cd build
$ make
$ cd ..
```

# 3 - Get started
### 3.1 - Tensor operations
```python
import norch

x1 = norch.Tensor([[1, 2], 
                  [3, 4]], requires_grad=True).to("cuda")

x2 = norch.Tensor([[4, 3], 
                  [2, 1]], requires_grad=True).to("cuda)

x3 = x1 @ x2
result = x3.sum()
result.backward

print(x1.grad)
```

### 3.2 - Create a model

```python
import norch
import norch.nn as nn
import norch.optim as optim

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(1, 10)
        self.sigmoid = nn.Sigmoid()
        self.fc2 = nn.Linear(10, 1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.sigmoid(out)
        out = self.fc2(out)
        
        return out
```