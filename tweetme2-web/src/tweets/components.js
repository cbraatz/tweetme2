import React from 'react'

export function ActionBtnComp(props){
    const {tweet, action} = props
    const className= props.className ? props.className : 'btn btn-primary btn-sm'
    return action.type === 'like' ? <button className={className}>{tweet.likes} Likes</button> : null
}
export function TweetComp(props){
    const {tweet}=props
    const className= props.className ? props.className : 'col-10 mx-auto col-md-6'
    //const action="like" se puede hacer asi y en action 1 solo parentesis o hacer todo junto con e parentesis como esta mas abajo.
    return <div className={className}>
              <p>{tweet.id} - {tweet.content}</p>
              <div className='btn btn-group'>
                <ActionBtnComp tweet={tweet} action={{type:"like"}}/>
                <ActionBtnComp tweet={tweet} action={{type:"unlike"}}/>
              </div>
           </div>
}