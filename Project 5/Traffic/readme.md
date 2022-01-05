## Model 1

* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* 1 hidden layer with 128 units,
* 0.5 dropout and 
* Output layer

### `333/333 - 3s - loss: 3.5065 - accuracy: 0.0472`

**Believing the image was not being generalized enough for the neural network to predict other images, I added a convolutional and a max-pooling layer.**

****

## Model 2

* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* **1 convolutional layer 32 filters, 3x3 kernel,**
* **1 max-pooling layer with 2x2 pool size,**
* 1 hidden layer with 128 units,
* 0.5 dropout and 
* Output layer

### `333/333 - 3s - loss: 0.2349 - accuracy: 0.9358`

**Results from my previous model greatly improved in this model, however the accuracy still could be worked on. I now tried adding another hidden layer with 128 units. This would result in increased computational time but greater accuracy. I also added an input layer.**

****


## Model 3 

* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* **Input layer**,
* **1 hidden layer with 128 units**, 
* 1 hidden layer with 128 units,
* 0.5 dropout and 
* Output layer

### `333/333 - 3s - loss: 0.1988 - accuracy: 0.9459`

**Accuracy could be slightly improved, but I was pretty content with the current model. In my next model, I try making the network more robust by changing the dropout rate.**

****


## Model 4 
* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* Input layer,
* 1 hidden layer with 128 units, 
* 1 hidden layer with 128 units,
* **0.7 dropout** and 
* Output layer

### `333/333 - 3s - loss: 0.1666 - accuracy: 0.9567`

**Changing the dropout rate to 0.7 improved accuracy greatly. But I soon came to the conclusion that the dropout rate was not global but infact only for the layer that it was placed after in the code. After this discovery, I decreased dropout rate greatly and added a dropout to each layer. I found a dropout rate of 0.25 on each layer to be the most accurate.**

****


## Model 5
* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* Input layer,
* 1 hidden layer with 128 units, 
* **0.25 dropout**,
* 1 hidden layer with 128 units,
* **0.25 dropout** and 
* Output layer

### `333/333 - 4s - loss: 0.1714 - accuracy: 0.9585`

****


## Some Observations
* Changing the matrix of the convolutional layers to **1x1** made the accuracy extremely low, which I soon realised meant not altering the image at all, and was effectively removing the convolutional layers.
* Changing the matrix of the convolutional layers to **5x5** decreased the accuracy to 85%, which would suggest that the image was being generalized a little too heavily.
* Changing pool size to **4x4** decreased accuracy to 0.67, **removing** pool layers increased computational times fourfold (13s -> 50s), but provided the same accuracy in the end (about 95%)
* [Source](https://towardsdatascience.com/simplified-math-behind-dropout-in-deep-learning-6d50f3f47275 "towardsdatascience.com/") states that a dropout rate of **0.5** provides the greatest regularization, however my testings with 0.5 dropout rate, my accuracy differs a fair amount. `333/333 - 4s - loss: 0.6406 - accuracy: 0.7924`

****



# Final Model

## Model 6


* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* 1 convolutional layer 32 filters, 3x3 kernel,
* 1 max-pooling layer with 2x2 pool size,
* Input layer,
* 1 hidden layer with 128 units, 
* 0.25 dropout,
* 1 hidden layer with 128 units,
* 0.25 dropout and 
* Output layer

`Epoch 1/10
500/500 [==============================] - 15s 29ms/step - loss: 2.8626 - accuracy: 0.3581
Epoch 2/10
500/500 [==============================] - 15s 29ms/step - loss: 1.1796 - accuracy: 0.6491
Epoch 3/10
500/500 [==============================] - 15s 29ms/step - loss: 0.7185 - accuracy: 0.7812
Epoch 4/10
500/500 [==============================] - 15s 29ms/step - loss: 0.5234 - accuracy: 0.8401
Epoch 5/10
500/500 [==============================] - 15s 29ms/step - loss: 0.3806 - accuracy: 0.8861
Epoch 6/10
500/500 [==============================] - 15s 29ms/step - loss: 0.3303 - accuracy: 0.9050
Epoch 7/10
500/500 [==============================] - 14s 29ms/step - loss: 0.2783 - accuracy: 0.9206
Epoch 8/10
500/500 [==============================] - 14s 29ms/step - loss: 0.2526 - accuracy: 0.9274
Epoch 9/10
500/500 [==============================] - 14s 29ms/step - loss: 0.2123 - accuracy: 0.9431
Epoch 10/10
500/500 [==============================] - 15s 29ms/step - loss: 0.1777 - accuracy: 0.9524
333/333 - 4s - loss: 0.1340 - accuracy: 0.9639
`

### `333/333 - 4s - loss: 0.1340 - accuracy: 0.9639`

****


