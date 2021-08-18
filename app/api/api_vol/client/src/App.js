import React, { Component } from 'react';
import logo from '../public/circle-logo-alt.png';
import './App.css';
import socketIOClient from "socket.io-client";
import ReactJson from 'react-json-view'


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



class App extends Component {

  constructor(){
    super();
    this.state={ clicks: 0, data: null}
    socket.on('floating info response', val => {
      console.log( val.map((el) => el.vtype) )
      this.setState({data: val.map((el) => el) });
    });
  }


  startStream = () => {
    socket.emit('floating info event', this.state.clicks);
  }

  handleValChange(e) {
    console.log(e)
  }

  IncrementItem = () => {
    new Promise((resolve, reject) => {
        this.setState({ clicks: this.state.clicks + 1 });
        resolve();
    })
    .then(() => {
        socket.emit('floating info event', this.state.clicks);
    })
  }
  DecreaseItem = () => {
    new Promise((resolve, reject) => {
        this.setState({ clicks: this.state.clicks - 1 });
        resolve();
    })
    .then(() => {
        socket.emit('floating info event', this.state.clicks);
    })
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2 className="header-text">Streaming Simulator</h2>
          <button onClick={this.startStream}>
            Start Stream
          </button>
          <div className="buttons-lower">
            <button onClick={this.DecreaseItem}>Click to decrease by 1</button>
            <button onClick={this.IncrementItem}>Click to increment by 1</button>
          </div>
        </div>
        <p> {this.state.clicks} </p>
       {/* <div><pre>{JSON.stringify(this.state.data, null, 2) }</pre></div> */}
        

        <div>
          <table className='table-data'>
            <thead>
                <tr>
                  <td>timestamp</td>
                  <td>type</td>
                  <td>longitude</td>
                  <td>latitude</td>
                </tr>
            </thead>
        <tbody>
          {
            this.state.data && 
            Object.keys(this.state.data).map( (element) => {
              console.log(this.state.data[element])
              return (
                <tr key={element}>
                  <td>{this.state.data[element].vts}</td>
                  <td>{this.state.data[element].vtype}</td>
                  <td>{this.state.data[element].vlon}</td>
                  <td>{this.state.data[element].vlat}</td>
                </tr>
              )
            })
          }
        </tbody>
        </table>
        </div>

      </div>
    );
  }
}

export default App;
