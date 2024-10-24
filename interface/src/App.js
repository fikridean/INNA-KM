// import logo from './logo.svg';
// import './App.css';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Welcome from './components/Welcome';
import Bacdive from './components/Bacdive';
import BacteryPage from './pages/BacteryPage';
import BacteryPage2 from './pages/BacteryPage2';
import SearchPage from './components/SearchPage'

function App() {
  return (
    <div className="App Container">
      <Router>
        <Routes>
          <Route path="/" element={<Home />}>
            <Route index element={<Welcome />} />
            <Route path="/bacdive" element={<Bacdive />} />
            <Route path="/bacdive/:bacteryName" element={<BacteryPage />} />
            <Route path="/bacdive/2/:bacteryName" element={<BacteryPage2 />} />
            <Route path="/search" element={<SearchPage />} />
          </Route>
         
        </Routes>
      </Router>
    </div>
  );
}

export default App;
