import React, { Component } from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter, Route } from 'react-router-dom';
import Livelocation from './components/Livelocation';
import Heatmap from './components/Heatmap';
import Usertrace from './components/Usertrace';
import Personcard from './components/Personcard';
import './App.css';

class App extends Component {
  render(){
    return (
      <BrowserRouter>
        <div >
          <Navbar></Navbar>
          <Route exact path="/" component = {Livelocation}></Route>
          <Route path="/heatmap" component = {Heatmap}></Route>
          <Route path="/usertrace" component = {Usertrace}></Route>
          <Route path="/personcard" component = {Personcard}></Route>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;