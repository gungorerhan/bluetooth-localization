import React, { Component } from 'react';
import axios from 'axios';
import './Heatmap.css';



class Heatmap extends Component {
    get_locations = () =>{
        if(document.getElementById("begin_date").value === ''
            || document.getElementById("begin_hour").value === ''
            || document.getElementById("end_date").value === ''
            || document.getElementById("end_hour").value === ''){
        }
        else{
            var begin_date = document.getElementById("begin_date").value + " " 
            + document.getElementById("begin_hour").value + ":00";

            var end_date = document.getElementById("end_date").value + " " 
            + document.getElementById("end_hour").value + ":00";

            if(end_date > begin_date){
                document.getElementById("begin_p_tag").innerHTML = "Begin date: " + begin_date;
                document.getElementById("end_p_tag").innerHTML = "End date: " + end_date;
                var params = {
                    startTime: begin_date,
                    endTime: end_date
                }
                axios.get(`https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/position/heatmap`, params)
                    .then(res => {
                    const data = res.data;
                    console.log(data);
                    
                });
            }
        }
    }
    render(){
        return(
            <div id="heatmap_container">
                <div id="heatmap_input_div">
                    <h2 id="heatmap_title">select time interval</h2>
                    <h3 >begin time</h3>
                    <div>
                        <p>date:</p>
                        <input id="begin_date" type="date"></input>
                    </div>
                    <div>
                        <p>hour:</p>
                        <input id="begin_hour" type="time"></input>
                    </div>
                    <h3 >end time</h3>
                    <div>
                        <p>date:</p>
                        <input id="end_date" type="date"></input>
                    </div>
                    <div>
                        <p>hour:</p>
                        <input id="end_hour" type="time"></input>
                    </div>
                    <input className="heatmap_submit" type="submit" value="Show" onClick={this.get_locations}></input>
                </div>
                <div id="heatmap_show">
                    <h1>Heatmap</h1>
                    <p id="begin_p_tag"></p>
                    <p id="end_p_tag"></p>
                    <div id="heatmap_floor">

                    </div>
                </div>
            </div>
        )
    }
}

export default Heatmap
