# Copyright 2023 The Deeper-I Authors. All Rights Reserved.
#
# BSD 3-Clause License
# 
# Copyright (c) 2017, 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# -*- coding: utf-8 -*-

import numpy as np



class Optimization:
    def __init__(
        self, 
        use_transform:bool=False, 
        bit:int=4, 
        max_scale:float=4.0,
        use_pruning:bool=False, 
        prun_weight:float=0.50,
        method:str='L1',
        transpose:bool=False,
        shape:list=None,
        ):

        self.bit = bit
        self.use_transform = use_transform
        self.use_pruning = use_pruning
        self.prun_weight = prun_weight
        self.method = method
        self.transpose = transpose

        self.dtype = np.float32 
        self.max_scale = float(max_scale)
        self.bit_scale = int(bit - 1)
        self.num_scale = np.power(2, self.bit_scale).astype(np.int32)
        self.map_scale = self._get_coeff()
        if shape is not None:
            self.set_shape(shape)
            
    def _get_coeff(self):
        map_scale = []
        for i in range(self.num_scale):
            coeff = np.power(0.5, i)
            map_scale.append((self.max_scale * coeff)[..., None])

        map_scale = np.concatenate(map_scale, axis=-1)
        return map_scale

    def _transform(self, x):
        '''
        x: (h,w,i,o)
        x_mag: (i,o)
        method = 'L1' or 'L2' default=L1
    
        Map means metrics with extended dimension
        '''
        xdtype = x.dtype
        # Check argument 
        if self.bypass_transform:
            return x
            
        x = x.astype(self.dtype)
        ones = np.ones_like(x, dtype=self.dtype)
        zeros = np.zeros_like(x, dtype=self.dtype)
    
        # Map of sign - Plus=1, Minus=-1
        x_sign = np.where(x >= zeros, ones, -ones) # (h,w,i,o)
    
        # Magnitude
        if self.method =='L2':
            x_mag = np.mean(np.sqrt(np.square(x)), axis=self.kernel_axis) # (i,o)
        else:
            x_mag = np.mean(np.abs(x), axis=self.kernel_axis) # (i,o)
    
        # No Scale bit
        if self.bit_scale < 1:
            x_p = np.where((x >= zeros), x_mag * ones, zeros) # (h,w,i,o)
            x_n = np.where((x < zeros), -x_mag * ones, zeros) # (h,w,i,o)
            x = x_p + x_n

        # Scale bit
        else:
            map_scale = self.map_scale[None, None, :] * x_mag[..., None] # (i,o,bb)

            # Map of weight
            map_diff = np.abs(np.abs(x)[..., None] - map_scale)
            indices = np.argmin(map_diff, axis=-1)[..., None]
            map_x = np.ones_like(map_diff, dtype=self.dtype) * map_scale
            x = np.take_along_axis(map_x, indices, axis=-1)[..., 0] * x_sign

        x = x.astype(xdtype)
        return x

    def _pruning(self, x): 
        """
        Pruning optimization
        x: (h,w,i,o)
        o: (h,w,i,o) or (i,o)
        """
        xdtype = x.dtype
        x = x.astype(self.dtype)
        x_mag = np.mean(np.abs(x), axis=self.kernel_axis)

        if not self.use_pruning: 
            return np.ones_like(x_mag, dtype=x.dtype)
    
        m_mag = np.mean(x_mag, axis=0)[None, :]
    
        mask = np.where(
            np.less(x_mag, m_mag * self.prun_weight), 
            np.zeros_like(x_mag, dtype=self.dtype), 
            np.ones_like(x_mag, dtype=self.dtype)
        ) # (i,o)
    
        mask = mask.astype(xdtype)
        return mask

    def optimize(self, x):
        '''
        x is AutoCastDistribuedVariable
        '''
        x = np.transpose(x, self.transpose_axis)
        x_tr = self._transform(x)
        x_mask = self._pruning(x)
        x_opt = x_tr * x_mask
        x = np.transpose(x_opt, self.transpose_axis)
        return x

    def set_shape(self, shape):
        self.shape = shape
        self.bypass_transform = (self.bit < 1) or not self.use_transform
        self.kernel_axis = tuple(range(len(shape) - 2))

        if len(self.shape) == 4:
            if self.transpose:
                self.transpose_axis = (0,1,3,2)
            else:
                self.transpose_axis = (0,1,2,3)
        elif len(self.shape) == 3:
            if self.transpose:
                self.transpose_axis = (0,2,1)
            else:
                self.transpose_axis = (0,1,2)
