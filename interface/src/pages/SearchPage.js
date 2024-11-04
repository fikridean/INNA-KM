import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'
import { Form, Container, Card, Row, Col, Button, InputGroup, Alert } from "react-bootstrap";
import { postSearch } from '../services/api';

const SearchPage = () => {

  const [searchTerm, setSearchTerm] = useState("");
  const [dataBacteries, setDataBacteries] = useState([]);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchBookings = async () => {
      try {
      } catch (error) {
        console.error('Failed to fetch bookings:', error);
      }
    };

    fetchBookings();
  }, []);

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearch = async () => {
    setIsLoading(true); 
    if (searchTerm !== "") {
      const response2 = await postSearch(searchTerm);
      if (response2.data != null) {
        // Sort data alphabetically by species name
        const sortedData = response2.data.sort((a, b) => 
          a.species.localeCompare(b.species)
        );
        setDataBacteries(sortedData);
        setSearchPerformed(true);
        console.log(response2.data);
        setIsLoading(false); 
      }
    }
  };

   // This function checks for the Enter key press
   const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevents form submission if the input is inside a form
      handleSearch();
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <h1>Bactery Search</h1>
      <Form.Group controlId="searchInput" as={Col} md="8">
        <InputGroup className="mb-3">
          <Form.Control
            type="text"
            placeholder="Search for a bacterium..."
            value={searchTerm}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown} // Check for Enter key press
          />
          <Button variant="primary" onClick={handleSearch}>
            <i className="bi bi-search"></i> {/* Bootstrap icon for search */}
          </Button>
        </InputGroup>
      </Form.Group>

      {searchPerformed && dataBacteries.length === 0 && (
        <Alert variant="warning">
          No results found for "{searchTerm}"
        </Alert>
      )}

      <Container className="">
        <Row>
          {dataBacteries.length > 0 ? (
            <>
              {dataBacteries.map((bacterium, index) => (
                <Col md={12} lg={12} key={index} className="mt-4">
                  <Card.Body>
                    <Card.Title>
                      <Link
                        to={`/list/${bacterium.species.replace(/\s+/g, '-')}`}
                        style={{ color: '#007bff', textDecoration: 'none' }}
                      >
                        {bacterium.species}
                      </Link>
                    </Card.Title>
                    <Card.Text style={{ color: '#555' }}>
                      {bacterium.data.Lineage}
                    </Card.Text>
                  </Card.Body>
                </Col>
              ))}
            </>
          ) : (
            <>
            </>
          )}
        </Row>
      </Container >
    </>
  )
}

export default SearchPage