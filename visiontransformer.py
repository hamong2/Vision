# -*- coding: utf-8 -*-
"""VisionTransformer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HmeQvV3bq1d65oHFFno3U27mYUu_r2tj
"""

!pip install einops

import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

from torch import nn
from torch import Tensor
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from einops.layers.torch import Rearrange, Reduce
from torchsummary import summary

class PatchEmbedding(nn.Module):
  def __init__(self, in_channels: int = 3, patch_size: int = 16, emb_size: int = 768):
    self.patch_size = patch_size
    super().__init__()
    self.projection = nn.Sequential(
        Rearrange('b c (h s1) (w s2) -> b (h w) (s1 s2 c)', s1=patch_size, s2=patch_size),
        nn.Linear(patch_size*patch_size*in_channels,emb_size)
    )
    self.cls_token = nn.Parameter(torch.randn(1,1,emb_size))
    self.positions = nn.Parameter(torch.randn((img_size//patch_size)**2+1, emb_size))

  def forward(self, x: Tensor) -> Tensor:
    b, _, _, _ = x.shape
    x = self.projection(x)
    cls_tokens = repeat(self.cls_token, '() n e -> b n e', b=b)
    x = torch.cat([cls_tokens,x], dim=1)
    x += self.positions
    return x

# Attention 
class MultiHeadAttention(nn.Module):
  queries = Rearrange(self.queries(x), "b n (h d) -> b h n d", h=self.n_heads)
  keys = Rearrange(self.keys(x), "b n (h d) - > b h n d", h = self.n_heads)
  values = Rearrange(self.values(x), "b n (h d) -> b h n d", h=self.n_heads)

  energy = torch.einusum('bhqd, bhkd-> bhqk', queries, keys)
  out = torch.einusum('bhal, bhlv -> bhav', att, values)

from PIL import Image
 
# 이미지 열기
im = Image.open('test.jpg')
 
# 이미지 크기 출력
print(im.size)

trans = Compose([Resize((100,100)), 
                            ToTensor(),
                            Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))])
testTensor = trans(im)

testTensor.shape

patcher = Rearrange('c (h s1) (w s2) -> (h w) (s1 s2 c)', s1 = 10, s2 = 10)
tensor_to_patch = patcher(testTensor)

tensor_to_patch.shape

pro = nn.Linear(10*10*3,300)
proo = pro(tensor_to_patch)

proo.shape

