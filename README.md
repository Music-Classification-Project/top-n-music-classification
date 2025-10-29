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
        /download_data.py    : Downloads datasets.    
        /preprocess_data.py  : Cleans and preprocesses data.    
        /extract_features.py : Extracts features from provided file path.   
        /process_data.py     : Combines download, process, and extract files into one smooth pipeline.  
    /data_analysis : Files needed to analyze pre and post processing data
        /output              : Contains the results of data analysis. Contains PNG and TXT files with plots and statistics respectively.
            /raw             : Contains results from raw dataset.
            /normalized      : Contains results from normalized dataset.
            /processed       : Contains results from processed dataset.
        /dataset_analysis.py : Analyzes raw and normalized data.
    

#### sandbox
    For the purpose of testing scripts. Each developer has their own folder here as needed. 
