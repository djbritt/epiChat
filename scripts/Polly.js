import * as React from 'react';
import {
    Socket
}
from './Socket';
export class PollyInput extends React.Component {
    
    render() {
        return (
            <div>
                <button onClick={this.logout} className="loginBtn loginBtn--facebook">
                  Logout from Facebook
                </button>
            </div>
        );
    }
}
