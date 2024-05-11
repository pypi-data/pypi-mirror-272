# Copyright 2023 The Deeper-I Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import tensorflow as tf
from tensorflow.keras import layers

from . import dpi_layers as dlayers
from .xwn import keras_layers as klayers



##############
# Block layers
##############
@tf.keras.utils.register_keras_serializable()
class Conv1DBlock(layers.Layer):

    def __init__(
        self, 
        filters, 
        kernel_size, 
        strides=1, 
        padding='valid', 
        data_format=None,
        dilation_rate=1, 
        activation=None, 
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        groups=1,
        # Components
        convolution=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['CONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        kwargs["dtype"] = "float16" if dtype == "mixed_float16" else dtype
        super(Conv1DBlock, self).__init__(**kwargs)
        kwargs["dtype"] = dtype
        kwargs["groups"] = groups

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout

        self.filters = filters
        self.kernel_size = kernel_size

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.max_scale = max_scale
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = False

        # Conv
        if convolution is None:
            self.conv = klayers.Conv1D(
                filters, 
                kernel_size,
                strides=strides, 
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                # dtype=dtype,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'CONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
            'dtype' : self.dtype,
            # 'groups' : self.groups,
        }
        base_config = super(Conv1DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class Conv2DBlock(layers.Layer):

    def __init__(
        self, 
        filters, 
        kernel_size, 
        strides=(1,1), 
        padding='valid', 
        data_format=None,
        dilation_rate=(1,1), 
        activation=None, 
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        groups=1,
        # Components
        convolution=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['CONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        kwargs["dtype"] = "float16" if dtype == "mixed_float16" else dtype
        super(Conv2DBlock, self).__init__(**kwargs)
        kwargs["dtype"] = dtype
        kwargs["groups"] = groups

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout
        
        self.filters = filters
        self.kernel_size = kernel_size
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = False
        
        # Conv
        if convolution is None:
            self.conv = klayers.Conv2D(
                filters, 
                kernel_size,
                strides=strides, 
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                # dtype=dtype,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'CONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
            'dtype' : self.dtype,
            # 'groups' : self.groups,
        }
        base_config = super(Conv2DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class DWConv2DBlock(layers.Layer):

    def __init__(
        self,
        kernel_size,
        strides=(1,1),
        padding='valid',
        depth_multiplier=1,
        data_format=None,
        dilation_rate=(1,1),
        activation=None,
        use_bias=False,
        depthwise_initializer='glorot_uniform',
        bias_initializer='zeros',
        depthwise_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        depthwise_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Components
        convolution=None,
        batchnormalization=None,
        dropout=None,
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['CONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        kwargs["dtype"] = "float16" if dtype == "mixed_float16" else dtype
        super(DWConv2DBlock, self).__init__(**kwargs)
        kwargs["dtype"] = dtype

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout

        self.kernel_size = kernel_size
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = False

        # Conv
        if convolution is None:
            self.conv = klayers.DepthwiseConv2D(
                kernel_size,
                strides=strides,
                padding=padding,
                depth_multiplier=depth_multiplier,
                data_format=data_format,
                dilation_rate=dilation_rate,
                use_bias=use_bias,
                depthwise_initializer=depthwise_initializer,
                bias_initializer=bias_initializer,
                depthwise_regularizer=depthwise_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                depthwise_constraint=depthwise_constraint,
                bias_constraint=bias_constraint,
                # dtype=dtype,

                use_transform=self.use_transform,
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'CONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'kernel_size' : self.kernel_size,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
            'dtype' : self.dtype,
        }
        base_config = super(DWConv2DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class FCBlock(layers.Layer):

    def __init__(
        self, 
        units,
        activation=None,
        use_bias=True,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Components
        multiply_accumulate=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization - Reserved
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['FC', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        kwargs["dtype"] = "float16" if dtype == "mixed_float16" else dtype
        super(FCBlock, self).__init__(**kwargs)
        kwargs["dtype"] = dtype

        # Assign
        self.act = activation
        self.bn = batchnormalization
        self.dropout = dropout

        self.units = units
        
        # Conv
        if multiply_accumulate is None:
            self.fc = layers.Dense(
                units, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                # dtype=dtype,
                **kwargs,
            )
        else:
            self.fc = multiply_accumulate

        self.layer_list = []
        for o in order:
            if o == 'FC': self.layer_list.append(self.fc)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'units' : self.units,
            'multiply_accumulate' : self.fc,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
            'dtype' : self.dtype,
        }
        base_config = super(FCBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class TConv2DBlock(layers.Layer):

    def __init__(
        self, 
        filters, 
        kernel_size, 
        strides=(1,1), 
        padding='valid', 
        data_format=None,
        dilation_rate=(1,1), 
        activation=None, 
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        groups=1,
        # Components
        convolution=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['TCONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        kwargs["dtype"] = "float16" if dtype == "mixed_float16" else dtype
        super(TConv2DBlock, self).__init__(**kwargs)
        kwargs["dtype"] = dtype
        kwargs["groups"] = groups

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout
        
        self.filters = filters
        self.kernel_size = kernel_size
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = True
        
        # TConv
        if convolution is None:
            self.conv = klayers.Conv2DTranspose(
                filters, 
                kernel_size,
                strides=strides, 
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                # dtype=dtype,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'TCONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
            'dtype' : self.dtype,
            # 'groups' : self.groups,
        }
        base_config = super(TConv2DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class SBConv2DBlock(layers.Layer):                                                                   
    
    def __init__(                                                                                    
        self, 
        filters:int,
        kernel_size, 
        strides=(1,1), 
        padding='valid',
        data_format=None,
        dilation_rate=(1,1),
        activation=None,
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        groups=1,
        # Custom
        scale_ratio:int=2,
        # Components
        convolution=None,
        batchnormalization=None,
        dropout=None,
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['SPCONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):  
        kwargs["dtype"] = "float16" if dtype == "mixed_float16" else dtype
        super(SBConv2DBlock, self).__init__(**kwargs)
        kwargs["dtype"] = dtype
        kwargs["groups"] = groups

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout
        
        self.scale_ratio = scale_ratio
        self.filters = filters
        self.kernel_size = kernel_size
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = False

        # SPConv
        if convolution is None:
            self.conv = klayers.SubPixelConv2D(
                filters, 
                kernel_size,
                strides=strides,
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias,
                kernel_initializer=kernel_initializer,
                bias_initializer=bias_initializer,
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                # dtype=dtype,

                scale_ratio=scale_ratio,
                transform=transform,
                pruning=pruning,
                max_scale=max_scale,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'SPCONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'scale_ratio' : self.scale_ratio,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
            'dtype' : self.dtype,
            # 'groups' : self.groups,
        }
        base_config = super(SBConv2DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x

@tf.keras.utils.register_keras_serializable()
class PositionEncoder(layers.Layer):
    def __init__(
        self,
        projection=None,
        height=7,
        width=7,
        batch_size=32,
        num_channels=3,
        dtype="float32",
        **kwargs,
    ):
        kwargs["dtype"] = "float16" if dtype == "mixed_float16" else dtype
        super(PositionEncoder, self).__init__(**kwargs)
        kwargs["dtype"] = dtype

        self.projection = projection
        self.num_channels = num_channels
        self.b = batch_size
        self.w = width
        self.h = height
        self.rw = width + 1 if width % 2 != 0 else width
        self.rh = height + 1 if height % 2 != 0 else height

        self.n_half = int(num_channels / 2)
        self.div_term = tf.exp(tf.range(0, self.num_channels, delta=2, dtype=tf.float32) * -(tf.math.log(10000.0) / float(self.num_channels)))

        self.regularizer_rate = 5e-4

    def build(self, input_shape):
        (_, _, _, self.e) = input_shape

    def get_config(self):
        config = {
            'projection' : self.projection,
            'num_channels' : self.num_channels,
            'height' : self.h,
            'width' : self.w,
            'dtype' : self.dtype,
            'batch_size' : self.b,
        }
        base_config = super(PositionEncoder, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, x):
        # Get the positional embeddings.
        sin_ry = tf.range(0, self.rh, delta=2, dtype=tf.float32)
        cos_ry = tf.range(1, self.rh, delta=2, dtype=tf.float32)
        sin_rx = tf.range(0, self.rw, delta=2, dtype=tf.float32)
        cos_rx = tf.range(1, self.rw, delta=2, dtype=tf.float32)

        sin_rx = tf.math.sin(sin_rx[:, None] * self.div_term[None, :])[..., None]   # (W/2,C/2,1)
        cos_rx = tf.math.cos(cos_rx[:, None] * self.div_term[None, :])[..., None]   # (W/2,C/2,1)
        rx = tf.concat([sin_rx, cos_rx], axis=-1)                                   # (W/2,C/2,2)
        rx = tf.reshape(rx, (1, self.rw, self.n_half))[:, :self.w, :]               # (1,W,C/2)
        rx = tf.tile(rx, (self.h, 1, 1))                                            # (H,W,C/2)

        sin_ry = tf.math.sin(sin_ry[:, None] * self.div_term[None, :])[..., None]   # (H/2,C/2,1)
        cos_ry = tf.math.cos(cos_ry[:, None] * self.div_term[None, :])[..., None]   # (H/2,C/2,1)
        ry = tf.concat([sin_ry, cos_ry], axis=-1)                                   # (H/2,C/2,2)
        ry = tf.reshape(ry, (self.rh, 1, self.n_half))[:self.h, ...]                # (H,1,C/2)
        ry = tf.tile(ry, (1, self.w, 1))                                            # (H,W,C/2)

        pos_embeddings = tf.reshape(tf.concat([rx, ry], axis=-1), (1, self.h, self.w, self.num_channels))   # (1,H,W,C)
        pos_embeddings = tf.cast(tf.tile(pos_embeddings, (self.b, 1, 1, 1)), self.dtype)                    # (B,H,W,C)

        # Embed the patches.
        x = x + pos_embeddings
        if self.projection is not None:
            x = self.projection(x)
        return x
                                                                                                                                                                                          725,16        Bot

