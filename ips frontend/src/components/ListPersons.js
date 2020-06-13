import React from 'react';


// component for listing persons
const ListPersons = ({persons, handle_show, handle_filter_person}) => {
    const person_list = (
        persons.map(person => {                        
            return (
                <div className="info_div" key={person.person_id} 
                onClick={() => handle_show(person.person_id, person.first_name, person.last_name, person.card_id)}>
                    <p>{person.person_id}</p>
                    <p>{person.first_name} {person.last_name}</p>
                    <p>{person.card_id}</p>
                </div>
            )
        })
    );
    return(
        <div>
            <div className="search">
                <p >Search Name or ID:</p>
                <input id="person_input" onChange={() => handle_filter_person()}></input>
            </div>
            <div className="list">
                <div className="info_div_title">
                    <p>Person ID</p>
                    <p>Name</p>
                    <p>Card ID</p>
                </div>
                {person_list}
            </div>
        </div>
    )
}

export default ListPersons