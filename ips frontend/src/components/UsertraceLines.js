import React from 'react';

const UsertraceLines = ({line_positions}) => {
    
    const person_list = (
        line_positions.map(line_position => {                        

            var real_start_x = ((line_position.start_x / 5.25) * 38.7 ) + 3;
            var real_start_y = ((line_position.start_y / 3.5) * 24.8) + 1.8;
            var real_end_x = ((line_position.end_x / 5.25) * 38.7 ) + 3;
            var real_end_y = ((line_position.end_y / 3.5) * 24.8) + 1.8;

            var line_width = Math.sqrt( Math.pow(real_end_y - real_start_y, 2) + Math.pow(real_end_x - real_start_x,2));
            var line_height = 1.5

            var rotation_degreeZ = 0;
            var rotation_degreeY = 0;

            if (line_height > line_width){
                var temp = line_height;
                line_height = line_width;
                line_width = temp;
                line_height = line_height + "vw";
                line_width = line_width + "vw";
                rotation_degreeZ = Math.atan( (real_end_x-real_start_x) 
                                        / (real_end_y - real_start_x) );
                 
            }
            else{
                line_height = line_height + "vw";
                line_width = line_width + "vw";
                rotation_degreeZ = Math.atan( (real_end_y-real_start_y) 
                                        / (real_end_x - real_start_x) );    
            }
            rotation_degreeZ = rotation_degreeZ * (180/Math.PI);
            
            if ( real_end_y > real_start_y && real_end_x > real_start_x){
                real_start_x = real_start_x + 0.5;
                rotation_degreeZ = rotation_degreeZ - 360;
            }
            else if( real_end_y > real_start_y && real_end_x < real_start_x){
                rotation_degreeZ =  -rotation_degreeZ;
                rotation_degreeY = 180;
            }
            else if( real_end_y < real_start_y && real_end_x < real_start_x){
                real_start_x = real_start_x + 0.5;
                rotation_degreeZ = -rotation_degreeZ;
                rotation_degreeY = 180;
            }
            

            console.log(rotation_degreeZ);

            var sty = {
                width: line_width,
                height: line_height,
                marginTop: real_start_y + "vw",
                marginLeft: real_start_x + "vw",
                transform: `rotateY(${rotation_degreeY}deg) rotateZ(${rotation_degreeZ}deg)`
            };
            
            return (
                <div key={line_position.date}>
                    <div className="position_line" style = {sty} ></div>
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

export default UsertraceLines