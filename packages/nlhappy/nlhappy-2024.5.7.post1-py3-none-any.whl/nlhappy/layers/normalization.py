import torch.nn as nn
import torch

class LayerNorm(nn.Module):
    def __init__(self, 
                 hidden_size:int, 
                 conditional_size:int,
                 eps:float=1e-12, 
                 weight:bool =True,
                 bias:bool = True,
                 norm_mode:str = 'normal',
                 **kwargs):
        """layernorm 层，这里自行实现，目的是为了兼容 conditianal layernorm，使得可以做条件文本生成、条件分类等任务
           条件layernorm来自于苏剑林的想法，详情：https://spaces.ac.cn/archives/7124
        """
        super(LayerNorm, self).__init__()
        if weight:
            self.weight = nn.Parameter(torch.ones(hidden_size))
        if bias:
            self.bias = nn.Parameter(torch.zeros(hidden_size))
        self.norm_mode = norm_mode

        self.eps = eps
        self.conditional_size = conditional_size
        if conditional_size:
            # 条件layernorm, 用于条件文本生成,
            # 这里采用全零初始化, 目的是在初始状态不干扰原来的预训练权重
            self.dense1 = nn.Linear(conditional_size, hidden_size, bias=False)
            self.dense1.weight.data.uniform_(0, 0)
            self.dense2 = nn.Linear(conditional_size, hidden_size, bias=False)
            self.dense2.weight.data.uniform_(0, 0)

    def forward(self, inputs, cond=None):
        """
        Args:
            inputs (B, L, H): 特征输入.
            cond (_type_, optional): 条件输入. Defaults to None.
        """
        if self.norm_mode == 'rmsnorm':
            # t5使用的是RMSnorm
            variance = inputs.to(torch.float32).pow(2).mean(-1, keepdim=True)
            o = inputs * torch.rsqrt(variance + self.eps)
        else:
            # 归一化是针对于inputs
            u = inputs.mean(-1, keepdim=True)
            s = (inputs - u).pow(2).mean(-1, keepdim=True)
            o = (inputs - u) / torch.sqrt(s + self.eps)

        if not hasattr(self, 'weight'):
            self.weight = 1
        if not hasattr(self, 'bias'):
            self.bias = 0

        if self.conditional_size:
            # 三者的形状都是一致的
            for _ in range(len(inputs.shape) - len(cond.shape)):
                cond = cond.unsqueeze(dim=1)
            return (self.weight + self.dense1(cond)) * o + (self.bias + self.dense2(cond))
        else:
            return self.weight * o + self.bias