import React, {useEffect, useState} from 'react';//useEffect is a hook that allows us to run the http request, actually do a lookup on our server (backend)
import logo from './logo.svg';
import './App.css';

import {TweetComp} from './tweets'

function loadTweets(callback){//from home.html
  console.log("N5")
  const xhr=new XMLHttpRequest()
  const method= 'GET' 
  const url = "http://localhost:8000/api/tweets/" //el que va a retornar el json
  const responseType="json"
  xhr.responseType = responseType
  xhr.open(method,url)//abre la url
  console.log("N6")
  xhr.onload=function(){
      callback(xhr.response, xhr.status)
      console.log("N10")
  }
  xhr.onerror= function(e){
    console.log(e)
    callback({"message":"The request was an error"},400)
  }
  xhr.send() //envia la request
  console.log("N7")
}

function App() {
  console.log("N1")
  const [tweets, setTweets] = useState([/*empty array*/]);
  useEffect(() =>{ //lo mismo que agregar lo de abajo a una funcion aparte con >> const performLookup = () =>{...} o function performLookup(){...} y luego llamar acá a con useEffect(performLookup, [])
      //do my lookup
      console.log("N3")
      const myCallback=(response,status)=>{ //esta funcion puede agregarse afuera del useEffect tambien..
        console.log("N9")
        //console.log(response,status)
        if(status===200){
          setTweets(response)//response should be an array
        }else{
          alert("An error happened. "+response.message+". Status= "+status)
        }
      }
      console.log("N4")
      loadTweets(myCallback)
      console.log("N8")
    }, []) //entre corchetes paso las dependencies al lookup
  console.log("N2")
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <div>
          {tweets.map(
            (item, index)=>{
              return <TweetComp tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`}/>
            }
          )}
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
console.log("N0")

export default App;
