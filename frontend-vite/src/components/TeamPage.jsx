import React from "react";
import { useNavigate } from "react-router-dom";

export default function TeamPage(){

    const memberData = [
        { id: 1, name: 'Jaclyn Rutter', image: '../../images/andy.png', github: 'https://github.com/jlr295'},
        { id: 2, name: 'Avni Gharpurey', image: '../../images/phyllis.jpg', github: 'https://github.com/avni-g'}, 
        { id: 3, name: 'Camden Warncke', image: '../../images/dwightSchrute.png', github: 'https://github.com/cjwarncke'},
        { id: 4, name: 'Jonas Field-Patton', image: '../../images/michaelScott.png', github: 'https://github.com/TheCheerfulCoder'},
        { id: 5, name: 'Cameron Lodge', image: '../../images/kevin.jpg', github:'https://github.com/cam5674'}
    ];



    return(
        <div class='flex items-center font-[DM Sans] justify-center h-full w-full bg-[url(../../images/team-bg.jpg)] bg-cover bg-no-repeat '>
            <div class='flex items-center justify-evenly w-full bg-black/80 w-full h-auto p-10 font-[DM Sans] overflow-x-auto '>
            { memberData.map(item => (
                <div key={item.id}  class='flex flex-col justify-center items-center h-full w-full space-y-5 m-5 p-5 bg-dusty-gray/60 shadow rounded-lg'>
                    <img class='rounded-md border p-2' src={item.image} />
                    <div class='flex flex-col items-center p-3 text-center justify-center font-[DM Sans] flex-nowrap'> 
                        <h1 class='font-bold text-4xl'>{item.name}</h1>
                        <p><strong>Github: </strong><a href={item.github}>{item.github}</a></p>
            
                </div>
                </div> 
                
                ))}
            </div>
            
            
        </div>
    )
}

