import React from 'react';

const ListCards = ({cards,handle_delete, handle_filter_card}) => {
    const card_list = (
        cards.map(card => {                        
            return (
                <div className="info_div" key={card.card_id} onClick={() => handle_delete(card.card_id)}>
                    <p>Card ID: {card.card_id}</p>
                </div>
            )
        })
    );
    return(
        <div>
            <div className="search">
                <p >Search Card ID:</p>
                <input id="card_input" onChange={() => handle_filter_card()}></input>
            </div>
            <div className="list">
                {card_list}
            </div>
        </div>
    )
}

export default ListCards