import React, { Component } from "react";
import NavBar from "./NavBar";
import TextCard from "./TextCard"
import { useParams } from "react-router-dom";
import RadialChart from "./RadialChart";


/** 
 * Results Page
 * Displays results returned from /v2/genres/music API
 * Displays recommended music
 */

export default function ResultsPage() {
    const params = useParams();
    const parameters = params.predictions;
    const predictionsJSON = JSON.parse(parameters)
    let predictions = predictionsJSON.predictions
    console.log(predictions)

    let chartData = predictions.map(item => {
        {
        name: item.genre
        x: item.confidence
        fill: '#ffa658'
        }
    })

    console.log(chartData)

    
   
     // Sample data
    const data = [
        { name: 'A', x: 1, fill: "green" },
        { name: 'B', x: 2, fill: "yellow" },
        { name: 'C', x: 3, fill: "aqua" },
        { name: 'D', x: 4, fill: "blue" },
        { name: 'E', x: 5, fill: "orange" },
        { name: 'F', x: 6, fill: "red" },
        { name: 'G', x: 7, fill: "black" },
        { name: 'H', x: 8, fill: "purple" },
        { name: 'I', x: 9, fill: "gray" },
    ];

    console.log(data)

    return(
        <>
        <NavBar />
        <div class="flex flex-row w-.1 my-5 stick self-center">
            <div class="flex object-contain flex-col w-1/2 px-5 flex-auto h-fit">
                <p class = "font-[DM Sans] text-left text-black/75 text-[60px]/20 tracking-tight">Predictions</p>
                <TextCard predictions={predictions.predictions}/>
            </div>
            <div class="flex object-contain flex-col w-1/2 px-5 flex-auto h-fit">
                <RadialChart predictions={predictions.predictions}/>
                <p class = "font-[DM Sans] text-left text-black/75 text-[60px]/20 tracking-tight">Data</p>
            
            </div>
         </div>
        </>
    )
}




