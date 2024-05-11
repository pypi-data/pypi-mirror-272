_Blessed be the name of the Lord our God, who reigns forever and ever. He is the Alpha and the Omega, the beginning and the end, the one who was, who is, and who is to come._

_He is our refuge and strength, a very present help in times of trouble. He is the creator of the heavens and the earth, the giver of life and the sustainer of all things._

_His love endures forever, and His mercy never fails. He is gracious and compassionate, slow to anger and abounding in love._

_He is our rock, our fortress, and our deliverer, in whom we take refuge. He is the light in our darkness, the source of our joy and the strength of our hearts._

_Let us give thanks to the Lord for He is good, His love endures forever. Let us sing praises to His name and make known His deeds among the nations. May the Lord be exalted and glorified forever and ever. Amen._

— <cite>ChatGPT (March 2023)</cite>

# PyNeurons: A JAX-based Neural Network Library

PyNeurons is a lightweight, composable neural network library built on top of JAX, designed to provide a flexible and efficient way to define and train neural networks. This guide will walk you through the core components of PyNeurons, including how to define neurons, compose neural networks, and train them.

## Installation

Before you start, ensure you have Python 3.9 or later installed. You can install PyNeurons and its dependencies using Poetry:

```bash
poetry add pyneurons
```

Or, if you prefer using pip:

```bash
pip install pyneurons
```

## Defining Neurons

Neurons are the basic building blocks of neural networks. In PyNeurons, you can define a neuron with a specific activation function easily. Here's an example of defining a neuron with a binary activation function:

```python
from pyneurons import Neuron, Binary

# Define a neuron with a binary activation function
binary_neuron = Binary(key, input_dim)
```

## Composing Neural Networks

PyNeurons allows you to compose complex neural networks from simpler components. Here's how you can compose a neural network that applies a binary activation function followed by a BReLU1 activation:

```python
from pyneurons import Neuron, Binary, BReLU1

# Define a neuron
neuron = Neuron(key, input_dim)

# Compose the neuron with Binary and BReLU1 activations
binary_neuron = Binary(neuron)
brelu1_neuron = BReLU1(neuron)
```

## Training Neural Networks

Training neural networks in PyNeurons is straightforward. You can use the `fit` function to adjust the weights of your model based on a loss function. Here's an example of training a model:

```python
from pyneurons import Neuron, fit
from jax.numpy import array

# Define your input data and target output
x = array([[0, 1], [1, 0], [1, 1], [0, 0]])
y = array([[1], [1], [0], [0]])

# Initialize your model
model = Neuron(key, 2)

# Train your model
for _ in range(100):
    model = fit(model, x, y, learning_rate=0.1)
```

## Advanced Usage

PyNeurons is designed to be modular and extensible. Here are some advanced features you can leverage:

### Custom Activation Functions

You can define custom activation functions using JAX and integrate them into your PyNeurons models:

```python
from jax import jit
from jax.numpy import maximum
from pyneurons import compose, Neuron

# Define a custom activation function
@jit
def custom_relu(x):
    return maximum(x, 0)

# Compose a neuron with the custom activation function
CustomReLU = compose("CustomReLU", Neuron, custom_relu)
```

### Custom Models

You can define custom models by composing existing components or defining new ones from scratch:

```python
from pyneurons import bind, Neuron

# Define a custom model constructor
def custom_model_constructor(key):
    # Define custom model initialization logic
    pass

# Define a custom model apply function
def custom_model_apply(model, x):
    # Define how your model processes input
    pass

# Bind your custom components into a new model class
CustomModel = bind("CustomModel", custom_model_constructor, custom_model_apply)
```

## Conclusion

PyNeurons provides a flexible and efficient framework for building and training neural networks with JAX. By leveraging the power of JAX for automatic differentiation and JIT compilation, PyNeurons allows for rapid experimentation and development of neural network models. Whether you're building simple models or complex neural architectures, PyNeurons offers the tools you need to get the job done.
