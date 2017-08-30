import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { FBbutton } from './Login';
import { Socket } from './Socket';

ReactDOM.render(<FBbutton />, document.getElementById('buttons'));

Socket.on('connect', function() {
    console.log('Connecting to the server!');
})
// Socket.on('disconnect', function() {
//     console.log('Somebody Disconnected');
// })


// import { Fav } from './MyFavoriteAnimals';

// ReactDOM.render(<Fav />, document.getElementById('animals'));
