import UploadElement from "./UploadElement"
import NavBar from "./NavBar"

/* Homepage that contains:
1. Project Title
2. Upload Component 
3. Navigation Bar 
*/
export default function HomePage() {

return( 
    <>
    <NavBar />
      <div class="flex flex-row divide-x-3 h-full my-15 flex-auto sticky">
        <div class="flex flex-col align-center w-1/2 px-10 flex-auto">
          <h1 class = "flex-auto flex font-[DM Sans] -tracking-1 leading-20 text-left text-[90px] ">Music Classification Project.</h1>
          <p class="flex font-[DM Sans] text-left text-[13px] text-lightgrey py-5">Top-n Music Genre Classification Neural Network, aims to improve the accuracy of music genre classification and enhance the user experience when searching for similar songs. This project allows users to upload an audio clip and receive a formatted list of the top-n predicted genres, sorted by confidence values in descending order. This system could serve as a foundation for improved playlist generation and recommendation engines in music applications. Furthermore, our stretch goals include creating a web application that helps users discover related music and refine their searches for similar songs. In addition, user feedback could be incorporated to further train the model and improve accuracy metrics.</p>
        </div>
      <div class="flex flex-col self-center  w-1/2 px-10 flex-auto"><UploadElement /></div>
    </div>
    </>
);
};
