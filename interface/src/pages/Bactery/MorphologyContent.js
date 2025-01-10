import React, { useState } from 'react';
import { Collapse, Table, Card } from 'react-bootstrap';
import { FaChevronDown, FaChevronRight } from 'react-icons/fa';

const MorphologyContent = ({ data }) => {
    const [morphologyOpen, setMorphologyOpen] = useState(true);

    return (
        <div>
            {data.data.Morphology && (
                <Card className="mb-4 shadow-sm">
                    <Card.Header
                        className="d-flex align-items-center justify-content-between"
                        style={{ backgroundColor: '#f8f9fa', cursor: 'pointer' }}
                        onClick={() => setMorphologyOpen(!morphologyOpen)}
                    >
                        <h4 className="mb-0">Morphology</h4>
                        {morphologyOpen ? <FaChevronDown /> : <FaChevronRight />}
                    </Card.Header>
                    <Collapse in={morphologyOpen}>
                        <div id="morphology-content">
                            <Card.Body>
                                <Table striped bordered hover className="mt-3">
                                    <tbody>
                                        {data.data.Morphology["cell morphology"] && (
                                            <>
                                                <tr>
                                                    <td><strong>Gram Stain</strong></td>
                                                    <td>{data.data.Morphology["cell morphology"]["gram stain"]}</td>
                                                </tr>
                                                <tr>
                                                    <td><strong>Cell Shape</strong></td>
                                                    <td>{data.data.Morphology["cell morphology"]["cell shape"]}</td>
                                                </tr>
                                                <tr>
                                                    <td><strong>Motility</strong></td>
                                                    <td>{data.data.Morphology["cell morphology"]["motility"]}</td>
                                                </tr>
                                            </>
                                        )}
                                        {data.data.Morphology["colony morphology"] && (
                                            <>
                                                {Array.isArray(data.data.Morphology["colony morphology"]) ? (
                                                    <>
                                                        {data.data.Morphology["colony morphology"].map((colonyMorphology, index) => (
                                                            <tr key={index}>
                                                                <td>
                                                                    <strong>Incubation period</strong>
                                                                    <p>@ref {colonyMorphology["@ref"]}</p>
                                                                </td>
                                                                <td>{colonyMorphology["incubation period"]}</td>
                                                            </tr>
                                                        ))}
                                                    </>
                                                ) : (
                                                    <tr>
                                                        <td>
                                                            <strong>Incubation period</strong>
                                                            <p>@ref {data.data.Morphology["colony morphology"]["@ref"]}</p>
                                                        </td>
                                                        <td>{data.data.Morphology["colony morphology"]["incubation period"]}</td>
                                                    </tr>
                                                )}
                                            </>
                                        )}
                                    </tbody>
                                </Table>
                            </Card.Body>
                        </div>
                    </Collapse>
                </Card>
            )}
        </div>
    );
};

export default MorphologyContent;
