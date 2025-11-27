import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import TopBarProgress from "react-topbar-progress-indicator";


createRoot(document.getElementById('root')).render(
  
  <StrictMode>
  <App />
  </StrictMode>,
)
