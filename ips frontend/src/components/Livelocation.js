import React, { Component } from 'react';
import axios from 'axios';
import Persons from './Persons';
import Now from './Now';
import './Livelocation.css';


class Livelocation extends Component{

    state = {
        persons: []
    }
    
    show_info = (id) => {
        document.getElementById(id).className = 'show_info'; 
    }
    hide_info = (id) => {
        document.getElementById(id).className = 'no_show_info';
    }
    
    get_locations = () =>{
        axios.get(`https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/position/live`)
                .then(res => {
                const data = res.data;
                var keys = Object.keys(data);
                var values = Object.values(data);
                let temp_persons = [];
                
                for (var i = 0; i < keys.length; i++){
                    var person = {
                        person_id: keys[i],
                        card_id: values[i].cardId,
                        person_name: values[i].firstName,
                        person_surname: values[i].lastName,
                        x_position: values[i].x,
                        y_position: values[i].y,
                        condition: 'no_show_info'
                    }
                    let persons = [...temp_persons, person];
                    temp_persons = persons;
                }

                this.setState({
                    persons: temp_persons
                })
                
            })
    }
    componentDidMount() {
        this.get_locations();
        this.interval_get_pos = setInterval(this.get_locations, 3000);
    }
    componentWillUnmount(){
        clearInterval(this.interval_get_pos);
    }
    
    
    render(){
        return(
            <div>
                <h1 className="title">Real time locations</h1>
                <Now></Now>
                <div id="floor_plan">
                    <Persons persons = {this.state.persons} show_info={this.show_info} hide_info={this.hide_info}></Persons>
                </div>
            </div>
        )
    }
}

export default Livelocation