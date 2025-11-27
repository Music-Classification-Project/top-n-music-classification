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

    // Display predictions via genrecards
    return(
        <>
        <NavBar />
        <div class="flex flex-row overflow-hidden w-auto items-center h-full m-15">
            <div class="flex flex-col w-1/2 h-full justify-center">
                <p class = "font-[DM Sans] text-black text-[60px] tracking-tight">Predictions</p>
                <GenreCard predictions={predictions}/>
            </div>
            <div class="flex flex-col w-1/2 h-full justify-end relative ">
                <RecommendationCard recommendations={recommendations.recommendations} />
                <p class = "absolute font-[DM Sans] right-5 bottom-0 text-black text-[60px]/20 tracking-tight">Similar Music</p>
            </div>
         </div>
        </>
    )
}




