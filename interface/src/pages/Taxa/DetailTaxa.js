import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Table, Button, Pagination } from "react-bootstrap";
import { getTaxonDetail, getPortalDetail, getRaws, deleteRaws, storeRaws, getTerms, deleteTerms, storeTerms, deletePortal, createPortal } from '../../services/api';

const DetailTaxa = () => {
    const { id } = useParams();
    const [dataTaxa, setDataTaxa] = useState([]);
    const [dataPortal, setDataPortal] = useState([]);
    const [dataRaw, setDataRaw] = useState([]);
    const [dataTerm, setDataTerm] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const responseTaxa = await getTaxonDetail(id);
                setDataTaxa(responseTaxa.data);
                const responsePortal = await getPortalDetail(id);
                setDataPortal(responsePortal.data);
                const responseRaw = await getRaws(responseTaxa.data.ncbi_taxon_id);
                setDataRaw(responseRaw);
                const responseTerm = await getTerms(responseTaxa.data.ncbi_taxon_id);
                setDataTerm(responseTerm);
                // console.log(responseTerm.data)
            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
        };
        fetchData();
    }, []);

    const handleDelete = async (ncbi_taxon_id) => {
        try {
            await deleteRaws(ncbi_taxon_id);
            window.location.reload(); // Refresh the page after successful deletion
        } catch (err) {
            console.error('Failed to delete taxa:', err);
        }
    };

    const handleDeleteTerm = async (ncbi_taxon_id) => {
        try {
            await deleteTerms(ncbi_taxon_id);
            window.location.reload(); // Refresh the page after successful deletion
        } catch (err) {
            console.error('Failed to delete taxa:', err);
        }
    };

    const handleDeletePortal = async (taxon_id) => {
        try {
            await deletePortal(taxon_id);
            window.location.reload(); // Refresh the page after successful deletion
        } catch (err) {
            console.error('Failed to delete taxa:', err);
        }
    };

    const handleCreate = async (ncbi_taxon_id) => {
        try {
            await storeRaws(ncbi_taxon_id);
            window.location.reload(); // Refresh the page after successful deletion
        } catch (err) {
            console.error('Failed to delete taxa:', err);
        }
    };

    const handleCreateTerm = async (ncbi_taxon_id) => {
        try {
            await storeTerms(ncbi_taxon_id);
            window.location.reload(); // Refresh the page after successful deletion
        } catch (err) {
            console.error('Failed to delete taxa:', err);
        }
    };

    const handleCreatePortal = async (taxon_id) => {
        try {
            await createPortal(taxon_id);
            window.location.reload(); // Refresh the page after successful deletion
        } catch (err) {
            console.error('Failed to delete taxa:', err);
        }
    };

    return (
        <div className='mt-3'>
            {/* <h1>{id}</h1> */}
            <h4>Detail Taxa</h4>
            <div id="taxonomy-content">
                <Table striped bordered hover className="mt-3">
                    <thead>
                        <tr>
                            <th>Taxon id</th>
                            <th>NCBI Taxon id</th>
                            <th>Species</th>
                        </tr>
                    </thead>
                    <tbody>
                        {dataTaxa.ncbi_taxon_id !== null ? (
                            <tr>
                                <td>{dataTaxa.taxon_id}</td>
                                <td>{dataTaxa.ncbi_taxon_id}</td>
                                <td>{dataTaxa.species}</td>
                            </tr>
                        ) : (
                            <tr>
                                <td colSpan="3" className="text-center">
                                    No results found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </Table>
            </div>

            <h4>Detail Portal</h4>
            <div id="taxonomy-content">
                {dataPortal.taxon_id !== null ? (
                    <>
                        <Button variant="danger" onClick={() => handleDeletePortal(dataTaxa.taxon_id)}>Delete Portal</Button>
                    </>
                ) : (
                    <>
                        <Button variant="primary" onClick={() => handleCreatePortal(dataTaxa.taxon_id)}>Create Portal</Button>
                    </>
                )}
                <Table striped bordered hover className="mt-3">
                    <thead>
                        <tr>
                            <th>Taxon id</th>
                            <th>Portal id</th>
                            <th>Web</th>
                        </tr>
                    </thead>
                    <tbody>
                        {dataPortal.taxon_id !== null ? (
                            <tr>
                                <td>{dataPortal.taxon_id}</td>
                                <td>{dataPortal.portal_id}</td>
                                <td>
                                    {dataPortal.web && (
                                        <>
                                            {dataPortal.web.map((data_web, index) => (
                                                <>
                                                    <p>{data_web}</p>
                                                </>
                                            ))}
                                        </>
                                    )}
                                </td>
                            </tr>
                        ) : (
                            <tr>
                                <td colSpan="3" className="text-center">
                                    No results found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </Table>
            </div>

            <h4>Detail Raws</h4>
            <div id="taxonomy-content">
                {Array.isArray(dataRaw.data) ? (
                    <>
                        {dataRaw.data[0].web !== null ? (
                            <>
                                {dataRaw.data[0].data !== null ? (
                                    <>
                                        <Button variant="danger" onClick={() => handleDelete(dataTaxa.ncbi_taxon_id)}>Delete</Button>
                                    </>
                                ) : (
                                    <>
                                        <Button variant="primary" onClick={() => handleCreate(dataTaxa.ncbi_taxon_id)}>Create Raw</Button>
                                    </>
                                )}
                            </>
                        ) : (
                            <>
                                {/* <Link to={`/raws/create`} className="btn btn-primary">
                                    Create Raw
                                </Link> */}
                                <Button variant="primary" onClick={() => handleCreate(dataTaxa.ncbi_taxon_id)}>Create Raw</Button>
                            </>
                        )}
                    </>
                ) : (
                    <>
                    </>
                )}
                <Table striped bordered hover className="mt-3">
                    <thead>
                        <tr>
                            <th>Website</th>
                            <th>Species</th>
                            <th>Data</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(dataRaw.data) ? (
                            <>
                                {dataRaw.data[0].web !== null ? (
                                    <>
                                        {dataRaw.data.map((data_web, index) => (
                                            <>
                                                <tr>
                                                    <td>{data_web.web}</td>
                                                    <td>{data_web.species}</td>
                                                    {dataRaw.data[0].data !== null ? (
                                                        <>
                                                            <td>{
                                                                Object.keys(data_web.data).length === 0
                                                                    ? "Isi data kosong"
                                                                    : JSON.stringify(data_web.data, null, 2) // Display data if not empty
                                                            }</td>
                                                        </>
                                                    ) : (
                                                        <>
                                                            <td className="text-center">
                                                                No Data. Please Create
                                                            </td>
                                                        </>
                                                    )}
                                                </tr>
                                            </>
                                        ))}
                                    </>
                                ) : (
                                    <>
                                        <tr>
                                            <td colSpan="3" className="text-center">
                                                No results found
                                            </td>
                                        </tr>
                                    </>
                                )}
                            </>
                        ) : (
                            <>
                            </>
                        )}
                    </tbody>
                </Table>
            </div>

            <h4>Detail Terms</h4>
            <div id="taxonomy-content">
                {Array.isArray(dataTerm.data) ? (
                    <>
                    </>
                ) : (
                    <>
                        {dataTerm.data !== null ? (
                            <>
                                <Button variant="danger" onClick={() => handleDeleteTerm(dataTaxa.ncbi_taxon_id)}>Delete Terms</Button>
                            </>
                        ) : (
                            <>
                                <Button variant="primary" onClick={() => handleCreateTerm(dataTaxa.ncbi_taxon_id)}>Create Terms</Button>
                            </>
                        )}
                    </>
                )}
                <Table striped bordered hover className="mt-3">
                    <thead>
                        <tr>
                            <th>Data</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Array.isArray(dataTerm.data) ? (
                            <>
                                a
                            </>
                        ) : (
                            <tr>
                                <td>{
                                    JSON.stringify(dataTerm, null, 2) // Display data if not empty
                                }</td>
                            </tr>
                        )}
                    </tbody>
                </Table>
            </div>


        </div >
    )
}

export default DetailTaxa