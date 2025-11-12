import React, { useState, useEffect } from 'react';
/*
Tests and displays data fetched from the backend API endpoints.
*/


// Tests endpoitns by fetching data and displaying databody.
export default function EndpointTest() {

     // State variables to hold fetched data and loading status
    const [data, setData] = useState('');
    const [selectedOption, setSelectedOption] = useState("");
    
    // Array of endpoints to be tested
    const [endpoints, setEndpoints] = useState(['/docs', '/openapi.json', '/v1/genres/recommendations?limit=5', 
        '/v1/genres/recommendations',
        '/v1/genres/music?top_k=5', '/v1/health', '/v1/models',
        '/v1/genres', '/v1/status', '/v1/genres/music']);
    
    // Handle form submission to fetch data from selected endpoint
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Selected endpoint: ", selectedOption);
        
        try {
            fetch("http://localhost:5000" + selectedOption)
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
        </div>
    )
}


