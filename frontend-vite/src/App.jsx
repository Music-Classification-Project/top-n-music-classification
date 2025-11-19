import './App.css'
import HomePage from './components/HomePage'
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from 'react-router-dom';


function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route index element = {<HomePage />}/>
      </Routes>
    </BrowserRouter>
  );
};

export default App
