import React from "react";
import soundWave from "../assets/audio-wave.svg"

/* Navbar Element - to be placed in header of every page. */

const Navbar = () => {
    /*
    Navbar to be displayed at the header of every page.
    */
   
    return ( 
        <nav class="flex flex-nowrap bg-neutral-secondary-soft fixed w-full top-0 start-0 p-3">
            <div class="flex w-full items-center justify-between mx-auto p-3">
                <a href="/" class="flex items-center space-x-3 rtl:space-x-reverse">
                    <img class="h-7" src={soundWave} alt="audio wave"/>
                    <span class="self-center text-xl text-heading font-semibold whitespace-nowrap">Top-N</span>
                </a>
                <div class="font-semibold font-display">
                    <a class="p-4">Team</a>
                    <a class="p-4">About</a>
                    <a class="p-4">Contact</a>
                </div>
                <button 
                type="button" 
                class="text-white bg-darkestgreen box-border border border-transparent hover:bg-success-strong focus:ring-4 focus:success-subtle shadow-xs font-medium leading-5 rounded-full px-4 py-2.5 focus:outline-none">
                Learn More</button>
            </div>
        </nav>
    );
};

export default Navbar