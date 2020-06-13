import React, { Component } from 'react';
import axios from 'axios';
import './Personcard.css';
import ListPersons from './ListPersons';
import ListCards from './ListCards';
import { confirmAlert } from 'react-confirm-alert'; // Import
import 'react-confirm-alert/src/react-confirm-alert.css'; // Import css


class Personcard extends Component{
    
    // boolean value for edit_texts  editable or not
    state = {
        persons: [],
        cards: [],
        filtered_persons:[],
        filtered_cards:[],
        items: [],
        boolean: false,
        the_card_id: ""
    }
    
    // Show add person or add card page
    handle_click_1 = (e) =>{
        this.setState({boolean: false})
        document.getElementById("add_person_personid").value = ""; 
        document.getElementById("add_person_cardid").value = "";  
        document.getElementById("add_person_firstname").value = ""; 
        document.getElementById("add_person_lastname").value = "";
        document.getElementById("add_card_cardid").value = "";
        document.getElementById("info_message").innerHTML = "";
        document.getElementsByClassName("op_active")[0].className = "op_passive";
        if (e.target.innerHTML === "Add Person" || e.target.innerHTML === "Update Person"){
            document.getElementById("operation_title").innerHTML = e.target.innerHTML;
            document.getElementById("add_person").className = "small_div op_active";
            document.getElementById("add_person_butt").className = "operation_button";
            document.getElementById("update_person_butt").className = "hide_button";
            document.getElementById("delete_person_butt").className = "hide_button";
        }
        else if (e.target.innerHTML === "Add Card" || e.target.innerHTML === "Update Card"){
            document.getElementById("operation_title").innerHTML = e.target.innerHTML;
            document.getElementById("add_card").className = "small_div op_active";
        }
    }
    
    // Show   show person or show card page
    handle_click_2 = (e) =>{
        document.getElementById("info_message").innerHTML = "";
        document.getElementsByClassName("op_active")[0].className = "op_passive";
        if (e.target.innerHTML === "Show Persons"){
            document.getElementById("operation_title").innerHTML = e.target.innerHTML;
            document.getElementById("show_persons").className = "list_div op_active";
            document.getElementsByClassName("")

            // get persons from server in order to show them
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
        else if (e.target.innerHTML === "Show Cards"){
            document.getElementById("operation_title").innerHTML = e.target.innerHTML;
            document.getElementById("delete_card").className = "list_div op_active";

            // get cards from server in order to show them
            axios.get(`https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/card`)
                .then(res => {
                const data = res.data;
                var keys = Object.keys(data);
                let temp_cards = [];

                for (var i = 0; i < keys.length; i++){
                    var card = {
                        card_id: keys[i]
                    }
                    let cards = [...temp_cards, card];
                    temp_cards = cards;
                }

                this.setState({
                    cards: temp_cards
                })         
                this.handle_filter_card();   
            })
        }
    }

    

    handle_show = (id, first_name, last_name, card_id) =>{
        document.getElementById("info_message").innerHTML = "";
        document.getElementsByClassName("op_active")[0].className = "op_passive";
        document.getElementById("operation_title").innerHTML = "show person";
        document.getElementById("add_person").className = "small_div op_active";
        document.getElementById("add_person_butt").className = "hide_button";
        document.getElementById("update_person_butt").className = "operation_button";
        document.getElementById("delete_person_butt").className = "operation_button";

        this.setState({boolean: true})

        document.getElementById("add_person_personid").value = id;
        document.getElementById("add_person_cardid").value = card_id;
        document.getElementById("add_person_firstname").value = first_name;
        document.getElementById("add_person_lastname").value = last_name;

        
    }

    // Add person to server
    handle_add_person(){
        if( document.getElementById("add_person_personid").value === "" || 
            document.getElementById("add_person_cardid").value === "" ||  
            document.getElementById("add_person_firstname").value === "" || 
            document.getElementById("add_person_lastname").value === ""){
            }
        else{
            // create person variable
            var params = {
                personId: document.getElementById("add_person_personid").value,
                firstName: document.getElementById("add_person_firstname").value,
                lastName: document.getElementById("add_person_lastname").value,
                cardId: document.getElementById("add_person_cardid").value
            }

            // insert person to server
            axios.post('https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/person', params).then(res => {
                if(res.status === 200){
                    document.getElementById("info_message").innerHTML = "Person is added succesfully!";
                    document.getElementById("add_person_personid").value = ""; 
                    document.getElementById("add_person_cardid").value = "";  
                    document.getElementById("add_person_firstname").value = ""; 
                    document.getElementById("add_person_lastname").value = "";
                }
                else{
                    document.getElementById("info_message").innerHTML = "Person is not added!";
                }
            });

            

        }
        
    }


    // update person information
    handle_update_person(){
        if( document.getElementById("add_person_personid").value === "" || 
            document.getElementById("add_person_cardid").value === "" ||  
            document.getElementById("add_person_firstname").value === "" || 
            document.getElementById("add_person_lastname").value === ""){
                console.log("errrorr");
            }
        else{
            var params = {
                personId: document.getElementById("add_person_personid").value,
                firstName: document.getElementById("add_person_firstname").value,
                lastName: document.getElementById("add_person_lastname").value,
                cardId: document.getElementById("add_person_cardid").value
            }

            // update person information to server
            axios.put('https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/person', params).then(res => {
                if(res.status === 200){
                    document.getElementById("info_message").innerHTML = "Person is updated succesfully!";
                }
                else{
                    document.getElementById("info_message").innerHTML = "Person is not updated!";
                }
            });
        }
        
    }

    // delete person by his id
    handle_delete_person = () =>{
        var person_id = document.getElementById("add_person_personid").value;
        confirmAlert({
            title: 'Delete the person',
            message: "Person ID: " + person_id,
            buttons: [
              {
                label: 'Yes',
                onClick: () => {
                    var url = "https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/person?personId=\"" + person_id + "\"";
                    axios.delete(url).then(res => {
                        if(res.status === 200){
                            document.getElementById("info_message").innerHTML = "Person is deleted succesfully!";
                            document.getElementById("add_person_personid").value = ""; 
                            document.getElementById("add_person_cardid").value = "";  
                            document.getElementById("add_person_firstname").value = ""; 
                            document.getElementById("add_person_lastname").value = "";
        
                        }
                        else{
                            document.getElementById("info_message").innerHTML = "Person is not deleted!";
                        }
                    });
                    
                }
              },
              {
                label: 'No',
                // No action
              }
            ]
          });
    }

    // add card to server
    handle_add_card = () =>{
        if( document.getElementById("add_card_cardid").value === "" ){
                console.log("errrorr");
            }
        else{
            var params = {
                cardId: document.getElementById("add_card_cardid").value
            }
            axios.post('https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/card', params)
            .then(res => {
                if(res.status === 200){
                    document.getElementById("info_message").innerHTML = "Card is added succesfully!";
                    document.getElementById("add_card_cardid").value = "";
                }
                else{
                    document.getElementById("info_message").innerHTML = "Card is not added!";
                }
            });
        }
    }

    // delete card from server by its card id
    handle_delete_card = (card_id) => {
        confirmAlert({
            title: 'Delete the card',
            message: "Card ID: " + card_id,
            buttons: [
              {
                label: 'Yes',
                onClick: () => {
                    var url = "https://t7ftvwr8bi.execute-api.eu-central-1.amazonaws.com/cors/card?cardId=\"" + card_id + "\"";
                    axios.delete(url   
                    )
                    .then(res => {
                        if(res.status === 200){
                            document.getElementById("info_message").innerHTML = "Card is deleted succesfully!";
                            document.getElementById("add_card_cardid").value = "";

                            this.setState({
                                cards: this.state.cards.filter(function(card){
                                    return card.card_id != card_id
                                })
                            })
                            this.handle_filter_card();
                        }
                        else{
                            document.getElementById("info_message").innerHTML = "Card is not deleted!";
                        }
                    });
        
                }
              },
              {
                label: 'No',
                // No action
              }
            ]
          });
    }


    // search a card by its id
    handle_filter_card = () =>{
        var input_value = document.getElementById("card_input").value;
        if(input_value === ""){
            this.setState({filtered_cards: this.state.cards});
        }
        else{
            this.setState({
                filtered_cards: this.state.cards.filter(function(card){
                    return card.card_id == input_value
                })
            })
        }
    }

    // search person by name or by person id
    handle_filter_person = () => {
        var input_value = document.getElementById("person_input").value;
        console.log(input_value);
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
        console.log(this.state.filtered_persons);

    }

    render(){
        return(
            <div id="person_card_container">
                <div id="personcard_menu">
                    <p className="side_title">PERSON</p>
                    <p className="side_link" onClick={this.handle_click_1}>Add Person</p>
                    <p className="side_link" onClick={this.handle_click_2}>Show Persons</p>
                    <p className="side_title">CARD</p>
                    <p className="side_link" onClick={this.handle_click_1}>Add Card</p>
                    <p className="side_link" onClick={this.handle_click_2}>Show Cards</p>
                </div>
                <div id="operation_div">
                    <h1 id="operation_title">Add Person</h1>
                    <p id="info_message"></p>
                    <div id="add_person" className="small_div op_active">
                        <div>
                            <div>
                                <p>Person ID:</p>
                                <input id="add_person_personid" maxLength="20" readOnly={this.state.boolean}></input>
                            </div>
                            <div>
                                <p>Card ID:</p>
                                <input id="add_person_cardid" maxLength="10" ></input>
                            </div>
                            <div>
                                <p>First Name:</p>
                                <input id="add_person_firstname" maxLength="50" ></input>
                            </div>
                            <div>
                                <p>Last Name:</p>
                                <input id="add_person_lastname" maxLength="50" ></input>
                            </div>
                        </div>
                        <input id="add_person_butt" className="operation_button" type="submit" 
                                value="Add Person" onClick={this.handle_add_person}></input>
                        <input id="delete_person_butt" className="hide_button" type="submit" 
                                value="Delete" onClick={this.handle_delete_person}></input>
                        <input id="update_person_butt" className="hide_button" type="submit" 
                                value="Update" onClick={this.handle_update_person}></input>
                    </div>
                    <div id="add_card" className="small_div op_passive">
                        <div>
                            <div>
                                <p>Card ID:</p>
                                <input id="add_card_cardid" maxLength="10" ></input>
                            </div>
                        </div>
                        <input id="add_card_butt" className="operation_button" type="submit" 
                                value="Add Card" onClick={this.handle_add_card}></input>
                    </div>
                    <div id="show_persons" className="list_div op_passive">
                        <ListPersons persons={this.state.filtered_persons} handle_show={this.handle_show}
                                        handle_filter_person={this.handle_filter_person}
                                        div_1={document.getElementById("personcard_menu")}></ListPersons>
                    </div>
                    <div id="delete_card" className="list_div op_passive">
                        <ListCards cards={this.state.filtered_cards} handle_delete={this.handle_delete_card}
                                        handle_filter_card={this.handle_filter_card}></ListCards>
                    </div>
                </div>
            </div>
        )
    }
}

export default Personcard