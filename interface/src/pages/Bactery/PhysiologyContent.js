import React, { useState } from 'react';
import { Link } from 'react-router-dom'
import { Collapse, Table, Card } from 'react-bootstrap';
import { FaChevronDown, FaChevronRight } from 'react-icons/fa';



const PhysiologyContent = ({ data }) => {
    const [physiologyOpen, setPhysiologyOpen] = useState(true);

    return (
        <div>
            {data.data["Physiology and metabolism"] && (
                <Card className="mb-4 shadow-sm">
                    <Card.Header
                        className="d-flex align-items-center justify-content-between"
                        style={{ backgroundColor: '#f8f9fa', cursor: 'pointer' }}
                        onClick={() => setPhysiologyOpen(!physiologyOpen)}
                    >
                        <h4 className="mb-0">Physiology and Metabolism</h4>
                        {physiologyOpen ? <FaChevronDown /> : <FaChevronRight />}
                    </Card.Header>
                    <Collapse in={physiologyOpen}>
                        <div id="physiology-content">
                            <Card.Body>
                                <Table striped bordered hover className="mt-3">
                                    <tbody>
                                        {data.data["Physiology and metabolism"]["oxygen tolerance"] && (
                                            <tr>
                                                <td><strong>Oxygen Tolerance</strong>
                                                    <p>@ref {data.data["Physiology and metabolism"]["oxygen tolerance"]["@ref"]}</p>
                                                </td>
                                                <td>{data.data["Physiology and metabolism"]["oxygen tolerance"]["oxygen tolerance"]}</td>
                                            </tr>
                                        )}

                                        {data.data["Physiology and metabolism"]["metabolite utilization"] && (
                                            <tr>
                                                <td><strong>Metabolite Utilization</strong></td>
                                                <td>
                                                    <Table striped bordered hover className="mt-3">
                                                        <thead>
                                                            <tr>
                                                                <td>Metabolite</td>
                                                                <td>Utilization activity</td>
                                                                <td>kind of utilization tested</td>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {data.data["Physiology and metabolism"]["metabolite utilization"].map((metabolite, index) => (
                                                                <>
                                                                    <tr>
                                                                        <td>{metabolite.metabolite}</td>
                                                                        <td>{metabolite["utilization activity"]}</td>
                                                                        <td>{metabolite["kind of utilization tested"]}</td>
                                                                    </tr>
                                                                </>
                                                            ))}
                                                        </tbody>
                                                    </Table>
                                                </td>
                                            </tr>
                                        )}

                                        <tr>
                                            <td>Metabolite production

                                            </td>
                                            <td>
                                                <Table striped bordered hover className="mt-3">
                                                    <tbody>
                                                        <tr>
                                                            <td>Ref</td>
                                                            <td>Metabolite</td>
                                                            <td>Production</td>
                                                        </tr>
                                                        {data.data["Physiology and metabolism"]["metabolite production"] && (
                                                            Array.isArray(data.data["Physiology and metabolism"]["metabolite production"]) ? (
                                                                data.data["Physiology and metabolism"]["metabolite production"].map((production, index) => (
                                                                    <>
                                                                        <tr>
                                                                            <td>@ref {production["@ref"]}</td>
                                                                            <td>{production["metabolite"]}</td>
                                                                            <td>{production["production"]}</td>
                                                                        </tr>
                                                                    </>
                                                                ))
                                                            ) : (
                                                                <>
                                                                    <tr>
                                                                        <td>@ref {data.data["Physiology and metabolism"]["metabolite production"]["@ref"]}</td>
                                                                        <td>{data.data["Physiology and metabolism"]["metabolite production"]["metabolite"]}</td>
                                                                        <td>{data.data["Physiology and metabolism"]["metabolite production"]["production"]}</td>
                                                                    </tr>
                                                                </>
                                                            )
                                                        )}
                                                    </tbody>
                                                </Table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Physiological test

                                            </td>
                                            <td>
                                                <Table striped bordered hover>
                                                    <tbody>
                                                        <tr>
                                                            <td>Ref</td>
                                                            <td>Metabolite</td>
                                                            <td>Indole test</td>
                                                        </tr>
                                                        {data.data["Physiology and metabolism"]["metabolite test"] && (
                                                            Array.isArray(data.data["Physiology and metabolism"]["metabolite tests"]) ? (
                                                                data.data["Physiology and metabolism"]["metabolite tests"].map((metabolite_test, index) => (
                                                                    <>
                                                                        <tr>
                                                                            <td>@ref {metabolite_test["@ref"]}</td>
                                                                            <td><Link to={`https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:${metabolite_test["Chebi-ID"]}`}>{metabolite_test["metabolite"]}</Link></td>
                                                                            <td>{metabolite_test["indole test"]}</td>
                                                                        </tr>
                                                                    </>
                                                                ))
                                                            ) : (
                                                                <>
                                                                    <tr>
                                                                        <td>@ref {data.data["Physiology and metabolism"]["metabolite tests"]["@ref"]}</td>
                                                                        <td><Link to={`https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:${data.data["Physiology and metabolism"]["metabolite tests"]["Chebi-ID"]}`}>{data.data["Physiology and metabolism"]["metabolite tests"]["metabolite"]}</Link></td>
                                                                        <td>{data.data["Physiology and metabolism"]["metabolite tests"]["indole test"]}</td>
                                                                    </tr>
                                                                </>
                                                            )
                                                        )}
                                                    </tbody>
                                                </Table>
                                            </td>
                                        </tr>

                                        {data.data["Physiology and metabolism"]["enzymes"] && (
                                            <tr>
                                                <td><strong>Enzymes</strong></td>
                                                <td>
                                                    <Table striped bordered hover className="mt-3">
                                                        <thead>
                                                            <tr>
                                                                <td>Enzyme</td>
                                                                <td>Enzyme activity</td>
                                                                <td>EC number</td>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {data.data["Physiology and metabolism"]["enzymes"].map((enzyme, index) => (
                                                                <>
                                                                    <tr>
                                                                        <td>{enzyme.value}</td>
                                                                        <td>{enzyme["activity"]}</td>
                                                                        <td>{enzyme["ec"]}</td>
                                                                    </tr>
                                                                </>
                                                            ))}
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

export default PhysiologyContent