import React from "react";
import soundWave from "../../public/images/audio-wave.svg";

/* Navbar Element - to be placed in header of every page. */

const Navbar = () => {
    /*
    Navbar to be displayed at the header of every page.
    */
   
    return ( 
        <nav class="flex flex-grow min-w-200 h-20 fixed top-0 left-0 right-0  spacebetween bg-black/40 inset-x-0 z-60 px-10 ">
            <div class="flex w-full  justify-between text-light-gray items-center">
                <a href="/" class="flex items-center space-x-3 rtl:space-x-reverse ">
                    <img class="h-7 rounded-full bg-white/40" src={soundWave} alt="audio wave"/>
                    <span class="self-center text-2xl text-heading font-semibold whitespace-nowrap">Top-N</span>
                </a>
                <div class="font-semibold text-xl text-white font-display">
                    <a class="p-4" href='/Team'>Team</a>
                    <a class="p-4">About</a>
                    <a class="p-4 " href="https://github.com/Music-Classification-Project/top-n-music-classification">GitHub</a>
                </div>
                <button 
                type="button" 
                class="text-white bg-forest-green box-border border border-transparent hover:bg-success-strong pointer-click focus:ring-4 focus:success-subtle shadow-xs font-medium leading-5 rounded-full px-4 py-2.5 focus:outline-none"
                >
                Learn More</button>
            </div>
        </nav>
    );
};

export default Navbar