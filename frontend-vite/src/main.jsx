import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Endpoint from './components/endpoint-test/EndpointTest.jsx'
import './index.css'
import App from './App.jsx'
import Navbar from '././components/navbar/NavBar.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar />
    <Endpoint />
  </StrictMode>,
)
