import React from 'react';
import { NavLink } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function Header() {
  return (
    <Navbar bg="light" expand="lg" className="shadow-sm">
      <Container>
        <Navbar.Brand as={NavLink} to="/">
          <img
            src="/logobrin.png" // Ganti dengan path ke logo Anda
            alt="Logo INNAKM"
            width="90"
            height="48"
            className="d-inline-block align-top"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={NavLink} to="/" end className="nav-link" activeClassName="active">
              Home
            </Nav.Link>
            <Nav.Link as={NavLink} to="/list" className="nav-link" activeClassName="active">
              Bactery List
            </Nav.Link>
            {/* <Nav.Link as={NavLink} to="/taxa" className="nav-link" activeClassName="active">
              Taxa
            </Nav.Link> */}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
