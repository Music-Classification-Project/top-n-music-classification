import React, { useState, useEffect } from "react";

/**
 * 
 * Tests backend connection. Tests and displays data fetched from the backend API.
 */

export default function App() {

    // State variables to hold fetched data and loading status
    const [items, setItems] = useState([]);
    const [predictions, setPredictions] = useState([]);
    const [dataIsLoaded, setDataIsLoaded] = useState(false);

    // Fetch data from the backend API 
    useEffect(() => {
        fetch("/v1/genres/recommendations?limit=5")
            .then((res) => res.json())
            .then((json) => {
                setItems(json);
                setDataIsLoaded(true);
            });
    }, []); 
     // Fetch data from the backend API 
    useEffect(() => {
        fetch("/v1/genres/music?top_k=5")
            .then((res) => res.json())
            .then((json) => {
                setPredictions(json);
                setDataIsLoaded(true);
            });
    }, []); 
    // Render loading message if data is not yet loaded
    if (!dataIsLoaded) {
        return (
            <div>
                <h1>Please wait some time....</h1>
            </div>
        );
    }



  // Render the fetched data
  return (
        <div className="App">
            <h1> Connection Test: Recommendations</h1>
            <div className="container">
              {items['recommendations'].map((item) => (
                    <div className="item" key={item.id}>
                        <ol>
                            <div>
                                <strong>Title: </strong>
                                {item.title},
                            </div>
                            <div>Artist: {item.artist}</div>
                            <div>Genre: {item.genre}</div>
                        </ol>
                    </div>
                ))}
            </div>
            <h1> Connection Test: Predictions</h1>
            <div className="container">
              {predictions.map((prediction) => (
                    <div className="genre" key={genre.id}>
                        <ol>
                          {predictions["genre"]}
                        </ol>
                    </div>
                ))}
            </div>
        </div>
    );
}
