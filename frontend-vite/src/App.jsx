import './App.css'
import HomePage from './components/HomePage'
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from 'react-router-dom';
import ResultsPage from './components/ResultsPage';


function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route index element = {<HomePage />}/>
        <Route path='results' element = {<ResultsPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App
