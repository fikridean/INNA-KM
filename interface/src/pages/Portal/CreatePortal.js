import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { Form, Button, Container, Alert } from "react-bootstrap";
import { getPortalDetail, createPortal } from '../../services/api';

const CreatePortal = () => {
    const [formData, setFormData] = useState({
        portal_id: '',
        taxon_id: '',
        web: [],
    });
    const [isPortalIdValid, setIsPortalIdValid] = useState(true);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const webOptions = ["wikidata", "ncbi", "bacdive", "gbif"];

    // Fungsi untuk mengecek apakah taxon_id unik
    const checkPortalIdUnique = async (id) => {
        try {
            const response = await getPortalDetail(id);
            // console.log(response.data.taxon_id)
            if (response.data.taxon_id) {
                setIsPortalIdValid(false);
            } else {
                setIsPortalIdValid(true);
            }
        } catch (error) {
            // Jika error berarti taxon_id belum ada (valid untuk dipakai)
            setIsPortalIdValid(true);
        }
    };


    const handlePortalIdChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
            taxon_id: name === 'portal_id' ? value : prevData.taxon_id,
        }));
        if (value) {
            checkPortalIdUnique(value);
        }
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
        if (!isPortalIdValid) {
            setError("Taxon ID sudah dipakai, gunakan ID lain.");
            return;
        }
        try {
            const response = await createPortal(formData);
            console.log(response)
            navigate('/portals');
        } catch (error) {
            setError("Gagal membuat taxa baru.");
        }
    };

    return (
        <Container className="mt-4">
            <h2>Create Portal</h2>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formPortalId">
                    <Form.Label>Portal ID</Form.Label>
                    <Form.Control
                        type="number"
                        name="portal_id"
                        value={formData.portal_id}
                        onChange={handlePortalIdChange}
                        isInvalid={!isPortalIdValid}
                        required
                    />
                    <Form.Control.Feedback type="invalid">
                        Portal ID sudah dipakai.
                    </Form.Control.Feedback>
                </Form.Group>

                {/* <Form.Group controlId="taxon_id">
                    <Form.Label>Taxon_id </Form.Label>
                    <Form.Control
                        type="number"
                        name="taxon_id"
                        value={formData.taxon_id}
                        disabled
                        readOnly
                    />
                </Form.Group> */}
                <br></br>
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
                <br></br>
                <Button variant="primary" type="submit" disabled={!isPortalIdValid}>
                    Submit
                </Button>
            </Form>
        </Container>
    )
}

export default CreatePortal