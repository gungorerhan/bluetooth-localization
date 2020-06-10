import React, {Component} from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom'


// Navigation bar
class Navbar extends Component {
    handle_click = (e) => {
        document.title = e.target.innerHTML;
        document.getElementsByClassName("active")[0].className = "passive";
        document.getElementById(e.target.id).className = "active";
    }
    
    
    render(){
        return(
            <nav id="main_navigation">  
                
                <ul>
                    <li><Link id="live_locations" className="active" to="/" onClick={this.handle_click}>Live Locations</Link></li>
                    <li><Link id="heatmap" className="passive"  to="/heatmap" onClick={this.handle_click}>Heatmap</Link></li>
                    <li><Link id="usertraces" className="passive" to="/usertrace" onClick={this.handle_click}>User Traces</Link></li>
                    <li><Link id="person_card" className="passive" to="/personcard" onClick={this.handle_click}>Person Card</Link></li>
                </ul>
            
            </nav>
        );
    }
    
}

export default Navbar