import React from "react";

export default function TeamPage(){

    const memberData = [
        { id: 1, name: 'Jaclyn Rutter', image: 'frontend-vite/public/andy.png', github: 'https://github.com/jlr295'},
        { id: 2, name: 'Avni Gharpurey', image: 'frontend-vite/public/pam.png', github: 'https://github.com/avni-g'}, 
        { id: 3, name: 'Camden Warncke', image: 'frontend-vite/public/dwightSchrute.png', github: 'https://github.com/cjwarncke'},
        { id: 4, name: 'Jonas Field-Patton', image: 'frontend-vite/public/michaelScott.png', github: 'https://github.com/TheCheerfulCoder'},
        { id: 5, name: 'Cameron Lodge', image: 'frontend-vite/public/jimHalpert.png', github:'https://github.com/cam5674'}
    ];


    return(
        <div class='flex items-center justify-center w-90/100 '>
            <div class='flex flex-col justify-evenly w-full font-[DM Sans] m-20 h-400 '>
            { memberData.map(item => (
                <div key={item.id} class='flex flex-row justify-evenly m-3 p-3  w-full border-1 rounded-lg border-dashed'>
                    <img class='  h-70 w-70 object-cover' src={item.image} />
                    <div class='flex flex-col items-center font-[DM Sans] '> 
                        <h1 class='font-bold text-4xl'>{item.name}</h1>
                        <p ><strong>Github: </strong>{item.github} </p>
                </div>
                </div> 
                
                ))}
            </div>
            
            
        </div>
    )
}

