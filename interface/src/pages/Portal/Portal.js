import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Table, Button, Pagination } from "react-bootstrap";
import { getPortals, deletePortal } from '../../services/api';

const BacteryList = () => {
  const navigate = useNavigate();
  const [dataBacteries, setDataBacteries] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;
  const [isSortedByTaxon, setIsSortedByTaxon] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getPortals();
        console.log(response.data);
        setDataBacteries(response.data);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
    fetchData();
  }, []);

  const handleDelete = async (portal_id) => {
    try {
      await deletePortal(portal_id);
      window.location.reload(); // Refresh the page after successful deletion
    } catch (err) {
      console.error('Failed to delete portal:', err);
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
      <h1>Portal List</h1>
      <Link to={`/portals/create`} className="btn btn-primary">
        Create
      </Link>
      {/* <Button variant="dark" onClick={toggleSort} className="ms-3">
        {isSortedByTaxon ? 'Sort by Name' : 'Sort by Taxon ID'}
      </Button> */}
      <Table striped bordered hover className="mt-3">
        <thead>
          <tr>
            <th>Portal_id</th>
            <th>Taxon_id</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {currentItems.length > 0 ? (
            currentItems.map((bacterium, index) => (
              <tr key={index}>
                <td>{bacterium.portal_id}</td>
                <td>{bacterium.taxon_id}</td>
                <td>
                  {/* <Link to={`/taxa/update/${bacterium.taxon_id}`} className="btn btn-primary">
                    Detail
                  </Link>{' '} */}
                  <Button variant="danger" onClick={() => handleDelete(bacterium.portal_id)}>Delete</Button>
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
