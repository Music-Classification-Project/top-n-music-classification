import './App.css'
import HomePage from './components/HomePage'
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from 'react-router-dom';
import ResultsPage from './components/ResultsPage';
import Navbar from './components/NavBar';



function App() {

  return (
    <>
    <Navbar />
    <BrowserRouter>
      <Routes>
        <Route index element = {<HomePage />}/>
        <Route path="/results/:predictions/:recommendations" element={<ResultsPage />} />
      </Routes>
    </BrowserRouter>
    </>
  );
};

export default App
