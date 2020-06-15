import tensorflow as tf
import numpy as np

'''
This code was developed by following Victor Zhou's CNN tutorial, found at:
    https://towardsdatascience.com/training-a-convolutional-neural-network-from-scratch-2235c2a25754
'''

#this method splits the mnist db into training and test images and labels
(img_train, lbl_train), (img_test, lbl_test) = tf.keras.datasets.mnist.load_data()

#the images are transformed to [-0.5, 0.5] range, to make them easier to work with.
img_train, img_test = (img_train/255)-0.5, (img_test/255)-0.5

img_train, img_test = np.expand_dims(img_train, axis = 3), np.expand_dims(img_test, axis = 3)

model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, 3, input_shape = (28, 28, 1), use_bias = False),
        tf.keras.layers.MaxPooling2D(pool_size = 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

model.compile(tf.keras.optimizers.Adam(lr=0.0002), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
    img_train,
    tf.keras.utils.to_categorical(lbl_train),
    batch_size=1,
    epochs=10,
    validation_data=(img_test, tf.keras.utils.to_categorical(lbl_test))
    )