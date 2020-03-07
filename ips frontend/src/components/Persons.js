import React from 'react';
import person_img_0 from './img/person_icon_0.png';
import person_img_1 from './img/person_icon_1.png';
import person_img_2 from './img/person_icon_2.png';
import person_img_3 from './img/person_icon_3.png';
import person_img_4 from './img/person_icon_4.png';
import person_img_5 from './img/person_icon_5.png';

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

            var real_x_pos = ((person.x_position / 15.7) * 36 );
            var real_y_pos = ((person.y_position / 12) * 18);
            var sty = {
                marginTop: (real_y_pos + 1.7) + "em",
                marginLeft: (real_x_pos + 3.8)+ "em",
                backgroundImage: `url(${person_icon})`
            };
            var pos1 = real_y_pos + 2.7;
            var pos2 = real_x_pos + 4.8;
            var info_div = {
                marginTop: pos1 + "em",
                marginLeft: pos2 + "em"
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