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
    <div class="flex flex-col border-b border-r-3 border-double  p-3 size-9/10">
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
            <div key={index} class="flex flex-row items-center justify-between overflow-hidden w-9/10 border-b-1 border-customgrey ">
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

                <div class="self-right w-2/3 rounded-r-full  h-8">
                    <div class={`${color} h-full rounded-r-full`} 
                    style={{width: modifiedConfidence*3}}></div>
                </div>
        </div>
    )
}
