import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li><NavLink to="/" activeClassName="active">Home</NavLink></li>
        <li><NavLink to="/selections" activeClassName="active">Selections</NavLink></li>
        <li><NavLink to="/standings" activeClassName="active">Standings</NavLink></li>
        <li><NavLink to="/events" activeClassName="active">Events</NavLink></li>
        <li><NavLink to="/rules" activeClassName="active">Rules</NavLink></li>
      </ul>
    </nav>
  );
};

export default Navbar;
