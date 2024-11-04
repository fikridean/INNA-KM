import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Welcome from './components/Welcome';
import BacteryList from './pages/BacteryList';
import BacteryPage from './pages/BacteryPage';
import SearchPage from './pages/SearchPage'

function App() {
  return (
    <div className="App Container">
      <Router>
        <Routes>
          <Route path="/" element={<Home />}>
            <Route index element={<Welcome />} />
            <Route path="/list" element={<BacteryList />} />
            <Route path="/list/:bacteryName" element={<BacteryPage />} />
            <Route path="/search" element={<SearchPage />} />
          </Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
