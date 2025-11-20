import React from "react";
import NavBar from "./NavBar";
import { useNavigation } from "react-router-dom";

/** 
 * Results Page
 * Displays results returned from /v2/genres/music API
 * Displays recommended music
 */

export default function() {


    return(
        <>
        <NavBar />
        <div class="flex divide-x-3 h-full align-middle">
            <div class="self-center align-center w-full p-5">
                <h1 class = "font-[DM Sans] -tracking-1 leading-20 text-left text-[20px] ">Results</h1>
                <div>
                </div>
        </div>
    </div>
        </>

    );
};