import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState(null);

  // Function to call the Flask backend
  const fetchMessageFromFlask = () => {
    // Replace with your actual backend URL in production
    const apiUrl = 'https://flask-backend-444703047901.us-central1.run.app/test'; // UPDATE THIS 

    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        setMessage(data.message);  // Set the message from the backend to state
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setMessage('Error connecting to Flask backend');
      });
  };

  return (
    <div className="App">
      <h1>React + Flask Connection Test</h1>
      <button onClick={fetchMessageFromFlask}>Get Message from Flask</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;