import React from 'react';
import { Link } from 'react-router';

export default class Nav extends React.Component {

  render() {
    let profileMenu;
    if (false) { // TODO: check user details here!
      profileMenu = (
        <ul className='nav navbar-nav navbar-right'>
          <li className='dropdown'>
            <a href className='dropdown-toggle' data-toggle='dropdown' role='button' aria-expanded='false'>TODO:USERNAME<span className='caret'></span></a>
            <ul className='dropdown-menu' role='menu'>
              <li><a href='profile'>Profile</a></li>
              <li><a href='logout'>Log out</a></li>
            </ul>
          </li>
          <li><a href='login'>Log in</a></li>
        </ul>
      );
    } else {
      profileMenu = (
        <ul className='nav navbar-nav navbar-right'>
          <li><a href='login'>Log in</a></li>
        </ul>
      );
    }

    return (
      <nav className='navbar navbar-inverse navbar-fixed-top' role='navigation'>
        <div className='container'>
          <div className='navbar-header'>
            <button type='button' className='navbar-toggle collapsed' data-toggle='collapse' data-target='#navbar' aria-expanded='false' aria-controls='navbar'>
              <span className='sr-only'>Toggle navigation</span>
              <span className='icon-bar'></span>
              <span className='icon-bar'></span>
              <span className='icon-bar'></span>
            </button>
            <Link className='navbar-brand' to='index'>CYB internsystem</Link>
          </div>
          <div id='navbar' className='collapse navbar-collapse'>
            <ul className='nav navbar-nav'>
              <li className='dropdown'>
                <a href className='dropdown-toggle' data-toggle='dropdown' role='button' aria-expanded='false'>Varer
                  <span className='caret'></span></a>
                <ul className='dropdown-menu' role='menu'>
                  <li><a href='varer'>Oversikt</a></li>
                  <li className='divider'></li>
                  <li className='dropdown-header'>Moduler</li>
                  <li><a href='varer/råvarer'>Råvarer</a></li>
                  <li><a href='varer/salgsvarer'>Salgsvarer</a></li>
                  <li><a href='varer/kontoer'>Kontoliste</a></li>
                  <li><a href='varer/leverandører'>Leverandørliste</a></li>
                  <li><a href='varer/salgskalkyler'>Salgskalkyler</a></li>
                  <li><a href='varer/varetellinger'>Varetellinger</a></li>
                </ul>
              </li>
              <li className='dropdown'>
                <a href className='dropdown-toggle' data-toggle='dropdown' role='button' aria-expanded='false'>Z <span
                  className='caret'></span></a>
                <ul className='dropdown-menu' role='menu'>
                  <li><a href='z'>Oversikt</a></li>
                  <li className='divider'></li>
                  <li className='dropdown-header'>Moduler</li>
                  <li><a href='z/stats'>Statistikk</a></li>
                </ul>
              </li>
              <li className='dropdown'>
                <a href className='dropdown-toggle' data-toggle='dropdown' role='button' aria-expanded='false'>Calendar
                  <span className='caret'></span></a>
                <ul className='dropdown-menu' role='menu'>
                  <li><Link to='cal/list'>Oversikt</Link></li>
                </ul>
              </li>
            </ul>
            {profileMenu}
          </div>
        </div>
      </nav>
    )
  }
}