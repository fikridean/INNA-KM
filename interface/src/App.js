import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Welcome from './components/Welcome';
import BacteryList from './pages/BacteryList';
import BacteryPage from './pages/BacteryPage';
import SearchPage from './pages/SearchPage';
import Taxa from './pages/Taxa/Taxa';
import CreateTaxa from './pages/Taxa/CreateTaxa';
import DetailTaxa from './pages/Taxa/DetailTaxa';
import UpdateTaxa from './pages/Taxa/UpdateTaxa';
import Portal from './pages/Portal/Portal';
import CreatePortal from './pages/Portal/CreatePortal';

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
            <Route path="/taxa" element={<Taxa />} />
            <Route path="/taxa/create" element={<CreateTaxa />} />
            <Route path="/taxa/detail/:id" element={<DetailTaxa />} />
            <Route path="/taxa/update/:id" element={<UpdateTaxa />} />
            <Route path="/portals" element={<Portal />} />
            <Route path="/portals/create" element={<CreatePortal />} />
            <Route path="/portals/update/:id" element={<UpdateTaxa />} />
            <Route path="/raws/create/:id" element={<CreatePortal />} />
          </Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
