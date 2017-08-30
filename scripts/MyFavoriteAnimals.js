import * as React from 'react';

export class Fav extends React.Component {
    render() {
        var animals = (
            <ul>
                <li>Tiger</li>
                <li>Whale</li>
                <li>Dragon</li>
            </ul>
        );

        return <div><h1>{animals}</h1></div>;
    }
}
