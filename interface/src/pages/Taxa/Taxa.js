import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Table, Button, Pagination, Container, Row, Col } from "react-bootstrap";
import { getTaxa, deleteTaxa, getTaxonDetail, deletePortal, deleteRaws, deleteTerms } from '../../services/api';

const BacteryList = () => {
  const [dataBacteries, setDataBacteries] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;
  const [isSortedByTaxon, setIsSortedByTaxon] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getTaxa();
        const sortedData = [...response.data].sort((a, b) =>
          isSortedByTaxon
            ? a.species.localeCompare(b.species)
            : a.taxon_id - b.taxon_id
        );
        setDataBacteries(sortedData);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
  }, [isSortedByTaxon]);

  const handleDelete = async (taxon_id) => {
    if (window.confirm("Are you sure you want to delete this item?")) {
      try {
        const responseTaxa = await getTaxonDetail(taxon_id);
        await deleteTerms(responseTaxa.data.ncbi_taxon_id);
        await deleteRaws(responseTaxa.data.ncbi_taxon_id);
        await deletePortal(taxon_id);
        await deleteTaxa(taxon_id);
        setDataBacteries((prev) => prev.filter((item) => item.taxon_id !== taxon_id));
      } catch (err) {
        console.error('Failed to delete taxa:', err);
      }
    }
  };

  const toggleSort = () => {
    setIsSortedByTaxon(!isSortedByTaxon);
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = dataBacteries.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(dataBacteries.length / itemsPerPage);

  const handleNextPage = () => currentPage < totalPages && setCurrentPage(currentPage + 1);
  const handlePrevPage = () => currentPage > 1 && setCurrentPage(currentPage - 1);
  const handlePageSelect = (page) => setCurrentPage(page);

  return (
    <Container className="mt-5">
      <Row className="mb-4">
        <Col>
          <h1 className="text-center text-primary">Taxa List</h1>
        </Col>
      </Row>
      <Row className="mb-4">
        <Col className="d-flex justify-content-between">
          <Button variant="success" as={Link} to={`/taxa/create`}>
            + Create New Taxon
          </Button>
          <Button variant="dark" onClick={toggleSort}>
            {isSortedByTaxon ? "Sort by Taxon ID" : "Sort by Name"}
          </Button>
        </Col>
      </Row>
      <Row>
        <Col>
          <Table striped bordered hover responsive>
            <thead className="bg-light">
              <tr>
                <th className="text-center">Taxon ID</th>
                <th className="text-center">Species Name</th>
                <th className="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {currentItems.length > 0 ? (
                currentItems.map((bacterium, index) => (
                  <tr key={index}>
                    <td className="text-center">{bacterium.taxon_id}</td>
                    <td className="text-center">{bacterium.species}</td>
                    <td className="text-center">
                      <Button
                        variant="info"
                        className="me-2"
                        as={Link}
                        to={`/taxa/detail/${bacterium.taxon_id}`}
                      >
                        Detail
                      </Button>
                      <Button
                        variant="danger"
                        onClick={() => handleDelete(bacterium.taxon_id)}
                      >
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3" className="text-center text-muted">
                    No data available. Please add new taxa.
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
