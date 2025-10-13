import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout

data = np.load("jonas_sandbox/features_and_labels.npz", allow_pickle=True)
X, y = data["X"], data["y"]

# If y is string labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Convert to one-hot
y_onehot = to_categorical(y_encoded)

# Save encoder classes if needed for later inference
label_classes = encoder.classes_

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_onehot, test_size=0.2, random_state=42, stratify=y_onehot
)

# Build keras model
num_genres = y_onehot.shape[1]
input_shape = X_train.shape[1]  # number of MFCC features, usually 40

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
