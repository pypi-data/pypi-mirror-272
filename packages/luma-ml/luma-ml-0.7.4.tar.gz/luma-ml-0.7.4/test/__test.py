import __local__
from luma.neural.optimizer import AdamOptimizer
from luma.neural.loss import CrossEntropy
from luma.neural.network import LeNet_1, LeNet_4, LeNet_5


model = LeNet_5(optimizer=AdamOptimizer())
model.summarize(in_shape=(100, 1, 28, 28))
