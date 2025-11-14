import React, { useState, useEffect } from 'react';
import axios from 'axios';
const apiUrl = import.meta.env.VITE_API_URL;

/*
Tests and displays data fetched from the backend API endpoints.
*/

// Backend: https://flask-backend-444703047901.us-central1.run.app/
// Backend Dev: http://localhost:5000 

// Tests endpoitns by fetching data and displaying databody.
export default function EndpointTest() {

     // State variables to hold fetched data and loading status
    const [data, setData] = useState('');
    const [selectedOption, setSelectedOption] = useState("");
    const [selectedFile, setSelectedFile] = useState(null);

    // Set selected file when user chooses a file
    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    // Saves the file as a Formdata object 
    const onFileUpload = () => {
        const formData = new FormData();
        formData.append(
            "myFile",
            selectedFile,
            selectedFile.name
        );

        //TODO: get this working.
        console.log(selectedFile);
        axios.post(`${apiUrl}/v1/genres/music`, selectedFile);
    };    

    // IF file is selected return file details. Else, prompt the user to select a file.
    const fileData = () => {
        if (selectedFile) {
            return (
                <div>
                    <h2>File Details:</h2>
                    <p>File Name: {selectedFile.name}</p>
                    <p>File Type: {selectedFile.type}</p>
                </div>
            );
        } else {
            return (
                <div>
                    <br />
                    <h4>Choose a file before pressing the upload button</h4>
                    </div>
            );
        }
    };
    
    // Array of endpoints to be tested
    const [endpoints, setEndpoints] = useState(['/docs', '/openapi.json', '/v1/genres/recommendations?limit=5', '/test',
        '/v1/genres/recommendations',
        '/v1/genres/music?top_k=5', '/v1/health', '/v1/models',
        '/v1/genres', '/v1/status', '/v1/genres/music']);
    
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
        <div>
            <h1>Endpoint Testing</h1>
            <div>Tests backend endpoints. Data fetched from each endpoint will appear below your selection.</div>
            
            <fieldset>
                <form action='#' method="get">
                    <label for="endpoint">Endpoint: </label>
                    <select 
                        name="endpoint" 
                        id="endpoint" 
                        value={selectedOption}
                        onChange={(e) => 
                        setSelectedOption(e.target.value)}>
                        {endpoints.map((endpoint) => (
                            <option value={endpoint} key={endpoint.id}>{endpoint}</option>
                        ))}
                    </select>

                    <button type="submit" value="submit" onClick={handleSubmit}>Show Data</button>
                    
                    <div>
                        <h2>Data Received:</h2>
                        <div>{data}</div>
                    </div>

                </form>
            </fieldset>

            <div>
                <h2>File Upload Test</h2>
                <input type="file" onChange={onFileChange} />
                <button onClick={onFileUpload}>
                    Upload!
                </button>
            </div>
            {fileData()}
        </div>
    )
}


