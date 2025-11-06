# top-n-music-classification

### File Structure:  
#### data   
    /raw       : Includes raw data.  
    /processed : Includes data after normalization.   
    /features  : Includes data after feature extraction.  
#### docs   
    Includes documentation.   
#### src  
    /preprocess : Files needed for data pipeline to load and process data.    
        /download_data.py          : Downloads datasets.    
        /preprocess_data.py        : Cleans and preprocesses data.    
        /extract_features.py       : Extracts features from provided file path.   
        /process_data.py           : Combines download, process, and extract files into one smooth pipeline.     
        /model_cnn.py              : Baseline CNN Architecture
        /save_and_serialization.py : Serializes and saves model weights.
        /train_model.py            : Implementation of training pipeline.
        /tune_hyperparams.py.      : Expreiments with model configurations and training parameters.
    /data_analysis                 : Files needed for the analysis of raw, processed, and normalized data  
        /output                    : Output of data analysis   
        /dataset_analysis.py       : Analyzes raw, processed, and normalized data    

#### sandbox
    For the purpose of testing scripts. Each developer has their own folder here as needed. 
