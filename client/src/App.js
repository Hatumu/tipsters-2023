import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, } from 'react-router-dom';
import './App.css';
import Navbar from './components/Nav/Navbar';
import Selections from './components/Selections/Selections';
import Standings from './components/Standings/Standings';
import Events from './components/Events/Events';
import Rules from './components/Rules/Rules';
  
const App = () => {
    return (
      <Router>
        <div>
          <Navbar />
          <Routes>
            <Route path="/" element={<h1>Tipsters 2023</h1>} />
            <Route path="/selections" element={<Selections />} />
            <Route path="/standings" element={<Standings />} />
            <Route path="/events" element={<Events />} />
            <Route path="/rules" element={<Rules />} />
          </Routes>
        </div>
      </Router>
    );
  };
  
  export default App;