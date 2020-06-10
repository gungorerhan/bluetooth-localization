import React from 'react';
import person_img_0 from './img/person_icon_0.png';
import person_img_1 from './img/person_icon_1.png';
import person_img_2 from './img/person_icon_2.png';
import person_img_3 from './img/person_icon_3.png';
import person_img_4 from './img/person_icon_4.png';
import person_img_5 from './img/person_icon_5.png';


// position a person on the map
const Persons = ({persons, show_info, hide_info}) => {
    const person_list = (
        persons.map(person => {                        
            var url_img = persons.indexOf(person) % 6;
            
            var person_icon;
            if(url_img === 0)
                person_icon = person_img_0;
            else if(url_img === 1)
                person_icon = person_img_1;
            else if(url_img === 2)
                person_icon = person_img_2;
            else if(url_img === 3)
                person_icon = person_img_3;
            else if(url_img === 4)
                person_icon = person_img_4;
            else
                person_icon = person_img_5;

            var real_x_pos = ((person.x_position / 5.25) * 38.7 );
            var real_y_pos = ((person.y_position / 3.5) * 51);
            var sty = {
                marginTop: (real_y_pos + 1.7) + "vh",
                marginLeft: (real_x_pos + 2.5)+ "vw",
                backgroundImage: `url(${person_icon})`
            };
            var pos1 = real_y_pos + 3.2;
            var pos2 = real_x_pos + 4;
            var info_div = {
                marginTop: pos1 + "vh",
                marginLeft: pos2 + "vw"
            };
            
            return (
                <div key={person.card_id}>
                    <div className="person_location" style = {sty} 
                        onMouseEnter={() => {show_info(person.card_id)}}
                        onMouseLeave={() => {hide_info(person.card_id)}}></div>
                    <div id={person.card_id} className={person.condition} style = {info_div}>
                        <p>Card id: {person.card_id}</p>
                        <p>Name: {person.person_name}</p>
                        <p>Surname: {person.person_surname}</p>
                        <p>X position: {person.x_position}</p>
                        <p>Y position: {person.y_position}</p>
                    </div>
                </div>
            )
        })
    );
    return(
        <div>
            {person_list}
        </div>
    )
}

export default Persons