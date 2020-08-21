

export function loadTweets(callback){//from home.html
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