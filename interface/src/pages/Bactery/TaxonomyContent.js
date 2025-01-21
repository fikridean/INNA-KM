import React, { useState } from 'react';
import { Collapse, Table, Card } from 'react-bootstrap';
import { FaChevronDown, FaChevronRight } from 'react-icons/fa';

const TaxonomyContent = ({ data }) => {
    const [taxonomyOpen, setTaxonomyOpen] = useState(true);

    return (
        <Card className="mb-4 shadow-sm">
            <Card.Header
                className="d-flex align-items-center justify-content-between"
                style={{ backgroundColor: '#f8f9fa', cursor: 'pointer' }}
                onClick={() => setTaxonomyOpen(!taxonomyOpen)}
            >
                <h4 className="mb-0">Name and Taxonomic Classification</h4>
                {taxonomyOpen ? <FaChevronDown /> : <FaChevronRight />}
            </Card.Header>
            <Collapse in={taxonomyOpen}>
                <div id="taxonomy-content">
                    <Card.Body>
                        <Table striped bordered hover className="mt-3">
                            <tbody>
                                <tr>
                                    <td><strong>Domain</strong></td>
                                    <td>{data.data["Name and taxonomic classification"].LineageEx.Taxon[1]?.ScientificName}</td>
                                </tr>
                                <tr>
                                    <td><strong>Phylum</strong></td>
                                    <td>{data.data["Name and taxonomic classification"].LineageEx.Taxon[2]?.ScientificName}</td>
                                </tr>
                                <tr>
                                    <td><strong>Class</strong></td>
                                    <td>{data.data["Name and taxonomic classification"].LineageEx.Taxon[3]?.ScientificName}</td>
                                </tr>
                                <tr>
                                    <td><strong>Order</strong></td>
                                    <td>{data.data["Name and taxonomic classification"].LineageEx.Taxon[4]?.ScientificName}</td>
                                </tr>
                                <tr>
                                    <td><strong>Family</strong></td>
                                    <td>{data.data["Name and taxonomic classification"].LineageEx.Taxon[5]?.ScientificName}</td>
                                </tr>
                                <tr>
                                    <td><strong>Genus</strong></td>
                                    <td>{data.data["Name and taxonomic classification"].LineageEx.Taxon[6]?.ScientificName}</td>
                                </tr>
                                <tr>
                                    <td><strong>Species</strong></td>
                                    <td>{data.species}</td>
                                </tr>
                                {data.data["Occurence (geoference records)"] && (
                                    <tr>
                                        <td><strong>Full Scientific Name (LPSN)</strong></td>
                                        <td>{data.data["Occurence (geoference records)"].scientificName}</td>
                                    </tr>
                                )}
                            </tbody>
                        </Table>
                    </Card.Body>
                </div>
            </Collapse>
        </Card>
    );
};

export default TaxonomyContent;
