import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'
import { Table, Button, Pagination } from "react-bootstrap";
import { getTaxa } from '../services/api';

const BacteryList = () => {

  const [dataBacteries, setDataBacteries] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getTaxa()
        // Sort data alphabetically by species name
        const sortedData = response.data.sort((a, b) => 
          a.species.localeCompare(b.species)
        );
        setDataBacteries(sortedData);
        console.log(response.data);
      } catch (error) {
        console.error('Failed to fetch bookings:', error);
      }
    };

    fetchData();
  }, []);

    // Calculate pagination
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
      <h1>Bactery List</h1>
      <Table striped bordered hover className="mt-3">
        <thead>
          <tr>
            <th>Name</th>
          </tr>
        </thead>
        <tbody>
          {currentItems.length > 0 ? (
            currentItems.map((bacterium, index) => (
              <tr key={index}>
                <td>
                  <Link to={`/list/${bacterium.species.replace(/\s+/g, '-')}`}>
                    {bacterium.species}
                  </Link>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" className="text-center">
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
  )
}

export default BacteryList