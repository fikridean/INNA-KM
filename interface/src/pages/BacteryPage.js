import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom'
import { Button, Collapse } from 'react-bootstrap';
import { getTerms, getPortalsWithWebDetail, getTaxonDetail } from '../services/api';
import { Table, Form, Container } from "react-bootstrap";

const BacteryPage = () => {
  const { bacteryName } = useParams();
  // console.log(bacteryName)
  const bacteryNameWithoutSlug = bacteryName.replace(/-/g, ' ');
  const [isLoading, setIsLoading] = useState(true);

  // kondisi untuk show dropdown
  const [open, setOpen] = useState(true);
  const [taxonomyOpen, setTaxonomyOpen] = useState(true);
  const [cultureOpen, setCultureOpen] = useState(true);
  const [physioOpen, setPhysioOpen] = useState(true);
  const [isolationOpen, setIsolationOpen] = useState(true);
  const [safetyOpen, setSafetyOpen] = useState(true);
  const [sequenceOpen, setSequenceOpen] = useState(true);
  const [genomeOpen, setGenomeOpen] = useState(true);
  const [externalOpen, setExternalOpen] = useState(true);
  const [referenceOpen, setReferenceOpen] = useState(true);

  const [dataBactery, setDataBactery] = useState([]);

  useEffect(() => {
    const fetchBookings = async () => {
      try {

        // const response = await getPortalsWithWebDetail()

        // const matchedBacterium = response.find(bacterium => bacterium.species === bacteryNameWithoutSlug);

        // if (matchedBacterium) {
        //   // Use the found taxonID to fetch the detailed data
        //   const taxonID = matchedBacterium.taxon_id;
        //   // console.log(taxonID);
        //   const data = await getTerms(taxonID)
        //   setDataBactery(data);
        //   console.log(data.data.Morphology);

        // } else {
        //   console.error('Bacterium not found');
        // }

        const taxonDetail = await getTaxonDetail(bacteryName);
        const response = await getTerms(taxonDetail.ncbi_taxon_id);
        // console.log(response);
        setDataBactery(response);


      } catch (error) {
        console.error('Failed to fetch bookings:', error);
      } finally {
        setIsLoading(false); // Setelah data selesai diambil atau ada error
      }
    };

    fetchBookings();
  }, []);


  if (isLoading) {
    return <div>Loading...</div>;
  }


  return (
    <div className='p-3'>
      <h1>{dataBactery.species}</h1>
      {/* <h1>{bacteryName}</h1> */}
      <br></br>

      <Button
        onClick={() => setTaxonomyOpen(!taxonomyOpen)}
        aria-controls="taxonomy-content"
        aria-expanded={setTaxonomyOpen}
        variant="link"
      >
        <h4>Name and taxonomic classification</h4>
      </Button>
      <Collapse in={taxonomyOpen}>
        <div id="taxonomy-content">
          <Table striped bordered hover className="mt-3">
            <tbody>
              <tr>
                <td><strong>Last LPSN update</strong></td>
                {/* <td>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[1].ScientificName}</td> */}
              </tr>
              <tr>
                <td><strong>Domain</strong></td>
                <td>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[1].ScientificName}</td>
              </tr>
              <tr>
                <td><strong>Phylum</strong></td>
                <td>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[2].ScientificName}</td>
              </tr>
              <tr>
                <td><strong>Class</strong></td>
                <td>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[3].ScientificName}</td>
              </tr>
              <tr>
                <td><strong>Order</strong></td>
                <td>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[4].ScientificName}</td>
              </tr>
              <tr>
                <td><strong>Family</strong></td>
                <td>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[5].ScientificName}</td>
              </tr>
              <tr>
                <td><strong>Genus</strong></td>
                <td>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[6].ScientificName}</td>
              </tr>
              <tr>
                <td><strong>Species</strong></td>
                <td>{dataBactery.species}</td>
              </tr>
              <tr>
                <td><strong>Full Scientific Name (LPSN)</strong></td>
                <td>{dataBactery.data["Occurence (geoference records)"].scientificName}</td>
              </tr>
            </tbody>
          </Table>

          {/* {bactery.synonym && (
            <pre>
              <strong>Synonym</strong>                       {bactery.synonym}
            </pre>
          )} */}
        </div>
      </Collapse>



      <br></br>
      {/* bagian morphology */}
      {dataBactery.data.Morphology && (
        <div>

          <Button
            onClick={() => setOpen(!open)}
            aria-controls="morphology-content"
            aria-expanded={open}
            variant="link"
          >
            <h4>Morphology</h4>
          </Button>
          <Collapse in={open}>
            <div id="morphology-content">
              <Table striped bordered hover className="mt-3">
                <tbody>
                  {dataBactery.data.Morphology["cell morphology"] && (
                    <>
                      <tr>
                        <td><strong>Gram Stain</strong></td>
                        <td>{dataBactery.data.Morphology["cell morphology"]["gram stain"]}</td>
                      </tr>
                      <tr>
                        <td><strong>Cell Shape</strong></td>
                        <td>{dataBactery.data.Morphology["cell morphology"]["cell shape"]}</td>
                      </tr>
                      <tr>
                        <td><strong>Motility</strong></td>
                        <td>{dataBactery.data.Morphology["cell morphology"]["motility"]}</td>
                      </tr>
                    </>
                  )}

                  {dataBactery.data.Morphology["colony morphology"] && (
                    <>
                      <tr>
                        <td>
                          <strong>Incubation period</strong>
                          <p>@ref {dataBactery.data.Morphology["colony morphology"][0]["@ref"]}</p>
                        </td>
                        <td>{dataBactery.data.Morphology["colony morphology"][0]["incubation period"]}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Incubation period</strong>
                          <p>@ref {dataBactery.data.Morphology["colony morphology"][1]["@ref"]}</p>
                        </td>
                        <td>{dataBactery.data.Morphology["colony morphology"][1]["incubation period"]}</td>
                      </tr>
                    </>
                  )}
                </tbody>
              </Table>





            </div>
          </Collapse>
        </div>
      )}


      {/* <br></br> */}
      <Button
        onClick={() => setCultureOpen(!cultureOpen)}
        aria-controls="culture-content"
        aria-expanded={setCultureOpen}
        variant="link"
      >
        <h4>Culture and Growth Conditions</h4>
      </Button>
      <Collapse in={cultureOpen}>
        <div id="culture-content">
          <Table striped bordered hover className="mt-3">
            <tbody>
              {dataBactery.data["Culture and growth conditions"]["culture medium"].map((medium, index) => (
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
              ))}
            </tbody>
          </Table>
        </div>
      </Collapse>


      {/* part4 */}
      <br></br>
      <Button
        onClick={() => setPhysioOpen(!physioOpen)}
        aria-controls="physio-content"
        aria-expanded={setPhysioOpen}
        variant="link"
      >
        <h4>Physiology and Metabolism</h4>
      </Button>
      <Collapse in={physioOpen}>
        <div id="physio-content">
          <Table striped bordered hover className="mt-3">
            <tbody>
              <tr>
                <td><strong>Oxygen Tolerance</strong>
                  <p>@ref {dataBactery.data["Physiology and metabolism"]["oxygen tolerance"]["@ref"]}</p>
                </td>
                <td>{dataBactery.data["Physiology and metabolism"]["oxygen tolerance"]["oxygen tolerance"]}</td>
              </tr>
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
                      {dataBactery.data["Physiology and metabolism"]["metabolite utilization"].map((metabolite, index) => (
                        <>
                          <tr>
                            <td>{metabolite.metabolite}</td>
                            <td>{metabolite["utilization activity"]}</td>
                            <td>{metabolite["kind of utilization tested"]}</td>
                          </tr>



                          {/* <tr>
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
                          <td><strong>Culture Medium Link</strong></td>
                          <td><pre>{medium["composition"]}</pre></td>

                        </tr>
                      )} */}

                          {/* <br></br> */}
                        </>
                      ))}
                    </tbody>
                  </Table>


                </td>
              </tr>
              <tr>
                <td>Metabolite production
                  <p>@ref {dataBactery.data["Physiology and metabolism"]["metabolite production"]["@ref"]}</p>
                </td>
                <td>
                  <Table striped bordered hover className="mt-3">
                    <tbody>
                      <tr>
                        <td>Metabolite</td>
                        <td>Production</td>
                      </tr>
                      <tr>
                        <td>{dataBactery.data["Physiology and metabolism"]["metabolite production"]["metabolite"]}</td>
                        <td>{dataBactery.data["Physiology and metabolism"]["metabolite production"]["production"]}</td>
                      </tr>
                    </tbody>
                  </Table>
                </td>
              </tr>
              <tr>
                <td>Physiological test
                  <p>@ref {dataBactery.data["Physiology and metabolism"]["metabolite tests"]["@ref"]}</p>
                </td>
                <td>
                  <Table striped bordered hover>
                    <tbody>
                      <tr>
                        <td>Metabolite</td>
                        <td>Indole test</td>
                      </tr>
                      <tr>
                        <td><Link to={`https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:${dataBactery.data["Physiology and metabolism"]["metabolite tests"]["Chebi-ID"]}`}>{dataBactery.data["Physiology and metabolism"]["metabolite tests"]["metabolite"]}</Link></td>
                        <td>{dataBactery.data["Physiology and metabolism"]["metabolite tests"]["indole test"]}</td>
                      </tr>
                    </tbody>
                  </Table>
                </td>
              </tr>
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
                      {dataBactery.data["Physiology and metabolism"]["enzymes"].map((enzyme, index) => (
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
            </tbody>
          </Table>
        </div>
      </Collapse>

      {/* part5 */}
      <br></br>
      <Button
        onClick={() => setIsolationOpen(!isolationOpen)}
        aria-controls="isolation-content"
        aria-expanded={setIsolationOpen}
        variant="link"
      >
        <h4>Isolation, sampling and environmental information</h4>
      </Button>
      <Collapse in={isolationOpen}>
        <div id="isolation-content">
          <Table striped bordered hover className="mt-3">
            <tbody>
              {dataBactery.data["Isolation, sampling and environmental information"]["isolation"].map((data, index) => (
                <>
                  <tr>
                    <td><strong>Sample type</strong>
                    </td>
                    <td>{data["sample type"]}</td>
                  </tr>
                  {data["sampling date"] && (
                    <tr>
                      <td><strong>Sampling date</strong></td>
                      <td>{data["sampling date"]}
                      </td>
                    </tr>
                  )}
                  <tr>
                    <td><strong>Country</strong></td>
                    <td>{data["country"]}</td>
                  </tr>
                  <tr>
                    <td><strong>Country ISO 3 Code</strong></td>
                    <td>{data["origin.country"]}</td>
                  </tr>
                  <tr>
                    <td><strong>Countinent</strong></td>
                    <td>{data["continent"]}</td>
                  </tr>
                  {data["isolation date"] && (
                    <tr>
                      <td><strong>Isolation date</strong></td>
                      <td>{data["isolation date"]}
                      </td>
                    </tr>
                  )}
                  <br></br>
                </>
              ))}

              <tr>
                <td>Isolation sources category</td>
                <td>
                  <Table striped bordered hover>
                    <tbody>
                      {dataBactery.data["Isolation, sampling and environmental information"]["isolation source categories"].map((data, index) => (
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
                            ):(
                              <>tes</>
                            )}
                          </tr>
                        </>
                      ))}

                    </tbody>
                  </Table>
                </td>
              </tr>

            </tbody>
          </Table>
        </div>
      </Collapse>


      {/* part6 */}
      {/* <h4>Name and taxonomic classification</h4> */}
      <br></br>
      {/* <Button
        onClick={() => setSafetyOpen(!safetyOpen)}
        aria-controls="safety-content"
        aria-expanded={setSafetyOpen}
        variant="link"
      >
        <h4>Safety information</h4>
      </Button>
      <Collapse in={safetyOpen}>
        <div id="safety-content">
          <pre>
            <strong>Last LPSN update</strong>              {bactery.last_update} (DD-MM-YYYY)
          </pre>
          <pre>
            <strong>Domain</strong>                        {bactery.domain}
          </pre>
          <div className='penamaan2'>
            <pre style={{ "margin-top": "-10px !important" }}>
              <strong>Phylum</strong>                        {bactery.phylum}
            </pre>
          </div>
          <pre>
            <strong>Class</strong>                         {bactery.class}
          </pre>
          <pre>
            <strong>Order</strong>                         {bactery.order}
          </pre>
          <pre>
            <strong>Family</strong>                        {bactery.family}
          </pre>
          <pre>
            <strong>Genus</strong>                         {bactery.genus}
          </pre>
          <pre>
            <strong>Species</strong>                       {bactery.species}
          </pre>
          <pre>
            <strong>Full Scientific Name (LPSN)</strong>   {bactery.lpsn}
          </pre>
          {bactery.synonym && (
            <pre>
              <strong>Synonym</strong>                       {bactery.synonym}
            </pre>
          )}
        </div>
      </Collapse> */}


      {/* part7 */}
      {/* <h4>Name and taxonomic classification</h4> */}
      <br></br>
      {/* <Button
        onClick={() => setSequenceOpen(!sequenceOpen)}
        aria-controls="sequence-content"
        aria-expanded={setSequenceOpen}
        variant="link"
      >
        <h4>Sequence information</h4>
      </Button>
      <Collapse in={sequenceOpen}>
        <div id="sequence-content">
          <pre>
            <strong>Last LPSN update</strong>              {bactery.last_update} (DD-MM-YYYY)
          </pre>
          <pre>
            <strong>Domain</strong>                        {bactery.domain}
          </pre>
          <div className='penamaan2'>
            <pre style={{ "margin-top": "-10px !important" }}>
              <strong>Phylum</strong>                        {bactery.phylum}
            </pre>
          </div>
          <pre>
            <strong>Class</strong>                         {bactery.class}
          </pre>
          <pre>
            <strong>Order</strong>                         {bactery.order}
          </pre>
          <pre>
            <strong>Family</strong>                        {bactery.family}
          </pre>
          <pre>
            <strong>Genus</strong>                         {bactery.genus}
          </pre>
          <pre>
            <strong>Species</strong>                       {bactery.species}
          </pre>
          <pre>
            <strong>Full Scientific Name (LPSN)</strong>   {bactery.lpsn}
          </pre>
          {bactery.synonym && (
            <pre>
              <strong>Synonym</strong>                       {bactery.synonym}
            </pre>
          )}
        </div>
      </Collapse> */}


      {/* part8 */}
      {/* <h4>Name and taxonomic classification</h4> */}
      <br></br>
      {/* <Button
        onClick={() => setGenomeOpen(!genomeOpen)}
        aria-controls="genome-content"
        aria-expanded={setGenomeOpen}
        variant="link"
      >
        <h4>Genome-based preditions</h4>
      </Button>
      <Collapse in={genomeOpen}>
        <div id="genome-content">
          <pre>
            <strong>Last LPSN update</strong>              {bactery.last_update} (DD-MM-YYYY)
          </pre>
          <pre>
            <strong>Domain</strong>                        {bactery.domain}
          </pre>
          <div className='penamaan2'>
            <pre style={{ "margin-top": "-10px !important" }}>
              <strong>Phylum</strong>                        {bactery.phylum}
            </pre>
          </div>
          <pre>
            <strong>Class</strong>                         {bactery.class}
          </pre>
          <pre>
            <strong>Order</strong>                         {bactery.order}
          </pre>
          <pre>
            <strong>Family</strong>                        {bactery.family}
          </pre>
          <pre>
            <strong>Genus</strong>                         {bactery.genus}
          </pre>
          <pre>
            <strong>Species</strong>                       {bactery.species}
          </pre>
          <pre>
            <strong>Full Scientific Name (LPSN)</strong>   {bactery.lpsn}
          </pre>
          {bactery.synonym && (
            <pre>
              <strong>Synonym</strong>                       {bactery.synonym}
            </pre>
          )}
        </div>
      </Collapse> */}


      {/* part9 */}
      {/* <h4>Name and taxonomic classification</h4> */}
      <br></br>
      {/* <Button
        onClick={() => setExternalOpen(!externalOpen)}
        aria-controls="external-content"
        aria-expanded={setExternalOpen}
        variant="link"
      >
        <h4>External links</h4>
      </Button>
      <Collapse in={externalOpen}>
        <div id="external-content">
          <pre>
            <strong>Last LPSN update</strong>              {bactery.last_update} (DD-MM-YYYY)
          </pre>
          <pre>
            <strong>Domain</strong>                        {bactery.domain}
          </pre>
          <div className='penamaan2'>
            <pre style={{ "margin-top": "-10px !important" }}>
              <strong>Phylum</strong>                        {bactery.phylum}
            </pre>
          </div>
          <pre>
            <strong>Class</strong>                         {bactery.class}
          </pre>
          <pre>
            <strong>Order</strong>                         {bactery.order}
          </pre>
          <pre>
            <strong>Family</strong>                        {bactery.family}
          </pre>
          <pre>
            <strong>Genus</strong>                         {bactery.genus}
          </pre>
          <pre>
            <strong>Species</strong>                       {bactery.species}
          </pre>
          <pre>
            <strong>Full Scientific Name (LPSN)</strong>   {bactery.lpsn}
          </pre>
          {bactery.synonym && (
            <pre>
              <strong>Synonym</strong>                       {bactery.synonym}
            </pre>
          )}
        </div>
      </Collapse> */}


      {/* part10 */}
      {/* <h4>Name and taxonomic classification</h4> */}
      <br></br>
      {/* <Button
        onClick={() => setReferenceOpen(!referenceOpen)}
        aria-controls="reference-content"
        aria-expanded={setReferenceOpen}
        variant="link"
      >
        <h4>References</h4>
      </Button>
      <Collapse in={referenceOpen}>
        <div id="reference-content">
          <pre>
            <strong>Last LPSN update</strong>              {bactery.last_update} (DD-MM-YYYY)
          </pre>
          <pre>
            <strong>Domain</strong>                        {bactery.domain}
          </pre>
          <div className='penamaan2'>
            <pre style={{ "margin-top": "-10px !important" }}>
              <strong>Phylum</strong>                        {bactery.phylum}
            </pre>
          </div>
          <pre>
            <strong>Class</strong>                         {bactery.class}
          </pre>
          <pre>
            <strong>Order</strong>                         {bactery.order}
          </pre>
          <pre>
            <strong>Family</strong>                        {bactery.family}
          </pre>
          <pre>
            <strong>Genus</strong>                         {bactery.genus}
          </pre>
          <pre>
            <strong>Species</strong>                       {bactery.species}
          </pre>
          <pre>
            <strong>Full Scientific Name (LPSN)</strong>   {bactery.lpsn}
          </pre>
          {bactery.synonym && (
            <pre>
              <strong>Synonym</strong>                       {bactery.synonym}
            </pre>
          )}
        </div>
      </Collapse> */}


    </div>
  );
};

export default BacteryPage;
