import React, { Component } from 'react';
import './Usertrace.css';
import UsertraceDots from './UsertraceDots';
import axios from 'axios';
import UsertraceLines from './UsertraceLines';



class Usertrace extends Component {
    state = {
        persons: [],
        filtered_persons: [],
        positions: [],
        line_positions:[]
    }
    componentDidUpdate(){
        this.add_persons();
    }
    componentDidMount(){
        this.get_persons();
        this.filter_positions();
        
    }
    

    // filter positions  inside 0.3 m near
    filter_positions = () =>{
        var length = this.state.positions.length;

        for( var i = 0; i < length; i++){
            var x_pos = this.state.positions[i].x_position;
            var y_pos = this.state.positions[i].y_position;
            for (var j = i+1; j<length; j++){
                var distance = Math.pow(x_pos-this.state.positions[j].x_position,2) +
                                Math.pow(y_pos-this.state.positions[j].y_position,2);
                
                distance = Math.sqrt(distance);
                
                if(distance < 0.3){
                    this.state.positions[j].date = "0";
                }
            }
        }

        this.setState({
            positions: this.state.positions.filter(function(position){
                return position.date !== "0";
            })
        })
    }

    // generate lines begin and end positions
    adjust_line_positions(){
        var length = this.state.positions.length - 1;
        
        let temp_line_positions = [];

        for( var i = 0; i < length; i++){
                
            var line_position = {
                start_x: this.state.positions[i].x_position,
                start_y: this.state.positions[i].y_position,
                end_x: this.state.positions[i+1].x_position,
                end_y: this.state.positions[i+1].y_position
            }
            let line_positions = [...temp_line_positions, line_position];
            temp_line_positions = line_positions;
        

            
        } 
        
        this.setState({
            line_positions: temp_line_positions
        });

    }

    // get locations from server
    get_positions = () =>{
        if(document.getElementById("begin_date").value === ''
            || document.getElementById("begin_hour").value === ''
            || document.getElementById("end_date").value === ''
            || document.getElementById("end_hour").value === ''){
        }
        else{
            if( document.getElementById("begin_date").value == document.getElementById("end_date").value){
                var begin_date = document.getElementById("begin_date").value + " " 
                    + document.getElementById("begin_hour").value + ":00";

                var end_date = document.getElementById("end_date").value + " " 
                    + document.getElementById("end_hour").value + ":00";

                if(end_date > begin_date){
                    document.getElementById("begin_p_tag").innerHTML = "Begin date: " + begin_date;
                    document.getElementById("end_p_tag").innerHTML = "End date: " + end_date;
                    

                    var e = document.getElementById("person_select");
                    var id = e.options[e.selectedIndex].value;

                    document.getElementById("person_p_tag").innerHTML = "Person: " + e.options[e.selectedIndex].innerHTML;


                    var url = 'https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/position/person-trace?personId="';
                    url = url + id + '"';
                    url = url + '&startTime="' + begin_date + '"';
                    url = url + '&endTime="' + end_date + '"';

                    axios.get(url)
                        .then(res => {
                            const data = res.data;
                            var keys = Object.keys(data);
                            var values = Object.values(data);
                            let temp_positions = [];
                
                            for (var i = 0; i < keys.length; i++){
                                var position = {
                                    date: keys[i],
                                    x_position: values[i].x,
                                    y_position: values[i].y,
                                    condition: "no_show_info"
                                }
                                let positions = [...temp_positions, position];
                                temp_positions = positions;
                            }
                
                            this.setState({
                                positions: temp_positions
                            })
                            this.filter_positions();
                            this.adjust_line_positions();
                    });
                }
            }
        }
    }

    // get persons from server
    get_persons(){
        axios.get(`https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/person`)
            .then(res => {
            const data = res.data;
            var keys = Object.keys(data);
            var values = Object.values(data);
            let temp_persons = [];

            for (var i = 0; i < keys.length; i++){
                var person = {
                    person_id: keys[i],
                    first_name: values[i].firstName,
                    last_name: values[i].lastName,
                    card_id: values[i].cardId
                }
                let persons = [...temp_persons, person];
                temp_persons = persons;
            }

            this.setState({
                persons: temp_persons
            })
            this.handle_filter_person();
   
        })
    }

    // search person by name or person id
    handle_filter_person = () => {
        var input_value = document.getElementById("search_input").value;
        if( input_value === ""){
            this.setState({filtered_persons: this.state.persons});
        }
        else{
            this.setState({
                filtered_persons: this.state.persons.filter(function(person){
                    var full_name = person.first_name + " " + person.last_name;
                    return person.person_id == input_value 
                                || person.first_name.toLowerCase() == input_value.toLowerCase() 
                                || person.last_name.toLowerCase() == input_value.toLowerCase()
                                || full_name.toLowerCase() == input_value.toLowerCase()
                })
            })
        }
    }


    // add persons to select tag
    add_persons = () =>{
        var person_select = document.getElementById('person_select');
        person_select.innerHTML = "";
        var length = this.state.filtered_persons.length;
        for(let i = 0; i<length; i++){
            let text = this.state.filtered_persons[i].person_id + " - " 
                      +this.state.filtered_persons[i].first_name + " "
                      +this.state.filtered_persons[i].last_name;     
            person_select.options[person_select.options.length] = 
                        new Option(text, this.state.filtered_persons[i].person_id);
        }
    } 

    show_info = (id) => {
        document.getElementById(id).className = 'show_info'; 
    }
    hide_info = (id) => {
        document.getElementById(id).className = 'no_show_info';
    }   
    render(){
        return(
            <div id="usertrace_container">
                <div id="user_trace_menu">
                    <h2>select person</h2>
                    <div>
                        <p>search:</p>
                        <input id="search_input" className="text" onChange={this.handle_filter_person}></input>
                    </div>
                    <div>
                        <p>person:</p>
                        <select id="person_select"></select>                
                        </div>
                    <h2 >begin time</h2>
                    <div>
                        <p>date:</p>
                        <input id="begin_date" type="date"></input>
                    </div>
                    <div>
                        <p>hour:</p>
                        <input id="begin_hour" type="time"></input>
                    </div>
                    <h2 >end time</h2>
                    <div>
                        <p>date:</p>
                        <input id="end_date" type="date"></input>
                    </div>
                    <div>
                        <p>hour:</p>
                        <input id="end_hour" type="time"></input>
                    </div>
                    <input className="usertrace_submit" type="submit" value="Show" onClick={this.get_positions}></input>
                </div >
                <div id="usertrace_show">
                    <h1>User Trace</h1>
                    <p id="person_p_tag"></p>
                    <p id="begin_p_tag"></p>
                    <p id="end_p_tag"></p>
                    <div id="usertrace_floor_plan">
                        <UsertraceDots positions = {this.state.positions} show_info={this.show_info} hide_info={this.hide_info}></UsertraceDots>
                        <UsertraceLines line_positions = {this.state.line_positions}></UsertraceLines>
                    </div>
                </div>
                    
    
            </div>
        )
    }
}

export default Usertrace