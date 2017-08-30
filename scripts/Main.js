import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { Content } from './Content';
import { Socket } from './Socket';
import { Logins } from './Login';
import { UserCount } from './UserCount.js'

ReactDOM.render(<Content />, document.getElementById('messages'));
ReactDOM.render(<Logins />, document.getElementById('buttons'));
ReactDOM.render(<UserCount />, document.getElementById('userCount'));

Socket.on('connect', function() {
    console.log('Connecting to the server!');
})
// Socket.on('disconnect', function() {
//     console.log('Somebody Disconnected');
// })


// import { Fav } from './MyFavoriteAnimals';

// ReactDOM.render(<Fav />, document.getElementById('animals'));
