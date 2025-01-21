import React, { useState } from 'react';
import { Collapse, Table, Card } from 'react-bootstrap';
import { FaChevronDown, FaChevronRight } from 'react-icons/fa';

const IsolationContent = ({ data }) => {
    const [isolationOpen, setIsolationOpen] = useState(true);

    return (
        <div>
            {data.data["Isolation, sampling and environmental information"] && (
                <Card className="mb-4 shadow-sm">
                    <Card.Header
                        className="d-flex align-items-center justify-content-between"
                        style={{ backgroundColor: '#f8f9fa', cursor: 'pointer' }}
                        onClick={() => setIsolationOpen(!isolationOpen)}
                    >
                        <h4 className="mb-0">Isolation, sampling and environmental information</h4>
                        {isolationOpen ? <FaChevronDown /> : <FaChevronRight />}
                    </Card.Header>
                    <Collapse in={isolationOpen}>
                        <div id="isolation-content">
                            <Card.Body>
                                <Table striped bordered hover className="mt-3">
                                    <tbody>
                                        {data.data["Isolation, sampling and environmental information"]["isolation"] && (
                                            <>
                                                {Array.isArray(data.data["Isolation, sampling and environmental information"]["isolation"]) ? (
                                                    data.data["Isolation, sampling and environmental information"]["isolation"].map((data, index) => (
                                                        <>
                                                            <tr>
                                                                <td>@ref {data["@ref"]}</td>
                                                                <td><strong>Sample type</strong>
                                                                </td>
                                                                <td>{data["sample type"]}</td>
                                                            </tr>
                                                            {data["sampling date"] && (
                                                                <tr>
                                                                    <td>@ref {data["@ref"]}</td>
                                                                    <td><strong>Sampling date</strong></td>
                                                                    <td>{data["sampling date"]}
                                                                    </td>
                                                                </tr>
                                                            )}
                                                            {data["country"] && (
                                                                <tr>
                                                                    <td>@ref {data["@ref"]}</td>
                                                                    <td><strong>Country</strong></td>
                                                                    <td>{data["country"]}</td>
                                                                </tr>
                                                            )}
                                                            {data["origin.country"] && (
                                                                <tr>
                                                                    <td>@ref {data["@ref"]}</td>
                                                                    <td><strong>Country ISO 3 Code</strong></td>
                                                                    <td>{data["origin.country"]}</td>
                                                                </tr>
                                                            )}
                                                            {data["continent"] && (
                                                                <tr>
                                                                    <td>@ref {data["@ref"]}</td>
                                                                    <td><strong>Countinent</strong></td>
                                                                    <td>{data["continent"]}</td>
                                                                </tr>
                                                            )}
                                                            {data["isolation date"] && (
                                                                <tr>
                                                                    <td>@ref {data["@ref"]}</td>
                                                                    <td><strong>Isolation date</strong></td>
                                                                    <td>{data["isolation date"]}
                                                                    </td>
                                                                </tr>
                                                            )}
                                                            <br></br>
                                                        </>
                                                    ))
                                                ) : (
                                                    <>
                                                        <tr>
                                                            <td>@ref {data.data["Isolation, sampling and environmental information"]["isolation"]["@ref"]}</td>
                                                            <td><strong>Sample type</strong>
                                                            </td>
                                                            <td>{data.data["Isolation, sampling and environmental information"]["isolation"]["sample type"]}</td>
                                                        </tr>
                                                        {data.data["Isolation, sampling and environmental information"]["isolation"]["sampling date"] && (
                                                            <tr>
                                                                <td>@ref {data.data["Isolation, sampling and environmental information"]["isolation"]["@ref"]}</td>
                                                                <td><strong>Sampling date</strong></td>
                                                                <td>{data.data["Isolation, sampling and environmental information"]["isolation"]["sampling date"]}
                                                                </td>
                                                            </tr>
                                                        )}
                                                        {data.data["Isolation, sampling and environmental information"]["isolation"]["country"] && (
                                                            <tr>
                                                                <td>@ref {data.data["Isolation, sampling and environmental information"]["isolation"]["@ref"]}</td>
                                                                <td><strong>Country</strong></td>
                                                                <td>{data.data["Isolation, sampling and environmental information"]["isolation"]["country"]}</td>
                                                            </tr>
                                                        )}
                                                        {data.data["Isolation, sampling and environmental information"]["isolation"]["origin.country"] && (
                                                            <tr>
                                                                <td>@ref {data.data["Isolation, sampling and environmental information"]["isolation"]["@ref"]}</td>
                                                                <td><strong>Country ISO 3 Code</strong></td>
                                                                <td>{data.data["Isolation, sampling and environmental information"]["isolation"]["origin.country"]}</td>
                                                            </tr>
                                                        )}
                                                        {data.data["Isolation, sampling and environmental information"]["isolation"]["continent"] && (
                                                            <tr>
                                                                <td>@ref {data.data["Isolation, sampling and environmental information"]["isolation"]["@ref"]}</td>
                                                                <td><strong>Countinent</strong></td>
                                                                <td>{data.data["Isolation, sampling and environmental information"]["isolation"]["continent"]}</td>
                                                            </tr>
                                                        )}
                                                        {data.data["Isolation, sampling and environmental information"]["isolation"]["isolation date"] && (
                                                            <tr>
                                                                <td>@ref {data.data["Isolation, sampling and environmental information"]["isolation"]["@ref"]}</td>
                                                                <td><strong>Isolation date</strong></td>
                                                                <td>{data.data["Isolation, sampling and environmental information"]["isolation"]["isolation date"]}
                                                                </td>
                                                            </tr>
                                                        )}
                                                        <br></br>
                                                    </>
                                                )}
                                            </>
                                        )}

                                        {data.data["Isolation, sampling and environmental information"]["isolation source categories"] && (
                                            <tr>
                                                <td>Isolation sources category</td>
                                                <td>
                                                    <Table striped bordered hover>
                                                        <tbody>
                                                            {Array.isArray(data.data["Isolation, sampling and environmental information"]["isolation source categories"]) ? (
                                                                data.data["Isolation, sampling and environmental information"]["isolation source categories"].map((data, index) => (
                                                                    <>
                                                                        <tr>
                                                                            {data["Cat1"] && (
                                                                                <td>{data["Cat1"]}
                                                                                </td>
                                                                            )}
                                                                            {data["Cat2"] && (
                                                                                <td>{data["Cat2"]}
                                                                                </td>
                                                                            )}
                                                                            {data["Cat3"] ? (
                                                                                <td>{data["Cat3"]}
                                                                                </td>
                                                                            ) : (
                                                                                <td>-</td>
                                                                            )}
                                                                        </tr>
                                                                    </>
                                                                ))
                                                            ) : (
                                                                <>
                                                                    <tr>
                                                                        <td>{data.data["Isolation, sampling and environmental information"]["isolation source categories"]["Cat1"] || '-'}</td>
                                                                        <td>{data.data["Isolation, sampling and environmental information"]["isolation source categories"]["Cat2"] || '-'}</td>
                                                                        <td>{data.data["Isolation, sampling and environmental information"]["isolation source categories"]["Cat3"] || '-'}</td>
                                                                    </tr>
                                                                </>
                                                            )}
                                                        </tbody>
                                                    </Table>
                                                </td>
                                            </tr>
                                        )}
                                    </tbody>
                                </Table>
                            </Card.Body>
                        </div>
                    </Collapse>
                </Card>
            )}
        </div>
    )
}

export default IsolationContent