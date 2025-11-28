import React, { useState } from 'react';
import upload from "../assets/cloud-upload.svg";
import { data, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BallTriangle } from 'react-loader-spinner'



function UploadElement(){
    /*
    Allows user to upload a file from their local drive.
    File is sent to the backend via a POST request.
    Data received is then displayed below the file upload form.
    */
   // SET file
    const [selectedFile, setSelectedFile] = useState();
    const [isLoading, setIsLoading] = useState(false);
    let navigate = useNavigate();
    const handleChange= (event) => {
        setSelectedFile(event.target.files[0])
    }

    const LoadingComponent = () => {
    return(
    <BallTriangle
        height={100}
        width={100}
        radius={5}
        color="#a98a4d79"
        ariaLabel="ball-triangle-loading"
        wrapperStyle={{}}
        wrapperClass=""
        visible={true}
                        />)}

    //Action to be performed while rendering the next screen.
    const getData = async () => {
        setIsLoading(true)
        await new Promise(resolve => setTimeout(resolve, 2000)); 
        setIsLoading(false); 
    }

    // Saves the file as a formdata object and submits the data to v1/genres/music 
    const handleSubmit = (event) => {
        event.preventDefault()
        const url =  `http://localhost:5000`;
        const formData = new FormData();
        
        // Add File Data
        formData.append('file', selectedFile);

        /* 
        SEND POST requests to /v1/genres/.. to receive: 
         1. Recommendations
         2. Genres
          */
        getData()
        axios.all([
            axios.post(`${url}/v1/genres/recommendations`, formData),
            axios.post(`${url}/v1/genres/music`, formData)
        ])
        .then(axios.spread((recommendations, predictions) =>{
            console.log('Genres received: ', predictions.data, 'Recommendations received: ', recommendations.data)
            navigate(`/results/${JSON.stringify(predictions.data)}/${JSON.stringify(recommendations.data)}`)
        }))
        .catch(function(error){
            console.log(error)
        });
        }; 

    // IF file is selected return file details. Else, prompt the user to select a file.
    const fileData = () => {
        if (selectedFile && selectedFile.type.match('audio.*')) {
            return (
                <div class ="text-lightgrey">
                    <div class="font-bold">Uploaded:</div>
                    <p class="flex "> {selectedFile.name} </p>
                </div>
            )} 
            
            else if (selectedFile && !selectedFile.type.match('audio.*')) {
                return(
                <div class="p-4 mb-4 text-sm text-fg-warning rounded-base bg-warning-soft" role="alert">
                    <span class="font-medium">Wrong file type!</span> Only audio files accepted.
                </div>)
        }
        else {
            return (
                    <h4>Choose an audio file before selecting upload.</h4>
            );
        };
    };

        return (
            // Upload Form
            <form onSubmit={handleSubmit} >
                <fieldset>
                    <div class='flex h-full flex-col align-center items-center justify-centerr'>
                        <label >
                            {isLoading ? (
                            <div class='grid grid-cols-1 justify-center items-center m-4'><LoadingComponent /><h1 class='font-bold m-2 text-15'>Loading...</h1></div>) :
                            (<div class="border-1 border-dashed border-mid green grid grid-cols-1 m-2 h-auto justify-items-center">
                            <div class="font-[DM Sans] font-bold text-gray-800">Upload</div>
                            <img  src={upload} class="object-scale-down cursor-pointer h-40 w-90" alt="upload icon" />
                            <input class='cursor-pointer' type="file" id="doc" name="doc" onChange={ handleChange } hidden/>
                            <div>Drag & drop files</div>    
                            </div>)}
                        </label>
                        <div class = "grid grid-cols-1 w-auto-full m-2 h-auto">
                            <button class="text-white bg-midgreen rounded-sm cursor-pointer hover:bg-success-strong h-full focus:ring-4 focus:success-subtle shadow-xs text-small w-full focus:outline-none"
                            type = "submit">
                            UPLOAD FILE </button> 
                            {fileData()} 
                        </div>
                    </div>
                </fieldset>
             </form>     
    )
}
export default UploadElement