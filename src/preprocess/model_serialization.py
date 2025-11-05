import keras

"""
Handles final model serialization and reproducibility.
Best model weights and architecture are saved for
future inference and evaluation.
"""


def save_model():
  
    model = keras.models.load_model('best_model.keras')
    model.save('src/preprocess/model_best.h5')


if __name__ == "__main__":
    save_model()
