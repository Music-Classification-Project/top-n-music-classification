import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout

# Load saved NumPy arrays X = song_features & y = song_genres
data = np.load("jonas_sandbox/features_and_labels.npz", allow_pickle=True)
X, y = data["X"], data["y"]

# Encode labels: ['Rock', 'Jazz', 'Rock', ...] becomes [0, 1, 0, ...]
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Convert to one-hot:
# [
#  [0, 0, 1, 0],   # rock
#  [0, 1, 0, 0],   # jazz
#  [1, 0, 0, 0],   # metal
#  [0, 0, 0, 1],   # pop
#  ...
# ]
y_onehot = to_categorical(y_encoded)

# Save encoder classes if needed for later inference
label_classes = encoder.classes_

# Split into training (80%) and test (20%) sets, which are the same for every
# run, determined by the random seed of 42. The training and test sets have
# roughly the same proportion of each music genre as the original dataset.
X_train, X_test, y_train, y_test = train_test_split(
    X, y_onehot, test_size=0.2, random_state=42, stratify=y_onehot
)

# --- Build keras model ---

# Determine size of model's output layer
num_genres = y_onehot.shape[1]  # number of cols in the one-hot encoded labels

# Determine size of model's input layer
input_shape = X_train.shape[1]  # number of MFCC features, usually 40

# Define architecture of Sequential Keras model:
"""
This creates a simple Feedforward Neural Network (FNN) with three layers:
- Input/Hidden Layer 1: A Dense layer with 256 neurons, using the ReLU
  (Rectified Linear Unit) activation function. The input_shape tells the model
  how many features to expect.
- Hidden Layer 2: A Dense layer with 128 neurons, also using ReLU activation.
- Output Layer: A Dense layer with num_genres (e.g., 4) neurons. It uses the
  Softmax activation function, which outputs a probability distribution over
  the genre classes (e.g., 80% Rock, 15% Jazz, 5% Metal, 0% Pop).

Dropout: The Dropout(0.3) layers randomly ignore 30% of the neurons during
training in the preceding layer. This is a regularization technique used to
prevent overfitting, making the model generalize better to unseen data.
"""
model = Sequential([
    Dense(256, activation='relu', input_shape=(input_shape,)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(num_genres, activation='softmax')  # output layer
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=30,
    batch_size=32
)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy:.2f}")

# Save model for later inference
model.save("jonas_sandbox/music_genre_model.h5")
