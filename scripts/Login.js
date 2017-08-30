import * as React from 'react';
import {
    Socket
}
from './Socket';

import {
    Input
}
from './Input';


function FBToken() {
    FB.getLoginStatus((response) => {
        console.log(response)
        if (response.status == 'connected') {
            Socket.emit('fbtoken', {
                'facebook_user_token': response.authResponse,
            });
            console.log("Token sent to server.")
        }
    });
}

function FBLogin() {
    FB.login(function(response) {
        if (response.authResponse) {
            console.log('Welcome!  Fetching your information.... ');
            FB.api('/me', function(response) {
                console.log('Good to see you, ' + response.name + '.');
                FBToken();
            });
        }
        else {
            console.log('User cancelled login or did not fully authorize.');
        }
    });

}

function FBLogout() {
    FB.getLoginStatus((response) => {
        if (response.status == 'connected') {
            FB.logout(function(response) {
                Socket.emit('fblogout');
                console.log("You are now logged out")
            });
        }
    });
}


export class FBLogoutButton extends React.Component {
    logout() {
        FBLogout();
    }

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

export class FBLoginButton extends React.Component {
    login() {
        FBLogin();
    }
    render() {
        return (
            <div>
                <button onClick={this.login} className="loginBtn loginBtn--facebook">
                  Login with Facebook
                </button>
            </div>
        );
    }
}

// function GoogleLogin() {
//     let auth = gapi.auth2.getAuthInstance();
//     let user = auth.currentUser.get();
//     console.log("sending data to server")
//     if (user.isSignedIn()) {
//         Socket.emit('googleToken', {
//             'google_user_token': user.getAuthResponse().id_token
//         });
//     }
// }

export class GLogoutButton extends React.Component {
    logout() {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function() {
            console.log('User signed out.');
            Socket.emit('glogout');
        });
    }
    render() {
        return (
            <div>
            <button onClick={this.logout} className="loginBtn loginBtn--google">
              Logout from Google
            </button>
        </div>
        );
    }
}
export class GLoginButton extends React.Component {
    componentDidMount() {
        console.log("Component mounted")
            // ----------------------------------------------- Non custom glogin button
            // gapi.signin2.render('my-signin2', {
            //     'scope': 'profile email',
            //     'width': 240,
            //     'height': 50,
            //     'longtitle': true,
            //     'theme': 'dark',
            //     'onsuccess': this.onSuccess,
            //     'onfailure': this.onFailure
            // });
            // console.log(element.id);
            // --------------------------------------------------------------
        gapi.load('auth2', function() {
            var d = gapi.auth2.init();
            // client_id: '703008667276-te6tqp98g8ogf25ipf7g26vcb0nelqp0.apps.googleusercontent.com',
            // cookiepolicy: 'single_host_origin',
            // Request scopes in addition to 'profile' and 'email'
            //scope: 'additional_scope'
            // });
            // attachSignin(document.getElementById('customBtn'));
            console.log("auth2 loaded")
                // console.log(d)

            d.attachClickHandler(document.getElementById('my-signin2'), {},
                function(googleUser) {
                    console.log("Signed in: " + googleUser.getBasicProfile().getName());
                    var token = googleUser.Zi.access_token;
                    var gName = googleUser.getBasicProfile().getName();
                    var gImage = googleUser.getBasicProfile().getImageUrl();
                    Socket.emit('googleToken', {
                        'gToken': token,
                        'gImage': gImage,
                        'gName': gName
                    });
                },
                function(error) {
                    alert(JSON.stringify(error, undefined, 2));
                });
        });


    }
    render() {
        return (
            <div>
                <button id="my-signin2" className="loginBtn loginBtn--google">
                Login to Google
                </button>
            </div>
        );
    }
}


// -------------------------------------------------------MAIN COMPONENT

export class Logins extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: '',
            fbloggedin: false,
            gloggedin: false,
        };
    }
    componentDidMount() {
        Socket.on('sendFB', (data) => {
            this.setState({
                fbloggedin: true
            });
        });
        Socket.on('fblogout', (data) => {
            console.log("entered fblogout set state")
            this.setState({
                fbloggedin: false
            });
        });
        Socket.on('glogin', (data) => {
            console.log("entered gLogin set state")
            this.setState({
                gloggedin: true
            });
        });
        Socket.on('glogout', (data) => {
            console.log("entered glogout set state")
            this.setState({
                gloggedin: false
            });
        });
    }
    render() {
        var fbloggedin = this.state.fbloggedin
        var gloggedin = this.state.gloggedin
        let button = null;
        if (fbloggedin === false & gloggedin === true) {
            button = <div id="logout"><GLogoutButton /><Input /></div>
        }
        else if (fbloggedin === true & gloggedin === false) {
            button = <div id="logout"><FBLogoutButton /><Input /></div>
        }
        else {
            button = <div id="login"><h1>Welcome to Daniel's Chatroom</h1><h2>Please Choose a Signin Option:</h2><FBLoginButton /><GLoginButton /></div>
        }

        return (
            <div>
                {button}
            </div>
        );
    }
}
