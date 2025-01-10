import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { Form, Button, Container, Alert, Card } from "react-bootstrap";
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

  const checkTaxonIdUnique = async (id) => {
    try {
      const response = await getTaxonDetail(id);
      if (response.data.ncbi_taxon_id) {
        setIsTaxonIdValid(false);
      } else {
        setIsTaxonIdValid(true);
      }
    } catch (error) {
      setIsTaxonIdValid(true);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isTaxonIdValid) {
      setError("Taxon ID sudah dipakai, gunakan ID lain.");
      return;
    }
    try {
      await createTaxa(formData);
      navigate('/taxa');
    } catch (error) {
      setError("Gagal membuat taxa baru.");
    }
  };

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
    <Container className="mt-5">
      <Card className="shadow">
        <Card.Header className="bg-primary text-white">
          <h4 className="mb-0">Create New Taxa</h4>
        </Card.Header>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="species" className="mb-3">
              <Form.Label>Species</Form.Label>
              <Form.Control
                type="text"
                name="species"
                value={formData.species}
                onChange={handleChange}
                placeholder="Enter species name"
                required
              />
            </Form.Group>

            <Form.Group controlId="ncbi_taxon_id" className="mb-3">
              <Form.Label>NCBI Taxon ID</Form.Label>
              <Form.Control
                type="text"
                name="ncbi_taxon_id"
                value={formData.ncbi_taxon_id}
                onChange={handleChange}
                placeholder="Enter NCBI Taxon ID"
                required
              />
            </Form.Group>

            <Form.Group controlId="taxon_id" className="mb-3">
              <Form.Label>Taxon ID</Form.Label>
              <Form.Control
                type="number"
                name="taxon_id"
                value={formData.taxon_id}
                onChange={handleTaxonIdChange}
                isInvalid={!isTaxonIdValid}
                placeholder="Enter unique Taxon ID"
                required
              />
              <Form.Control.Feedback type="invalid">
                Taxon ID sudah dipakai, coba ID lain.
              </Form.Control.Feedback>
            </Form.Group>

            <div className="d-flex justify-content-between">
              <Button variant="secondary" onClick={() => navigate('/taxa')}>
                Cancel
              </Button>
              <Button variant="primary" type="submit" disabled={!isTaxonIdValid}>
                Submit
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default CreateTaxa;
