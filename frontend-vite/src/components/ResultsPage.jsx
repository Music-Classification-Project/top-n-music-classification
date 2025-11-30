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
            <div class="flex justify-center items-center -z-10 h-full bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]">
                <div class="flex items-center min-w-300 max-w-320 justify-center w-9/10 h-9/10 m-5 gap-1 overflow-auto">
                    <div class="flex flex-col items-center w-1/2 justify-center relative -z-5 rounded-full bg-midgreen/15  ">
                            <h1 class = "absolute tracking-tight top-0 left-0 font-[DM Sans] text-black text-[65px]/20 tracking-tight">Predictions</h1>
                            <GenreCard predictions={predictions}/>
                    </div>
                    <div class="flex flex-col relative w-1/2">
                        <RecommendationCard recommendations={recommendations.recommendations} />
                        <h1 class = "absolute font-[DM Sans] right-5 bottom-0 text-black text-[65px]/20 tracking-tight">Similar Music</h1>
                    </div>
                </div>
             </div>
        </>
    )
}




