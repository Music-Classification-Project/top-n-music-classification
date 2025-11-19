import React from "react";
import soundWave from "../assets/audio-wave.svg"

const Navbar = () => {
    /*
    Navbar to be displayed at the header of every page.
    TODO: auto adjust the the width to window size
    */
   
    return (    
        <nav class="bg-neutral-secondary-soft fixed w-full top-0 start-0 p-3 z-30">
            <div class=" flex flex-wrap w-full items-center justify-between mx-auto p-3">
                <a href="#" class="flex items-center space-x-3 rtl:space-x-reverse">
                    <img class="h-7" src={soundWave} alt="audio wave"/>
                    <span class="self-center text-2xl text-heading font-semibold whitespace-nowrap">Top-N</span>
                </a>
                <div class="font-semibold font-display text-lg">
                    <a class="p-4">Team</a>
                    <a class="p-4">About</a>
                    <a class="p-4">Contact</a>
                </div>
                <button 
                type="button" 
                class="text-white text-base bg-darkestgreen box-border border border-transparent hover:bg-success-strong focus:ring-4 focus:success-subtle shadow-xs font-medium leading-5 rounded-full px-4 py-2.5 focus:outline-none">
                Learn More</button>
            </div>
        </nav>
    );
};

export default Navbar