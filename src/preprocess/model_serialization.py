import keras
"""
Handles final model serialization.
Best model weights and architecture are saved for
future inference and evaluation.
"""


def save_and_serialize_model(model='best_model.keras'):
    # Load the model
    model = keras.models.load_model(model)
    # Serialize model to JSON
    json_config = model.to_json()
    with open('model_config.json', 'w') as f:
        f.write(json_config)
    # Save model
    model.save('best_model.h5')


def deserialize_model(model_path='best_model.h5'):
    # Load JSON and create model
    with open('model_config.json', 'r') as f:
        json_config = f.read()
    model = keras.models.model_from_json(json_config)
    # Load weights into new model
    model.load_weights('best_model.h5')
    return model


if __name__ == "__main__":
    save_and_serialize_model()
    deserialize_model()
