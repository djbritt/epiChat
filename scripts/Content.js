import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
    Socket
}
from './Socket';


var messagesArray = [];
var num = 0;


export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'data': '',
            'messages': []
        };
    }
    componentDidMount() {
        
        Socket.on('update', (data) => {
            this.setState(data);
        });
        Socket.emit('pageLoad');
        
        Socket.on('messageSend', (list) => {
            // this.scrollToBottom();
            console.log(list['list'])
            this.setState({
                "messages": list['list'],
            });
            // console.log(this.state.messages)
        });
    }
    render() {
        console.log("messages length is " + this.state.messages.length)
        if (this.state.messages.length > 0) {
            
            for (var i in this.state.messages) {
                // console.log(this.state.messages[i])
                var current = this.state.messages[i].message;
                //CHECK FOR URLS
                if (current.includes("<a")) {
                    var str = current.replace('<a', '');
                    this.state.messages[i].message = <a href={str}>{str}</a>;
                }
                //CHECK FOR IMAGES
                if (current.includes(".jpg") || current.includes(".png") || current.includes(".jpeg") || current.includes(".gif")) {
                    this.state.messages[i].message = <img src={str} />;
                }
            }
            
            var current = this.state.messages
            var messages = current.map(
                (n, index) =>
                <div key={index} id="message">
                    <img style={{height: '50px'}} src={n['pic']} />
                    {n['name']}: {n.message}
                    <hr />
                </div>
        );
    }
    return (
        <div>
            <br />
            {messages}
            <br />
            {Audio}
        </div>
    );
}
}
