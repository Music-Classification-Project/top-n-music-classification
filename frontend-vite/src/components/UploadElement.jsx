import React, { useState } from 'react';
import axios from 'axios';
import upload from "../assets/cloud-upload.svg";

function UploadElement(){
    /*
    Allows user to upload a file from their local drive.
    File is sent to the backend via a POST request.
    Data received is then displayed below the file upload form.
    */
   // SET file
    const [selectedFile, setSelectedFile] = useState(null);
    const apiUrl = "http://localhost:5000"

    // Set selected file when user chooses a file
    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0])
    }

    // Saves the file as a Formdata object 
    const onFileUpload = () => {
        const formData = new FormData();
        formData.append(
            "myFile",
            selectedFile,
            selectedFile.name
        );
        console.log(selectedFile);
        axios.post(`${apiUrl}/v1/genres/music`, selectedFile);
    };

    // IF file is selected return file details. Else, prompt the user to select a file.
    const fileData = () => {
        if (selectedFile) {
            return (
                <div class ="text-left text-lightgrey">
                    <div class="font-bold">Uploaded:</div>
                    <p class="flex border-1 border-solid border-lightgreen px-2 my-2"> {selectedFile.name} </p>
                </div>
            );
        } else {
            return (
                    <h4>Choose a file before selecting upload.</h4>
            );
        };
    };

    // Handle form submission to fetch data from selected endpoint
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Selected endpoint: ", selectedOption);
        
        try {
            fetch(`${apiUrl}` + selectedOption)
            .then((res) => res.text())
            .then((text) => {
                setData(text);
            }); 
        }
        catch (error) {
            console.error("Error fetching data from endpoint:", error);
        }}; 

        return (
        <fieldset>
            <label for="doc">

                <div class="border-1 border-dashed border-lightgreen align-center my-4 grid grid-cols-1 justify-items-center">
                    <div>
                        <div class="font-[DM Sans] font-bold text-gray-800">Upload</div>
                    </div>
                    <img src={upload} class="object-scale-down h-40 w-90" alt="upload icon" />
                        <input type="file" id="doc" name="doc" onChange = {onFileChange} hidden/>
                    <div>Drag & drop files</div>
                </div>

                <div class="py-4">
                    <div class="">
                    {fileData()}
                    </div>
                    <button 
                    class="text-white bg-midgreen rounded-sm hover:bg-success-strong focus:ring-4 focus:success-subtle shadow-xs text-small  w-full py-1.5 my-2 focus:outline-none"
                    onClick={onFileUpload}>
                    UPLOAD FILE
                    </button>
                    
                </div>
            
            </label>
        </fieldset>
    )

}


    

export default UploadElement