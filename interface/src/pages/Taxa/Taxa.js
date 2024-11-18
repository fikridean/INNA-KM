import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Table, Button, Pagination } from "react-bootstrap";
import { getTaxa, deleteTaxa, getTaxonDetail, deletePortal, deleteRaws,deleteTerms } from '../../services/api';

const BacteryList = () => {
  const navigate = useNavigate();
  const [dataBacteries, setDataBacteries] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;
  const [isSortedByTaxon, setIsSortedByTaxon] = useState(true);
  const [dataTaxa, setDataTaxa] = useState([]);

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
        setIsSortedByTaxon(!isSortedByTaxon);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
    
    fetchData();
  }, []);

  const handleDelete = async (taxon_id) => {
    try {
      const responseTaxa = await getTaxonDetail(taxon_id);
      setDataTaxa(responseTaxa.data);
      console.log(responseTaxa.data.ncbi_taxon_id)
      await deleteTerms(responseTaxa.data.ncbi_taxon_id);
      await deleteRaws(responseTaxa.data.ncbi_taxon_id);
      await deletePortal(taxon_id);
      await deleteTaxa(taxon_id);
      window.location.reload(); // Refresh the page after successful deletion
    } catch (err) {
      console.error('Failed to delete taxa:', err);
    }
  };

  // Sort and set dataBacteries based on toggle
  const toggleSort = () => {
    const sortedData = [...dataBacteries].sort((a, b) =>
      isSortedByTaxon
        ? a.species.localeCompare(b.species)
        : a.taxon_id - b.taxon_id
    );
    setDataBacteries(sortedData);
    setIsSortedByTaxon(!isSortedByTaxon);
  };

  // Pagination logic to get current items based on the sorted data
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = dataBacteries.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(dataBacteries.length / itemsPerPage);

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
    <div>
      <h1>Taxa List</h1>
      <Link to={`/taxa/create`} className="btn btn-primary">
        Create
      </Link>
      <Button variant="dark" onClick={toggleSort} className="ms-3">
        {isSortedByTaxon ? 'Sort by Name' : 'Sort by Taxon ID'}
      </Button>
      <Table striped bordered hover className="mt-3">
        <thead>
          <tr>
            <th>Taxon_id</th>
            <th>Name</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {currentItems.length > 0 ? (
            currentItems.map((bacterium, index) => (
              <tr key={index}>
                <td>{bacterium.taxon_id}</td>
                <td>{bacterium.species}</td>
                <td>
                  <Link to={`/taxa/detail/${bacterium.taxon_id}`} className="btn btn-info">
                    Detail
                  </Link>{' '}
                  
                  <Button variant="danger" onClick={() => handleDelete(bacterium.taxon_id)}>Delete</Button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3" className="text-center">
                No results found
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      {/* Pagination Controls */}
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
    </div>
  );
};

export default BacteryList;
