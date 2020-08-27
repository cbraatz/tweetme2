import React, {useEffect, useState} from 'react'
import {loadTweets} from '../lookup'

export function TweetsComponent(props){
  const textAreaRef=React.createRef()
  const [newTweets,setNewTweets]=useState([])
  const handleSubmit= (event) => {
    event.preventDefault()
    const newVal=textAreaRef.current.value
    let tempNewTweets=[...newTweets]//copying newTweets
    //change this to a sever side call
    console.log('bef='+tempNewTweets.length)
    tempNewTweets.unshift({content:newVal , likes:0 , id:12323}) //unshift agrega el elemento al inicio de la lista o array
    console.log('af='+tempNewTweets.length)
    setNewTweets(tempNewTweets)
    textAreaRef.current.value=''
  }
  return <div className={props.className}>
          <div className='col-12 mb-3'>
            <form onSubmit={handleSubmit}>
              <textarea ref={textAreaRef} required={true} className='form-control' name='tweet'></textarea>
              <button type='submit' className='btn btn-primary my-3'>Tweet</button>
            </form>
          </div>
          <TweetsListComp newTweets={newTweets}/>
         </div>
}
export function TweetsListComp(props){
  const [tweetsInit, setTweetsInit] = useState([]);
  const [tweets, setTweets] = useState([])

  useEffect(() =>{ //video 6:13:20
      const final = [...props.newTweets].concat(tweetsInit)//lo que sera la lista nueva
      if(final.length!==tweets.length){//si cambia el estado o sea si se agrega uno nuevo hay que actualizar la lista
        setTweets(final)
      }
    }, [props.newTweets, tweets, tweetsInit]) //entre corchetes van las dependencias




  useEffect(() =>{ //lo mismo que agregar lo de abajo a una funcion aparte con >> const performLookup = () =>{...} o function performLookup(){...} y luego llamar acá a con useEffect(performLookup, [])
      //do my lookup
      console.log("N3")
      const myCallback=(response,status)=>{ //esta funcion puede agregarse afuera del useEffect tambien..
        console.log("N9")
        //console.log(response,status)
        if(status===200){
          setTweetsInit(response)//response should be an array
        }else{
          alert("An error happened. "+response.message+". Status= "+status)
        }
      }
      console.log("N4")
      loadTweets(myCallback)
      console.log("N8")
    }, [tweetsInit]) //entre corchetes paso las dependencies al lookup
    return tweets.map(
      (item, index)=>{
        return <TweetComp tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`}/>
      }
    )
}

export function ActionBtnComp(props){
    const {tweet, action} = props
    const [likes, setLikes]=useState(tweet.likes ? tweet.likes : 0) //para actualizar/refrescar los likes del boton al hacerle click incrementando en 1
    const [userLike, setUserLike]=useState(tweet.userLike === true ? true : false) //FALTA RECIBIR EL VALOR INICIAL para verificar si el usuario logueado fue el que ya le dio like, el valor por defecto o initial state 6:02 se carga en useState() entre los parentesis.
    const className= props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay= action.display ? action.display : 'Action' //en caso de que no tenga action.display ej <ActionBtnComp tweet={tweet} action={{type:"retweet"}}/> entonces va a decir Action en el boton pero sigue siendo del tipo especificado ahi
    
    const handleClick = (event) => {
      event.preventDefault() //para que no redireccione
      if (action.type === 'like'){
        if (userLike === true){//si ya me gusta y le doy click de nuevo
          setLikes(likes - 1)
          setUserLike(false)
        }else{//si aun not le di like y le doy click
          setLikes(likes + 1)
          setUserLike(true)
        }
      }
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay //`${tweet.likes} ${actionDisplay}` tweet.likes OR actionDisplay ...creo
    return <button className={className} onClick={handleClick}>{display}</button>
}
export function TweetComp(props){
    const {tweet}=props
    const className= props.className ? props.className : 'col-10 mx-auto col-md-6'
    //const action="like" se puede hacer asi y en action 1 solo parentesis o hacer todo junto con e parentesis como esta mas abajo.
    return <div className={className}>
              <p>{tweet.id} - {tweet.content}</p>
              <div className='btn btn-group'>
                <ActionBtnComp tweet={tweet} action={{type:"like", display:"Likes"}}/>
                <ActionBtnComp tweet={tweet} action={{type:"unlike", display:"Unlike"}}/>
                <ActionBtnComp tweet={tweet} action={{type:"retweet", display:"Retweet"}}/>
              </div>
           </div>
}