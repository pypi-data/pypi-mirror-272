import __local__
from luma.neural.optimizer import AdamOptimizer
from luma.neural.layer import Activation
from luma.neural.loss import CrossEntropy
from luma.neural.network import LeNet_5

from luma.preprocessing.encoder import OneHotEncoder
from luma.model_selection.split import TrainTestSplit

from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

mnist = fetch_openml("mnist_784", version=1)
X = mnist.data.values.reshape(-1, 1, 28, 28)
y = mnist.target.values.astype(int)

X = (
    np.pad(
        X,
        pad_width=((0, 0), (0, 0), (2, 2), (2, 2)),
        mode="constant",
        constant_values=0,
    )
    / 255.0
)
y = OneHotEncoder().fit_transform(y.reshape(-1, 1))

X_train, X_test, y_train, y_test = TrainTestSplit(
    X,
    y,
    test_size=0.2,
).get

model = LeNet_5(
    optimizer=AdamOptimizer(),
    activation=Activation.ReLU(),
    loss=CrossEntropy(),
    initializer="he",
    batch_size=128,
    n_epochs=2,
    learning_rate=0.001,
    shuffle=True,
    deep_verbose=True,
)

print(*model.model.layers, sep="\n")
model.fit(X_train, y_train)
score = model.score(X_test, y_test.argmax(axis=1))

plt.plot(model.running_loss_, lw=1, label="Running Loss")
plt.xlabel("Batches")
plt.ylabel("Loss")
plt.title(f"{str(model)} on MNIST [Acc: {score:.4f}]")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
