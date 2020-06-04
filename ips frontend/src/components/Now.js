import React, {Component} from 'react';

class Now extends Component{
    state = {
        current_date: ""
    }
    append_zero = (number) => {
        if (number < 10){
            number = '0' + number;
        }
        return number;
    }
    convert_day = (day) => {
        var the_day = '';
        if( day === 1){
            the_day = 'Monday';
        } else if( day === 2){
            the_day = 'Tuesday';
        } else if( day === 3){
            the_day = 'Wednesday';
        } else if( day === 4){
            the_day = 'Thursday';
        } else if( day === 5){
            the_day = 'Friday';
        } else if( day === 6){
            the_day = 'Saturday';
        } else {
            the_day = 'Sunday';
        }
    
        return the_day;
    }
    update_date = () => {
        var today = new Date();
        var date = this.append_zero(today.getDate()) + "-" + this.append_zero(today.getMonth() + 1) + "-" + today.getFullYear();
        var day = this.convert_day(today.getDay());
        var time = this.append_zero(today.getHours()) + ":" + this.append_zero(today.getMinutes()) + ":" + this.append_zero(today.getSeconds());
        var dateTime = date+' ' + day + ' ' +time;
        try{
            this.setState({
                current_date: dateTime
            });
        }
        catch(error){
            console.error(error);
        }
    }
    componentDidMount() {this.interval = setInterval(() => this.update_date(),1)}
    componentWillUnmount() {clearInterval(this.interval)}
    render(){
        return(
        <p>{this.state.current_date}</p>
        );
    }
}

export default Now