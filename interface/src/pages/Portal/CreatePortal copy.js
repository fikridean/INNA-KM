import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { getPortalDetail, createTaxa } from '../../services/api';

const CreatePortal = () => {
    const [formData, setFormData] = useState({
        taxon_id: '',
        portal_id: '',
        web: [],
    });
    const [isTaxonIdValid, setIsTaxonIdValid] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const webOptions = ["wikidata", "ncbi", "bacdive", "gbif"];

    // Fungsi untuk mengecek apakah taxon_id unik
    const checkTaxonIdUnique = async (id) => {
        try {
            const response = await getPortalDetail(id);
            console.log(response.data.taxon_id)
            if (response.data.taxon_id) {
                setError('Taxon ID is already in use.');
            } else {
                setIsTaxonIdValid(true);
            }
        } catch (error) {
            // Jika error berarti taxon_id belum ada (valid untuk dipakai)
            setIsTaxonIdValid(true);
        }
    };

    const handleTaxonIdChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
        if (value) {
            checkTaxonIdUnique(value);
        }
    };

    // Handle input changes
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
            taxon_id: name === 'portal_id' ? value : prevData.taxon_id,
        }));
    };

    // Handle checkbox changes for web options
    const handleCheckboxChange = (option) => {
        setFormData((prevData) => ({
            ...prevData,
            web: prevData.web.includes(option)
                ? prevData.web.filter((item) => item !== option)
                : [...prevData.web, option],
        }));
    };

    // Handler untuk submit form
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!isTaxonIdValid) {
            setError("Portal ID sudah dipakai, gunakan ID lain.");
            return;
        }
        try {
            //   const response = await createTaxa(formData);
            //   console.log(response)
            //   navigate('/taxa');
        } catch (error) {
            setError("Gagal membuat taxa baru.");
        }
    };

    return (
        <div>
            <h2>Create Portal</h2>
            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}

            
            <Form onSubmit={handleSubmit}>
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


                <Form.Group controlId="portal_id">
                    <Form.Label>Portal ID</Form.Label>
                    <Form.Control
                        type="number"
                        name="portal_id"
                        value={formData.portal_id}
                        onChange={handleTaxonIdChange}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="taxon_id">
                    <Form.Label>Portal ID (Auto-filled)</Form.Label>
                    <Form.Control
                        type="number"
                        name="taxon_id"
                        value={formData.taxon_id}
                        readOnly
                    />
                </Form.Group>

                <Form.Group controlId="web">
                    <Form.Label>Web Options</Form.Label>
                    {webOptions.map((option) => (
                        <Form.Check
                            key={option}
                            type="checkbox"
                            label={option}
                            checked={formData.web.includes(option)}
                            onChange={() => handleCheckboxChange(option)}
                        />
                    ))}
                </Form.Group>

                <Button variant="primary" type="submit" disabled={!isTaxonIdValid}>
                    Submit
                </Button>
            </Form>
        </div>
    )
}

export default CreatePortal