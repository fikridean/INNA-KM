import React, { useState, useEffect } from 'react';
// import data from '../data/bakteri.json'
import bacteria1Data from '../data/bakteri.json'
import { Link } from 'react-router-dom'
import { Table, Form, Container } from "react-bootstrap";
import { getMyBookings } from '../services/api';

const Bacdive = () => {

  // const bacteriaData = bacteria1Data

  const [dataBacteries, setDataBacteries] = useState([]);

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await getMyBookings(token)
        setDataBacteries(response.data);
        console.log(response.data);
        // console.log(`data` + dataBacteries);
      } catch (error) {
        console.error('Failed to fetch bookings:', error);
      }
    };

    fetchBookings();
  }, []);



  // function BacteriaSearch() {
  const [searchTerm, setSearchTerm] = useState("");

  // Function to handle search and filter the data
  const handleSearch = (event) => {
    setSearchTerm(event.target.value.toLowerCase());
    console.log(uniqueSpecies)
  };

  const uniqueSpecies = dataBacteries.reduce((acc, current) => {
    const x = acc.find(item => item.species === current.species);
    if (!x) {
      return acc.concat([current]);
    } else {
      return acc;
    }
  }, []);

  // Filter the bacteria data based on the search term
  // const filteredBacteria = uniqueSpecies.filter((bacterium) =>
  //   bacterium.species.toLowerCase().includes(searchTerm)
  // );

  const createSlug = (species) => {
    // return species.toLowerCase().replace(/\s+/g, '-');
    return species.replace(/\s+/g, '-');
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
        {/* <tbody>
          {filteredBacteria.length > 0 ? (
            filteredBacteria.map((bacterium, index) => (
              <tr key={index}>
                <td><Link to={`/bacdive/${bacterium.species}`}>{bacterium.species}</Link></td>
                <td><Link to={`/bacdive/${createSlug(bacterium.species)}`}>{bacterium.species}</Link></td>
               
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" className="text-center">
                No results found
              </td>
            </tr>
          )}
        </tbody> */}
      </Table>

      {/* <h2>Name and taxonomic classification</h2>
      
      <p>List Bacteria</p>
      <ul>
        {data.map((category, index) => (
          <li key={index}>
            <Link to={`/bacdive/${category.nama}`}>{category.nama}</Link>
          </li>
        ))}
      </ul> */}



    </div>
  )
}

export default Bacdive