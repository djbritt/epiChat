import {
    Socket
}
from './Socket';
import * as React from 'react';

export class Input extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            value: event.target.value
        });
    }

    handleSubmit(event) {
        Socket.emit('message', {
            data: this.state.value
        });
        // alert('A name was submitted: ' + this.state.value);
        $("#textarea").val('')
        event.preventDefault();
    }

    render() {
        return (
            <div id="inputArea">
              <form id="messageForm" onSubmit={this.handleSubmit}>
                <label>
                  <input placeholder="Message..." id="textarea" type="text" onChange={this.handleChange} />
                </label>
                <input type="submit" id="button" />
                <div style={ {float:"left", clear: "both"} }
                ref={(el) => { this.messagesEnd = el; }}></div>
              </form>
            </div>
        );
    }
}
