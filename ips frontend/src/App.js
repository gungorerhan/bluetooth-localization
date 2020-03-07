import React, { Component } from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter, Route } from 'react-router-dom';
import Home from './components/Home';
import Livelocation from './components/Livelocation';
import Heatmap from './components/Heatmap';
import Usertrace from './components/Usertrace';
import './App.css';

class App extends Component {
  render(){
    return (
      <BrowserRouter>
        <div >
          <Navbar></Navbar>
          <Route exact path="/" component = {Home}></Route>
          <Route path="/livelocation" component = {Livelocation}></Route>
          <Route path="/heatmap" component = {Heatmap}></Route>
          <Route path="/usertrace" component = {Usertrace}></Route>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;