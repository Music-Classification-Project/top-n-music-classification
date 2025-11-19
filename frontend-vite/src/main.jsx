import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Endpoint from './components/endpoint-test/EndpointTest.jsx'
import './index.css'
import App from './App.jsx'
import Navbar from './components/NavBar.jsx'
import MainBody from './components/MainBody.jsx'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar />
    <div class="flex flex-row w-full ">
      <div class="w-full">tester</div>
      <div class="w-full">tester</div>
    </div>
  </StrictMode>,
)
