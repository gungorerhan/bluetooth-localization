import React, { Component } from 'react';
import './Usertrace.css';
import UsertraceDots from './UsertraceDots';
import axios from 'axios';
import UsertraceLines from './UsertraceLines';



class Usertrace extends Component {
    state = {
        persons: [],
        filtered_persons: [],
        positions: [
            {x_position: 2, y_position:3.5, date: "22-02-2020 18:30:00", condition: "no_show_info"},
            {x_position: 1.2, y_position:3, date: "22-03-2020 18:30:00", condition: "no_show_info"},
            {x_position: 4.1, y_position:1.8, date: "22-04-2020 18:30:00", condition: "no_show_info"}
        ],
        line_positions:[
            {start_x: 2, start_y: 3.5, end_x: 1.2, end_y:3},
            {start_x: 1.2, start_y: 3, end_x: 4.1, end_y:1.8},
        ]
    }
    componentDidUpdate(){
        this.add_persons();
    }
    componentDidMount(){
        //this.get_persons();
        this.interval_get_pos = setInterval(this.randomPositions, 3000);
    }
    randomPositions = () =>{
        var p1 = Math.random() * 5.25;
        var p2 = Math.random() * 3.5;

        var p3 = Math.random() * 5.25;
        var p4 = Math.random() * 3.5;

        var p5 = Math.random() * 5.25;
        var p6 = Math.random() * 3.5;

        this.setState({positions: [
            {x_position: p1, y_position:p2, date: "22-02-2020 18:30:00", condition: "no_show_info"},
            {x_position: p3, y_position:p4, date: "22-03-2020 18:30:00", condition: "no_show_info"},
            {x_position: p5, y_position:p6, date: "22-04-2020 18:30:00", condition: "no_show_info"}
        ]});

        this.setState({line_positions:[
            {start_x: p1, start_y: p2, end_x: p3, end_y:p4},
            {start_x: p3, start_y: p4, end_x: p5, end_y:p6},
        ]});
    }
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
                        <input type="date"></input>
                    </div>
                    <div>
                        <p>hour:</p>
                        <input type="time"></input>
                    </div>
                    <h2 >end time</h2>
                    <div>
                        <p>date:</p>
                        <input type="date"></input>
                    </div>
                    <div>
                        <p>hour:</p>
                        <input type="time"></input>
                    </div>
                    <input className="usertrace_submit" type="submit" value="Show"></input>
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