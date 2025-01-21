import React, { useState } from 'react';
import { Collapse, Table, Card } from 'react-bootstrap';
import { FaChevronDown, FaChevronRight } from 'react-icons/fa';

const SequenceContent = ({ data }) => {
    const [sequenceOpen, setSequenceOpen] = useState(true);

    return (
        <div>
            {data.data["Sequence information"] && (
                <Card className="mb-4 shadow-sm">
                    <Card.Header
                        className="d-flex align-items-center justify-content-between"
                        style={{ backgroundColor: '#f8f9fa', cursor: 'pointer' }}
                        onClick={() => setSequenceOpen(!sequenceOpen)}
                    >
                        <h4 className="mb-0">Sequence information</h4>
                        {sequenceOpen ? <FaChevronDown /> : <FaChevronRight />}
                    </Card.Header>
                    <Collapse in={sequenceOpen}>
                        <div id="sequence-content">
                            <Card.Body>
                                <h6>16S sequence information:</h6>
                                <Table striped bordered hover className="mt-3">
                                    <thead>
                                        <tr>
                                            <td></td>
                                            <td><strong>Sequence accession description</strong></td>
                                            <td><strong>Seq. accession number</strong></td>
                                            <td><strong>Sequence length (bp)</strong></td>
                                            <td><strong>Sequence database</strong></td>
                                            <td><strong>Associated NCBI tax ID</strong></td>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {Array.isArray(data.data["Sequence information"]["16S sequences"]) ? (
                                            data.data["Sequence information"]["16S sequences"].map((data, index) => (
                                                <>
                                                    <tr>
                                                        <td>@ref {data["@ref"]}</td>
                                                        <td>{data["description"]}</td>
                                                        <td>{data["accession"]}</td>
                                                        <td>{data["length"]}</td>
                                                        <td>{data["database"]}</td>
                                                        <td>{data["NCBI tax ID"]}</td>
                                                    </tr>
                                                </>
                                            ))
                                        ) : (
                                            <>
                                                <tr>
                                                    <td>@ref {data.data["Sequence information"]["16S sequences"]["@ref"]}</td>
                                                    <td>{data.data["Sequence information"]["16S sequences"]["description"]}</td>
                                                    <td>{data.data["Sequence information"]["16S sequences"]["accession"]}</td>
                                                    <td>{data.data["Sequence information"]["16S sequences"]["length"]}</td>
                                                    <td>{data.data["Sequence information"]["16S sequences"]["database"]}</td>
                                                    <td>{data.data["Sequence information"]["16S sequences"]["NCBI tax ID"]}</td>
                                                </tr>
                                            </>
                                        )}
                                    </tbody>
                                </Table>

                                {data.data["Sequence information"]["Genome sequences"] && (
                                    <>
                                        <h6>Genome sequence information:</h6>
                                        <Table striped bordered hover className="mt-3">
                                            <thead>
                                                <tr>
                                                    <td><strong>Sequence accession description</strong></td>
                                                    <td><strong>Seq. accession number</strong></td>
                                                    <td><strong>Assembly level</strong></td>
                                                    <td><strong>Sequence database</strong></td>
                                                    <td><strong>Associated NCBI tax ID</strong></td>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {Array.isArray(data.data["Isolation, sampling and environmental information"]["isolation source categories"]) ? (
                                                    data.data["Sequence information"]["Genome sequences"].map((genome, index) => (
                                                        <>
                                                            <tr>
                                                                <td>{genome["description"]}</td>
                                                                <td>{genome["accession"]}</td>
                                                                <td>{genome["assembly level"]}</td>
                                                                <td>{genome["database"]}</td>
                                                                <td>{genome["NCBI tax ID"]}</td>
                                                            </tr>
                                                        </>
                                                    ))
                                                ) : (
                                                    <>
                                                        <tr>
                                                            <td>{data.data["Sequence information"]["Genome sequences"]["description"]}</td>
                                                            <td>{data.data["Sequence information"]["Genome sequences"]["accession"]}</td>
                                                            <td>{data.data["Sequence information"]["Genome sequences"]["assembly level"]}</td>
                                                            <td>{data.data["Sequence information"]["Genome sequences"]["database"]}</td>
                                                            <td>{data.data["Sequence information"]["Genome sequences"]["NCBI tax ID"]}</td>
                                                        </tr>
                                                    </>
                                                )}
                                            </tbody>
                                        </Table>
                                    </>
                                )}
                            </Card.Body>
                        </div>
                    </Collapse>
                </Card>
            )}
        </div>
    )
}

export default SequenceContent