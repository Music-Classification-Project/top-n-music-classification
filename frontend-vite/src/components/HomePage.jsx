import UploadElement from "./UploadElement"

/* Homepage that contains:
1. Project Title
2. Upload Component 
3. Navigation Bar 
*/
export default function HomePage() {

const description = "Top-n Music Genre Classification Neural Network, aims to improve the accuracy of music genre classification and enhance the user experience when searching for similar songs. This project allows users to upload an audio clip and receive a formatted list of the top-n predicted genres, sorted by confidence values in descending order. This system could serve as a foundation for improved playlist generation and recommendation engines in music applications. Furthermore, our stretch goals include creating a web application that helps users discover related music and refine their searches for similar songs. In addition, user feedback could be incorporated to further train the model and improve accuracy metrics."
const title = "Music Classification Project."

return( 
  <div class="flex flex-row h-screen w-screen relative gap-10">
    <div class='flex flex-col bg-[url(../../public/images/the-doors.jpg)] w-50/100 p-4 h-full -z-100 absolute left-0'>
      <div class="flex items-center flex-col w-full h-full p-15 justify-center-safe bg-black/60 ">
        <div class= "flex flex-col text-white justify-start p-2 space-y-4 ">
          <h1 class = "font-[DM Sans] -tracking-1 leading-18 text-left text-[90px] max-w-160 ">{title}</h1>
          <p class="font-[DM Sans] text-left text-[16px] text-lightgrey max-w-170">{description}</p>
        </div>
      </div>
  </div>
      <div class="flex h-full w-50/100 flex-col text-darkest-green border-forest-green border-l-10 border-double absolute right-0 ">
      <div class="flex h-4/10 top-0 bg-dusty-gray/80  bg-[url(../../public/images/concert-1.jpg)] bg-bottom  hue-rotate-600"> </div>
        <div class="flex flex-col h-6/10 justify-center items-center border-t-10 border-forest-green border-double w-full ">
          <UploadElement />
        </div>
      </div>
  </div>


);
};
