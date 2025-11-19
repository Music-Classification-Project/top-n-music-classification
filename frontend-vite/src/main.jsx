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
    <div class="flex divide-x-3 h-full align-middle">
      <div class="self-center align-center w p-5">
      <h1 class = "font-[DM Sans] -tracking-1 leading-20 text-left text-[90px] ">Music Classification Project.</h1>
      <p class="font-[DM Sans] text-left text-[13px] text-lightgrey py-5">Top-n Music Genre Classification Neural Network, aims to improve the accuracy of music genre classification and enhance the user experience when searching for similar songs. This project allows users to upload an audio clip and receive a formatted list of the top-n predicted genres, sorted by confidence values in descending order. This system could serve as a foundation for improved playlist generation and recommendation engines in music applications. Furthermore, our stretch goals include creating a web application that helps users discover related music and refine their searches for similar songs. In addition, user feedback could be incorporated to further train the model and improve accuracy metrics.</p>
      </div>
      <div class="w-full self-center">tester</div>
    </div>
  </StrictMode>,
)
