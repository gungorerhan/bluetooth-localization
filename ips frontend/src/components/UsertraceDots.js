import React from 'react';

const UsertraceDots = ({positions, show_info, hide_info}) => {
    const person_list = (
        positions.map(position => {                        

            var real_x_pos = ((position.x_position / 5.25) * 38.7 );
            var real_y_pos = ((position.y_position / 3.5) * 24.8);
            var sty = {
                marginTop: (real_y_pos + 1.8) + "vw",
                marginLeft: (real_x_pos + 3)+ "vw",
            };
            var pos1 = real_y_pos + 2.5;
            var pos2 = real_x_pos + 3.6;
            var info_div = {
                marginTop: pos1 + "vw",
                marginLeft: pos2 + "vw"
            };
            
            return (
                <div key={position.date}>
                    <div className="position_location" style = {sty} 
                        onMouseEnter={() => {show_info(position.date)}}
                        onMouseLeave={() => {hide_info(position.date)}}></div>
                    <div id={position.date} className={position.condition} style = {info_div}>
                        <p>Date: {position.date}</p>
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

export default UsertraceDots