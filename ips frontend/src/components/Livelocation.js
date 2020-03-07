import React, { Component } from 'react';
import Persons from './Persons';
import Now from './Now';
import './Livelocation.css';


class Livelocation extends Component{
    
    state = {
        persons: [
        {card_id: 133, person_name: 'Mehmet', person_surname: 'MUM', x_position: 0, y_position: 0, condition: 'no_show_info'},
        {card_id: 134, person_name: 'Arda', person_surname: 'KOLTUK', x_position: 6, y_position: 10, condition: 'no_show_info'},
        {card_id: 135, person_name: 'Faşo', person_surname: 'ERHAN', x_position: 2, y_position: 11.3, condition: 'no_show_info'},
        {card_id: 136, person_name: 'Hakan', person_surname: 'KALIR', x_position: 20, y_position: 7, condition: 'no_show_info'}
        ]
    }
    
    show_info = (id) => {
        document.getElementById(id).className = 'show_info'; 
    }
    hide_info = (id) => {
        document.getElementById(id).className = 'no_show_info';
    }
    
    add_todo = (person) => {
        person.card_id = Math.random();
        let persons = [...this.state.persons, person];
        this.setState({
        persons: persons
        })
    }
    componentDidMount() {this.interval = setInterval(() => this.loop(),10000)}
    loop = () => {
        let test_per = [];

        for(var i = 1; i < 11; i++){
            var x = Math.random() * 15.7;
            var y = Math.random() * 12;
            var person = {
                card_id: i,
                person_name: x,
                person_surname: y,
                x_position: x,
                y_position: y,
                condition: 'no_show_info',
            }
            let persons = [...test_per, person];
            test_per = persons;
        }
        
        this.setState({
            persons: test_per
        })
    };
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