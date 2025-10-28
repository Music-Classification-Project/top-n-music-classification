import numpy as np
import json
import os
import csv
from model_cnn import build_baseline_cnn_model
from keras.utils import to_categorical, Sequence
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint, ReduceLROnPlateau

def get_variables():
    learning_rate = float(input("Input learning rate: (default: 0.00005): " ))
    regularizer_1 = float(input("Input regularizer 1: (default: 0.001): " ))
    regularizer_2 = float(input("Input regularizer 2: (default: 0.001): " ))
    regularizer_3 = float(input("Input regularizer 3: (defualt: 0.001): " ))
    regularizer_4 = float(input("Input regularizer 4: (defualt: 0.001): " ))
    dropout_1 = float(input("Input dropout 1 (default: 0.3): " ))
    dropout_2 = float(input("Input dropout 2 (default: 0.4): "))
    return learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2

def train_model_wrapper(learning_rate=0.00005, regularizer_1=0.001, regularizer_2=0.001, regularizer_3=0.001, regularizer_4=0.001, 
                        dropout_1=0.3, dropout_2=0.4, i=1): 
    BASE_PATH = os.path.abspath('../../data/features/Data')

    #Genres aren't part of .npz files, so I used metadata.json to build a dictionary to map filename to genre
    #Load metadata
    metadata_path = os.path.join(BASE_PATH, 'metadata.json')
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    #Dictionary to associate genre with filename
    filename_to_genre = {entry['filename']: entry['genre'] for entry in metadata}

    #Build label map for neural net
    genres = sorted(list(set(filename_to_genre.values())))
    label_map = {genre: i for i, genre in enumerate(genres)}

    #Build lists of filepaths and labels for neural net
    file_paths = []
    labels = []
    for filename, genre in filename_to_genre.items():
        filename = filename.replace('.wav','.npz')
        full_path = os.path.join(BASE_PATH, genre, filename)
        if os.path.exists(full_path):
            file_paths.append(full_path)
            labels.append(label_map[genre])
        else:
            print(f'Missing file: {full_path}')


    class DataGenerator(Sequence):
        """Generates batches of training data, so all files don't have to be loaded into RAM at once"""
        def __init__(self, file_paths, labels, batch_size, num_classes, shuffle=True):
            self.file_paths = file_paths
            self.labels = labels
            self.batch_size = batch_size
            self.num_classes = num_classes
            self.shuffle = shuffle
            self.indices = np.arange(len(file_paths))

        def __len__(self):
            #Number of batches per epoch
            return int(np.ceil(len(self.file_paths) / self.batch_size))
        
        def __getitem__(self, index):
            start_index = index * self.batch_size
            end_index = (index+1) * self.batch_size
            batch_indices = self.indices[start_index:end_index]
            x_batch = []
            y_batch = []
            for j in batch_indices:
                data = np.load(self.file_paths[j])
                x_batch.append(data['mel_spec'])
                y_batch.append(self.labels[j])
            x_batch = np.array(x_batch)
            y_batch = to_categorical(y_batch, num_classes=self.num_classes)
            return x_batch, y_batch

        def on_epoch_end(self):
            if self.shuffle:
                np.random.shuffle(self.indices)


    #Split data into training and testing sets
    train_paths, test_paths, train_labels, test_labels = train_test_split(file_paths, labels, test_size=0.2, stratify=labels, random_state=27)

    #Build generators
    batch_size = 10
    train_gen = DataGenerator(train_paths, train_labels, batch_size=batch_size, num_classes=len(label_map))
    test_gen = DataGenerator(test_paths, test_labels, batch_size=batch_size, num_classes=len(label_map), shuffle=False)

    #Build model
    model = build_baseline_cnn_model(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2, 
                                     input_shape=(128, 431, 1), num_classes=len(label_map))


    #Callbacks
    #Saves the best model based on validation loss
    checkpoint = ModelCheckpoint(
        filepath='best_model.keras',
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        mode='min'
    )

    #Stops training if validation loss doesn't improve for a number of epochs
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=7, #wait 7 epochs for improvement
        restore_best_weights=True,
        verbose=1
    )

    #Reduce learning rate when validation loss plateaus
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5, # reduce learning rate by half
        patience=3, #wait 3 epochs before reducing
        min_lr=1e-6,
        verbose=1
    )

    tensorboard = TensorBoard(
        log_dir='logs',
        histogram_freq=1
    )

    callbacks = [checkpoint, early_stopping, reduce_lr, tensorboard]

    #Train model
    history = model.fit(
        train_gen,
        validation_data=test_gen,
        epochs=30,
        callbacks=callbacks
    )

    index_used = history.history['val_loss'].index(min(history.history['val_loss']))
    best_loss = history.history['val_loss'][index_used]
    best_accuracy = history.history['val_accuracy'][index_used]
    
    results = {"index": i, "learning_rate": learning_rate, 
           "regularizers": (regularizer_1, regularizer_2, regularizer_3, regularizer_4), 
           "dropouts": (dropout_1, dropout_2),
           "val_loss": best_loss, 
           "val_accuracy": best_accuracy}
    fieldnames = ["index", "learning_rate", "regularizers", "dropouts", "val_loss", "val_accuracy"]
    print(results)

    with open('test_results.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(results) 

    #make new directory and enter into it
    # create a unique run directory and switch into it
    os.chdir("final_models")
    model.save(f'final_model_{i}.keras')
    os.chdir("../")


if __name__ == "__main__":
    # learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2 = get_variables()
    # train_model_wrapper(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)

    for i in range(3):
        learning_rate = 0.00005
        regularizer_1 = 0.0001
        regularizer_2 = 0.0001
        regularizer_3 = 0.0001
        regularizer_4 = 0.0001
        dropout_1 = 0.3
        dropout_2 = 0.4
        train_model_wrapper(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2, i)



    # def reset_dropouts(): 
    #     learning_rate = 0.00005
    #     regularizer_1 = 0.0001
    #     regularizer_2 = 0.0001
    #     regularizer_3 = 0.0001
    #     regularizer_4 = 0.0001
    #     dropout_1 = 0.3
    #     dropout_2 = 0.4
    #     return learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2

     
    # learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2 = reset_dropouts() 
    # dropouts = [(0.3, 0.3), (0.4, 0.4), (0.5, 0.5), (0.3, 0.4), (0.4, 0.5), (0.3, 0.5), (0.35, 0.45)]
    # for dropout_1, dropout_2 in dropouts:
    #    train_model_wrapper(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)

    # learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2 = reset_dropouts() 
    # learning_rates =  [0.00005, 0.00001, 0.0001, 0.0005, 0.001]
    # for learning_rate in learning_rates:
    #    train_model_wrapper(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)

    # learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2 = reset_dropouts() 
    # regularizers = [(0.001, 0.001, 0.001, 0.001), (0.01, 0.01, 0.01, 0.01), (0.0001, 0.0001, 0.0001, 0.0001), (0.01, 0.005, 0.001, 0.001)]
    # for regularizer_1, regularizer_2, regularizer_3, regularizer_4 in regularizers:
    #     train_model_wrapper(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)

    # learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2 = reset_dropouts()
    # train_model_wrapper(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)

