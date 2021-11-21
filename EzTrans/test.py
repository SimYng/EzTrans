import re

a = '''
We proposed a deep convolutional neural network with multi-scale 
feature extraction and recalibration architecture for automatic liver 
and tumor segmentation. Fig. 2 shows the proposed MS-UNet encoder-
decoder architecture. We embed the Res2Net bottleneck module with 
the SE network in place of two 3 × 3 convolution operations in UNet 
encoder-decoder stages. The bottleneck Res2Net module has the same 
architecture, such as bottleneck ResNet except a single 3 × 3 convolu-
tion operation replaced by small 3 × 3 convolutions in hierarchical
'''.replace('- ', '').replace('-\r\n', '').replace('-\n', '').replace('\n', ' ').replace('\r', '').strip().replace('Fig.', 'Fig')

print(a)
print(re.split('([.?])\s', a))
