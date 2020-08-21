import React from 'react';//useEffect is a hook that allows us to run the http request, actually do a lookup on our server (backend)
import logo from './logo.svg';
import './App.css';

import {TweetsListComp} from './tweets'


function App() {
  console.log("N2")
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <div>
          <TweetsListComp />
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}
console.log("N1")

export default App;
