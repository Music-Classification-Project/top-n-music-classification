from train_model import train_model_wrapper, get_variables
import csv 
import ast

def reset_metrics():
    """Function to set metrics to preferred metrics. Requires user input. This can be passed into testing functions"""
    learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2 = get_variables()
    return {"regularizer_list": [(regularizer_1, regularizer_2, regularizer_3, regularizer_4)], "dropouts_list": [(dropout_1, dropout_2)], 
            "learning_rate": [learning_rate], "val_accuracy": None, "val_loss": None}

def get_best_metrics_so_far(): 
    """Gets the metrics associated with the lowest loss. This can be passed into testing functions"""
    with open('record_changes_updated.csv', mode='r', newline='') as csv_file:
        val_loss = float(1000000)
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_val_loss = row['val_loss']
            if float(new_val_loss) < float(val_loss):
                val_loss = new_val_loss
                best_record = row 
    regularizers = ast.literal_eval(best_record['regularizers'])
    regularizer_list = [regularizers]
    dropouts = ast.literal_eval(best_record['dropouts'])
    dropouts_list = [dropouts]
    learning_rate = [best_record['learning_rate']]
    val_accuracy = [best_record['val_accuracy']]
    val_loss = [best_record['val_loss']]
    
    return {"regularizer_list": regularizer_list, "dropouts_list": dropouts_list, "learning_rate": learning_rate, "val_accuracy": val_accuracy, "val_loss": val_loss}

def learning_rates(get_params=get_best_metrics_so_far, learning_rate_list=[0.0005, 0.0005]): 
    """Loops through provided list of learning rates and tests model for each. Records results in record_changes.csv"""
    metrics = get_params()
    # dropouts = metrics_get("dropouts_list")[0]
    dropout_1, dropout_2 = metrics.get("dropouts_list")[0][0], metrics.get("dropouts_list")[0][1]
    regularizers = metrics.get("regularizer_list")[0]
    regularizer_1, regularizer_2, regularizer_3, regularizer_4 = regularizers[0], regularizers[1], regularizers[2], regularizers[3]
    # Learning Rates 
    learning_rates =  learning_rate_list 
    for learning_rate in learning_rates:
        results = run_model_and_add_to_csv(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)
    return results 

def dropouts(get_params=get_best_metrics_so_far, 
            dropout_list = [(0.3, 0.3), (0.4, 0.4), (0.5, 0.5), (0.3, 0.4), (0.4, 0.5), (0.3, 0.5), (0.35, 0.45)]): 
    """
    Loops through provided list of dropout tuples in the format [(dropout_1, dropout_2), (dropout_1, dropout_2)]
    and builds model with each. Saves results in record_changes.csv 
    """
    metrics = get_params()
    learning_rate = metrics.get("learning_rate")[0]
    regularizers = metrics.get("regularizer_list")[0]
    regularizer_1, regularizer_2, regularizer_3, regularizer_4 = regularizers[0], regularizers[1], regularizers[2], regularizers[3]
    # Learning Rates 
    dropouts =  dropout_list 
    for dropout_list in dropouts:
        dropout_1 = dropout_list[0]
        dropout_2 = dropout_list[1]
        results = run_model_and_add_to_csv(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)
    return results

def regularizers(get_params=get_best_metrics_so_far, regularizer_list=[(0.001, 0.001, 0.001, 0.001)]): 
    """
    Loops through provided list of dropout tuples in the format [(regularizer_1, regularizer_2, regularizer_3, regularizer_4), 
    (regularizer_1, regularizer_2, regularizer_3, regularizer_4)] and builds model with each. Saves results in record_changes.csv 
    """
    metrics = get_params()
    learning_rate = metrics.get("learning_rate")[0]
    dropout_1, dropout_2 = metrics.get("dropouts_list")[0][0], metrics.get("dropouts_list")[0][1]
    # Learning Rates 
    regularizers =  regularizer_list 
    for regularizer_list in regularizers:
        regularizer_1 = regularizer_list[0]
        regularizer_2 = regularizer_list[1]
        regularizer_3 = regularizer_list[2]
        regularizer_4 = regularizer_list[3]
        results = run_model_and_add_to_csv(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2)
    return results 

def run_model_and_add_to_csv(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2, results=[]):
    """Main function for running model and saving results in record_changes.csv, called in testing functions"""
    history = train_model_wrapper(learning_rate, regularizer_1, regularizer_2, regularizer_3, regularizer_4, dropout_1, dropout_2) # will add to CSV 

    # index_used = history.history['val_loss'].index(min(history.history['val_loss']))
    # best_loss = history.history['val_loss'][index_used]
    # best_accuracy = history.history['val_accuracy'][index_used]

    # # Add to list 
    # record = {"learning_rate": learning_rate, 
    # "regularizers": (regularizer_1, regularizer_2, regularizer_3, regularizer_4), 
    # "dropouts": (dropout_1, dropout_2),
    # "val_loss": best_loss, 
    # "val_accuracy": best_accuracy}
    # results.append(record)

    # Add to CSV  
    fieldnames = ["learning_rate", "regularizers", "dropouts", "val_loss", "val_accuracy"]
    # print(results)

    with open('record_changes_updated.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(results) 
    
    return results 


if __name__ == "__main__":
    # results = get_best_metrics_so_far()
    # print(results) 
    learning_rates(reset_metrics, [float(0.001)])
    dropouts(reset_metrics, [(0.3, 0.4)])
    regularizers(reset_metrics, [(0.001, 0.001, 0.001, 0.001)])