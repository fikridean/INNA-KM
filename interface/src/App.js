import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Welcome from './components/Welcome';
import BacteryList from './pages/Bactery/BacteryList';
import BacteryPage from './pages/Bactery/BacteryPage';
import Taxa from './pages/Taxa/Taxa';
import CreateTaxa from './pages/Taxa/CreateTaxa';
import DetailTaxa from './pages/Taxa/DetailTaxa';

function App() {
  return (
    <div className="App Container">
      <Router>
        <Routes>
          <Route path="/" element={<Home />}>
            <Route index element={<Welcome />} />
            <Route path="/list" element={<BacteryList />} />
            <Route path="/list/:bacteryName" element={<BacteryPage />} />
            <Route path="/taxa" element={<Taxa />} />
            <Route path="/taxa/create" element={<CreateTaxa />} />
            <Route path="/taxa/detail/:id" element={<DetailTaxa />} />
          </Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
