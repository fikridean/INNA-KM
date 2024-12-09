import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { Form, Button, Container, Alert } from "react-bootstrap";
import { getTaxonDetail, createTaxa } from '../../services/api';

const CreateTaxa = () => {
  const [formData, setFormData] = useState({
    species: '',
    ncbi_taxon_id: '',
    taxon_id: '',
  });
  const [isTaxonIdValid, setIsTaxonIdValid] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Fungsi untuk mengecek apakah taxon_id unik
  const checkTaxonIdUnique = async (id) => {
    try {
      const response = await getTaxonDetail(id);
      console.log(response.data.ncbi_taxon_id)
      if (response.data.ncbi_taxon_id) {
        setIsTaxonIdValid(false);
      } else {
        setIsTaxonIdValid(true);
      }
    } catch (error) {
      // Jika error berarti taxon_id belum ada (valid untuk dipakai)
      setIsTaxonIdValid(true);
    }
  };

  // Handler untuk submit form
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isTaxonIdValid) {
      setError("Taxon ID sudah dipakai, gunakan ID lain.");
      return;
    }
    try {
      const response = await createTaxa(formData);
      console.log(response)
      navigate('/taxa');
    } catch (error) {
      setError("Gagal membuat taxa baru.");
    }
  };

  // Handler untuk perubahan taxon_id
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleTaxonIdChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
    if (value) {
      checkTaxonIdUnique(value);
    }
  };

  return (
    <Container className="mt-4">
      <h2>Create Taxa</h2>
      {error && <Alert variant="danger">{error}</Alert>}
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="species">
          <Form.Label>Species</Form.Label>
          <Form.Control
            type="text"
            name="species"
            value={formData.species}
            onChange={handleChange}
            placeholder="Enter species"
          />
        </Form.Group>

        <Form.Group controlId="ncbi_taxon_id">
          <Form.Label>NCBI Taxon ID</Form.Label>
          <Form.Control
            type="text"
            name="ncbi_taxon_id"
            value={formData.ncbi_taxon_id}
            onChange={handleChange}
            placeholder="Enter NCBI Taxon ID"
          />
        </Form.Group>

        <Form.Group controlId="formTaxonId">
          <Form.Label>Taxon ID</Form.Label>
          <Form.Control
            type="number"
            name="taxon_id"
            value={formData.taxonId}
            onChange={handleTaxonIdChange}
            isInvalid={!isTaxonIdValid}
            required
          />
          <Form.Control.Feedback type="invalid">
            Taxon ID sudah dipakai.
          </Form.Control.Feedback>
        </Form.Group>

        <Button variant="primary" type="submit" disabled={!isTaxonIdValid}>
          Submit
        </Button>
      </Form>
    </Container>
  )
}

export default CreateTaxa