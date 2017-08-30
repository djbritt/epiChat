import {
    Socket
}
from './Socket';
import * as React from 'react';

export class UserCount extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'num': 0,
        };
    }
    componentDidMount() {
        Socket.on('userCount', (num) => {
            // console.log(num['num'])
            this.setState({
                "num": num['num'],
            });
        });
    }
    render() {
        if (this.state.num === 0) {
            var num = "0 Users Connected"
        } else {
            var num = this.state.num + " User(s) connected"
        }
        return (
            <div id="userCount">
                {num}
            </div>
        );
    }
}
