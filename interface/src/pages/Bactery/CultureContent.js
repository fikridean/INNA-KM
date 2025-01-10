import React, { useState } from 'react';
import { Collapse, Table, Card } from 'react-bootstrap';
import { FaChevronDown, FaChevronRight } from 'react-icons/fa';

const CultureContent = ({ data }) => {
    const [cultureOpen, setCultureOpen] = useState(true);

    return (
        <div>
            {data.data["Culture and growth conditions"] && (
                <Card className="mb-4 shadow-sm">
                    <Card.Header
                        className="d-flex align-items-center justify-content-between"
                        style={{ backgroundColor: '#f8f9fa', cursor: 'pointer' }}
                        onClick={() => setCultureOpen(!cultureOpen)}
                    >
                        <h4 className="mb-0">Culture and Growth Conditions</h4>
                        {cultureOpen ? <FaChevronDown /> : <FaChevronRight />}
                    </Card.Header>
                    <Collapse in={cultureOpen}>
                        <div id="culture-content">
                            <Card.Body>
                                <Table striped bordered hover className="mt-3">
                                    <tbody>
                                        {data.data["Culture and growth conditions"]["culture medium"] && (
                                            Array.isArray(data.data["Culture and growth conditions"]["culture medium"]) ? (
                                                data.data["Culture and growth conditions"]["culture medium"].map((medium, index) => (
                                                    <>
                                                        <tr>
                                                            <td><strong>Culture Medium</strong>
                                                                <p>@ref {medium["@ref"]}</p>
                                                            </td>
                                                            <td>{medium["name"]}</td>
                                                        </tr>
                                                        <tr>
                                                            <td><strong>Culture Medium Growth</strong></td>
                                                            <td>{medium["growth"]}</td>
                                                        </tr>
                                                        {medium["link"] && (
                                                            <tr>
                                                                <td><strong>Culture Medium Link</strong></td>
                                                                <td><a href={medium["link"]}>{medium["link"]}</a>
                                                                </td>
                                                            </tr>
                                                        )}
                                                        {medium["composition"] && (
                                                            <tr>
                                                                <td><strong>Culture Medium composition</strong></td>
                                                                <td><pre>{medium["composition"]}</pre></td>

                                                            </tr>
                                                        )}
                                                        <br></br>
                                                    </>
                                                ))
                                            ) : (
                                                <>
                                                    <tr>
                                                        <td><strong>Culture Medium</strong>
                                                            <p>@ref {data.data["Culture and growth conditions"]["culture medium"]["@ref"]}</p>
                                                        </td>
                                                        <td>{data.data["Culture and growth conditions"]["culture medium"]["name"]}</td>
                                                    </tr>
                                                    <tr>
                                                        <td><strong>Culture Medium Growth</strong></td>
                                                        <td>{data.data["Culture and growth conditions"]["culture medium"]["growth"]}</td>
                                                    </tr>
                                                    {data.data["Culture and growth conditions"]["culture medium"]["link"] && (
                                                        <tr>
                                                            <td><strong>Culture Medium Link</strong></td>
                                                            <td><a href={data.data["Culture and growth conditions"]["culture medium"]["link"]}>{data.data["Culture and growth conditions"]["culture medium"]["link"]}</a>
                                                            </td>
                                                        </tr>
                                                    )}
                                                    {data.data["Culture and growth conditions"]["culture medium"]["composition"] && (
                                                        <tr>
                                                            <td><strong>Culture Medium composition</strong></td>
                                                            <td><pre>{data.data["Culture and growth conditions"]["culture medium"]["composition"]}</pre></td>
                                                        </tr>
                                                    )}
                                                    <br></br>
                                                </>
                                            )
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

export default CultureContent