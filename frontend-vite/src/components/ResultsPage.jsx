import React, { Component } from "react";
import NavBar from "./NavBar";
import GenreCard from "./GenreCard";
import { useParams } from "react-router-dom";
import RecommendationCard from "./RecommendationCard";


/** 
 * Results Page
 * Displays results returned from /v2/genres/music API
 * Displays recommended music
 */

export default function ResultsPage() {
    // Grab passed parameters & convert to JSON.
    const params = useParams();
    const predictions = params.predictions;
    const recommendations = params.recommendations;
    console.log(`RESULTS PAGE: Data received fron upload form: ${predictions, recommendations}`)

    // Display predictions and recommendations
    return(
        <>
            <NavBar />
            <div class="flex m-10 flex-row justify-center align-center h-full w-full -z-40 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]">
                <div class="flex self-center align-center w-full justify-center -z-5 inset-0 rounded-full bg-[#8E9C78]/20 size-60/100">
                    <div class="flex flex-col mx-10 w-full">
                        <h1 class = "flex-auto -tracking-1 leading-18 font-[DM Sans] text-black text-[60px] tracking-tight">Predictions</h1>
                        <GenreCard predictions={predictions}/>
                    </div>
                </div>
                <div class="flex self-center align-center justify-center w-full ">
                    <div class="flex flex-col m-10 w-full relative ">
                        <RecommendationCard recommendations={recommendations.recommendations} />
                        <p class = "absolute font-[DM Sans] right-5 bottom-0 text-black text-[60px]/20 tracking-tight">Similar Music</p>
                    </div>
                </div>
             </div>
        </>
    )
}




