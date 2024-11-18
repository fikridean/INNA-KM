import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Form, Button, Container } from 'react-bootstrap';
import { getTaxonDetail, createTaxa } from '../../services/api';

const UpdateTaxa = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        species: '',
        ncbi_taxon_id: '',
        taxon_id: id
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await getTaxonDetail(id)
                const { species, ncbi_taxon_id, taxon_id } = response.data;
                // console.log("1response.data");
                // console.log(response.data);
                setFormData({ species, ncbi_taxon_id, taxon_id });
            } catch (error) {
                console.error("Error fetching taxa details:", error);
            }
        };
        fetchData();
    }, [id]);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Di sini Anda dapat menambahkan logika untuk mengirim data ke backend
        // console.log(formData);
        const response = await createTaxa(formData);
        console.log(response)
        navigate('/taxa');
    };

    return (
        <Container className="mt-4">
            <h2>Update Taxa</h2>
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

                <Form.Group controlId="taxon_id">
                    <Form.Label>Taxon ID</Form.Label>
                    <Form.Control
                        type="text"
                        name="taxon_id"
                        value={formData.taxon_id}
                        readOnly
                    />
                </Form.Group>
                <br></br>
                <Button variant="primary" type="submit">
                    Update Taxa
                </Button>
            </Form>
        </Container>
    )
}

export default UpdateTaxa