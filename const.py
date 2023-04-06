LABEL_SCALE = 100
HIDDEN=64
DROP=0.2
BATCH_SIZE=32
HIS_LEN=100
PSEUDO=1000
NEIGHBOR_LEN=100 
CLIP=0.1
LR=0.01
EPS=1
EPOCH=3

# NOTE: 
# LABEL_SCALE：标签缩放因子，用于调整标签的权重。
# HIDDEN：神经网络中隐藏层的大小。
# DROP：dropout的概率，用于防止过拟合。
# BATCH_SIZE：每个客户端在每轮训练中使用的样本数。
# HIS_LEN：历史信息的长度。
# PSEUDO：伪交互的数量
# NEIGHBOR_LEN：邻居节点的数量。
# CLIP：梯度裁剪的阈值。
# LR：学习率，用于控制模型参数更新的速度。
# EPS：epsilon值。
# EPOCH：训练轮数。