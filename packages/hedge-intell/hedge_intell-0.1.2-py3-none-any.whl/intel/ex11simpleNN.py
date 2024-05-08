import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# Generate some random data for demonstration
np.random.seed(42)
X = np.random.rand(100, 2)
y = np.random.randint(0, 2, (100,))

# Define the architecture of the neural network
model = Sequential()
model.add(Dense(4, input_dim=2, activation='relu'))  # Input layer with 2 features and 4 neurons
model.add(Dense(1, activation='sigmoid'))  # Output layer with 1 neuron and sigmoid activation

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10, batch_size=10, verbose=1)

# Evaluate the model
loss, accuracy = model.evaluate(X, y)
print("Model loss:", loss)
print("Model accuracy:", accuracy)
