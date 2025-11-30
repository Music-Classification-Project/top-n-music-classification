import React from "react"
import { useParams } from "react-router-dom"
import { useState } from "react"

/**
 * 
 * @returns Card that displays text
 */

export default function GenreCard(){
    const params = useParams()
    let predictionList = JSON.parse(params.predictions)
    predictionList = predictionList['predictions']


    predictionList.sort((a, b) => b.confidence - a.confidence);
    console.log('List of predictions that was sent to  the genre card: ', predictionList)
    const colors = [
         'bg-bar-darkest', 
         'bg-bar-dark', 
         'bg-bar-mid', 
         'bg-bar-green', 
         'bg-bar-light'
    ]

     console.log(predictionList)
    return(
    <div class="flex flex-col border-r-3 border-double border-b-2 m-10 p-5 w-8/10">
        {predictionList.map((prediction, index) => 
            <CardValue genre={prediction.genre} confidence={prediction.confidence} index={index} color={colors[index]} />
        )}
    </div>
    )
}

function CardValue({genre, confidence, index, color}) {
    let modifiedConfidence = parseFloat(confidence)*100
    let modifiedGenre = genre.charAt(0).toUpperCase() + genre.slice(1)

    return(
            <div key={index} class="flex mx-2 text-nowrap border-b-1 border-midgreen/80 justify-between w-full items-center space-x-2 px-2 ">
                <div class="font-[DM Sans] text-anothergrey/50 text-left text-[60px]">
                    0{index+1}
                </div>
                <div>
                    <div class ="font-[crimson] text-darkgrey text-[20px]">
                        {modifiedGenre}
                    </div>
                    <div class ="font-[DM Sans] text-grey">
                        {modifiedConfidence.toFixed(2)}%
                    </div>
                </div>

                <div class="self-right w-2/3 rounded-r-full h-10 w-full p-2 ">
                    <div class={`${color} h-full rounded-r-full`} 
                    style={{width: modifiedConfidence*3}}></div>
                </div>
        </div>
    )
}
