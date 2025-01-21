import React, { useState } from 'react';
import { Collapse, Table, Card } from 'react-bootstrap';
import { FaChevronDown, FaChevronRight } from 'react-icons/fa';

const SafetyContent = ({ data }) => {
    const [safetyOpen, setSafetyOpen] = useState(true);

    return (
        <div>
            {data.data["Safety information"] && (
                <Card className="mb-4 shadow-sm">
                    <Card.Header
                        className="d-flex align-items-center justify-content-between"
                        style={{ backgroundColor: '#f8f9fa', cursor: 'pointer' }}
                        onClick={() => setSafetyOpen(!safetyOpen)}
                    >
                        <h4 className="mb-0">Safety information</h4>
                        {safetyOpen ? <FaChevronDown /> : <FaChevronRight />}
                    </Card.Header>
                    <Collapse in={safetyOpen}>
                        <div id="safety-content">
                            <Card.Body>
                                <Table striped bordered hover className="mt-3">
                                    <tbody>
                                        {Array.isArray(data.data["Safety information"]["risk assessment"]) ? (
                                            data.data["Safety information"]["risk assessment"].map((risk, index) => (
                                                <>
                                                    <tr>
                                                        <td>@ref {risk["@ref"]}</td>
                                                        <td><strong>Biosafety Level</strong></td>
                                                        <td>{risk["biosafety level"]}</td>
                                                        <td>{risk["biosafety level comment"]}</td>
                                                    </tr>
                                                </>
                                            ))
                                        ) : (
                                            <>
                                                <tr>
                                                    <td>@ref {data.data["Safety information"]["risk assessment"]["@ref"]}</td>
                                                    <td><strong>Biosafety Level</strong></td>
                                                    <td>{data.data["Safety information"]["risk assessment"]["biosafety level"]}</td>
                                                    <td>{data.data["Safety information"]["risk assessment"]["biosafety level comment"]}</td>
                                                </tr>
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
    )
}

export default SafetyContent