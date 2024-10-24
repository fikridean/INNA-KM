import React, { useState, useEffect } from 'react';
// import data from '../data/bakteri.json'
import bacteria1Data from '../data/bakteri.json'
import { Link } from 'react-router-dom'
import { Table, Form, Container } from "react-bootstrap";
import { getMyBookings, getSearch } from '../services/api';

const SearchPage = () => {

  // const bacteriaData = bacteria1Data

  const [dataBacteries, setDataBacteries] = useState([]);

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        // const token = localStorage.getItem('token');
        const response = await getMyBookings()
        setDataBacteries(response.data);
        console.log(response.data);
        // console.log(`data` + dataBacteries);
      } catch (error) {
        console.error('Failed to fetch bookings:', error);
      }
    };

    fetchBookings();
  }, []);

  const createSlug = (species) => {
    // return species.toLowerCase().replace(/\s+/g, '-');
    // console.log(species);
    if(species === undefined){
      // console.log("kokono");
    } else {
      return species.replace(/\s+/g, '-');
    }
    // return species.replace(/\s+/g, '-');
    return "ssss1"
  };

  // Function to handle search and filter the data
  const handleSearch = async (event) => {
    if (event.target.value != "") {
      const response2 = await getSearch(event.target.value)
      if (response2.data != null) {
        setDataBacteries(response2.data);
        // console.log(response2.data[0].species)
      }
    }
  };

  return (
    <div>
      <h1>Bacteria Search</h1>
      <Form.Group controlId="searchInput">
        <Form.Control
          type="text"
          placeholder="Search for a bacterium..."
          onChange={handleSearch}
        />
      </Form.Group>

      <Table striped bordered hover className="mt-3">
        <thead>
          <tr>
            <th>Name</th>
            {/* <th>Domain</th>
            <th>Phylum</th>
            <th>Class</th>
            <th>Last Updated</th> */}
          </tr>
        </thead>
        <tbody>
          {dataBacteries.length > 0 ? (
            dataBacteries.map((bacterium, index) => (
              <tr key={index}>
                <td><Link to={`/bacdive/${bacterium.taxon_id}`}>{bacterium.species}</Link></td>
                {/* <td><Link to={`/bacdive/${createSlug(bacterium.species)}`}>{bacterium.species}</Link></td> */}

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





    </div>
  )
}

export default SearchPage