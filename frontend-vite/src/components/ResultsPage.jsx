import React, { Component } from "react";
import NavBar from "./NavBar";
import GenreCard from "./GenreCard";
import { useParams } from "react-router-dom";


/** 
 * Results Page
 * Displays results returned from /v2/genres/music API
 * Displays recommended music
 */

export default function ResultsPage() {
    // Grab passed parameters & convert to JSON.
    const params = useParams();
    const parameters = params.predictions;
   
    console.log(`RESULTS PAGE: Data received fron upload form: ${parameters}`)
    // Parse Predictions
    const predictionsJSON = JSON.parse(parameters)
    let predictions = predictionsJSON.predictions

    // Display predictions via genrecards
    return(
        <>
        <NavBar />
        <div class="flex flex-row overflow-hidden h-80% m-15">
            <div class="flex flex-col w-1/2">
                <p class = "font-[DM Sans] text-left text-black/75 text-[60px]/20 tracking-tight">Predictions</p>
                <GenreCard predictions={predictions.predictions}/>
            </div>
            <div class="relative flex flex-col justify-end w-1/2 flex-auto">
                <p class = "absolute font-[DM Sans] right-0 bottom-0 text-black/75 text-[60px]/20 tracking-tight">Similar Music</p>
            </div>
         </div>
        </>
    )
}




