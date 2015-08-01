import React from 'react';

export default class Index extends React.Component {

  render() {
    return (
      <div>
        <h1>CYB internsystem</h1>
          <p>For informasjon om dette systemet, se prosjektet på <a href="https://github.com/cybrairai/internsystem">https://github.com/cybrairai/internsystem</a>.</p>
          <ul>
            <li><a href="varer">Varesystem</a></li>
            <li><a href="z">Z-rapporter</a></li>
            <li><a href="cal">Cal</a></li>
          </ul>
      </div>
    );
  }
}