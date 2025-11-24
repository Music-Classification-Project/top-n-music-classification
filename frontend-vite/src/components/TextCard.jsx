import React from "react"
import { useState } from "react"
import { useParams } from "react-router-dom"

/**
 * 
 * @returns Card that displays text
 */

export default function TextCard(){
    const params = useParams()
    const [count, setCount] = useState(1)
    let predict = JSON.parse(params.predictions)
    predict = predict['predictions']
    predict.sort((a, b) => b.confidence - a.confidence);
    console.log('PREEDICT', predict)

    return(
    <div class="flex flex-col border-r p-3">
    {predict.map((genre, index) => 
        <GenreCard genre={genre} count={index} />
    )}
    </div>
    )
}

function GenreCard({genre, count}) {
    let confidence = genre.confidence 

    console.log(genre)
    return(
        <div class="flex flex-row w-full mx-2 ">
            <div class="flex flex-row w-full h-27 items-end  border-b-1 border-customgrey ">
                <div class="-tracking-1 size-27 font-[DM Sans] text-coolgreen/50 text-[80px]">
                    0{count+1}
                </div>
                <div class="mx-2 size-18">
                    <div class ="font-[crimson] text-darkgrey text-[18px]">
                        {genre.genre}
                    </div>
                    <div class ="font-[DM Sans] text-grey">
                        {genre.confidence}
                    </div>
                </div>
                <div class="m-4 w-full border-1 rounded-full h-5">
                    <div class="bg-darkgrey bg-orange-bright/70 h-4 rounded-full" style={{width: confidence}}></div>
                </div>
            </div>
            

        </div>
    )
}
