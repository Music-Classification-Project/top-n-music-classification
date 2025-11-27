import React from "react"
import { useState } from "react"
import { useParams } from "react-router-dom"

/**
 * 
 * @returns Card that displays song recommendations
 * 
 */

export default function ReccomendationCard(){
        const params = useParams()
        let recommendationList = JSON.parse(params.recommendations)
        recommendationList = recommendationList['recommendations']
        console.log('List of recommendations sent to genre card: ', recommendationList)

    
        return(
        <div class="flex flex-col border border-bg-darkgreen/20 justify-center m-7 bg-box-fill/5 p-10">
            {recommendationList.map((recommendation, index) => 
                <RecommendationValue artist={recommendation.artist} title={recommendation.title} index={index} />
            )}
        </div>     )
}
function RecommendationValue({artist, title, index}){
    return(
       <div key={index} class="text-nowrap p-2">
                <div class=" font-[DM Sans] tracking-tighter text-rec-text/65 text-[32px]">
                    Song {index+1}
                </div>
                <div class ="font-[DM Sans] text-anothergrey text-[15px]">
                    <strong>Title:</strong> {title} | <strong>Artist: </strong>{artist}
                </div>
        </div>
    )

}



