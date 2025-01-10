import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Table, Button, Pagination, Form, InputGroup, Container, Row, Col } from "react-bootstrap";
import { getTaxa } from '../../services/api';

const BacteryList = () => {
  const [dataBacteries, setDataBacteries] = useState([]);
  const [filteredBacteries, setFilteredBacteries] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const itemsPerPage = 20;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getTaxa();
        // Sort data alphabetically by species name
        const sortedData = response.data.sort((a, b) => 
          a.species.localeCompare(b.species)
        );
        setDataBacteries(sortedData);
        setFilteredBacteries(sortedData); // Initialize with all data
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
  }, []);

  const handleSearch = (query) => {
    setSearchQuery(query);
    const filtered = dataBacteries.filter((bacterium) =>
      bacterium.species.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredBacteries(filtered);
    setCurrentPage(1); // Reset to first page after search
  };

  // Calculate pagination
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredBacteries.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredBacteries.length / itemsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handlePageSelect = (page) => {
    setCurrentPage(page);
  };

  return (
    <Container className="mt-5">
      <Row className="mb-4">
        <Col>
          <h1 className="text-center text-primary">Bactery List</h1>
        </Col>
      </Row>
      <Row className="mb-4">
        <Col md={{ span: 6, offset: 3 }}>
          <InputGroup>
            <Form.Control
              type="text"
              placeholder="Search for a species..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
            />
            <Button variant="primary" onClick={() => handleSearch(searchQuery)}>
              Search
            </Button>
          </InputGroup>
        </Col>
      </Row>
      <Row>
        <Col>
          <Table striped bordered hover responsive>
            <thead className="bg-light">
              <tr>
                <th className="text-center">Species Name</th>
              </tr>
            </thead>
            <tbody>
              {currentItems.length > 0 ? (
                currentItems.map((bacterium, index) => (
                  <tr key={index}>
                    <td className="text-center">
                      <Link to={`/list/${bacterium.species.replace(/\s+/g, '-')}`} className="text-decoration-none">
                        {bacterium.species}
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="1" className="text-center text-muted">
                    No results found. Try searching for another species.
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </Col>
      </Row>
      <Row>
        <Col>
          <Pagination className="justify-content-center">
            <Pagination.Prev onClick={handlePrevPage} disabled={currentPage === 1} />
            {Array.from({ length: totalPages }, (_, i) => (
              <Pagination.Item
                key={i + 1}
                active={i + 1 === currentPage}
                onClick={() => handlePageSelect(i + 1)}
              >
                {i + 1}
              </Pagination.Item>
            ))}
            <Pagination.Next onClick={handleNextPage} disabled={currentPage === totalPages} />
          </Pagination>
        </Col>
      </Row>
    </Container>
  );
};

export default BacteryList;
