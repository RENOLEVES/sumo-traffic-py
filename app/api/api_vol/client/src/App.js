import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import socketIOClient from "socket.io-client";

var socket;
socket = socketIOClient("localhost:8000/");

let k=0;
setInterval(() => {
  socket.emit("my event", k);
  k+=1;
}, 2000);

socket.on('connection', (ss) => {
  console.log('a user connected');
});

socket.on('my response', (ss) => {
  console.log(ss);
});

socket.on('floating info response', (ss) => {
  console.log(ss);
});

function startStream() {
  socket.emit('floating info event', 999);
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
          <button onClick={startStream}>
            Start Stream
          </button>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default App;
