import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom'
import { Button, Collapse } from 'react-bootstrap';
import { getTerms, getPortalsWithWebDetail } from '../services/api';

const BacteryPage = () => {
  const { bacteryName } = useParams();
  const species = bacteryName.replace(/-/g, ' ');
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
        
        const response = await getPortalsWithWebDetail()

        const matchedBacterium = response.find(bacterium => bacterium.species === species);
        
        if (matchedBacterium) {
          // Use the found taxonID to fetch the detailed data
          const taxonID = matchedBacterium.taxon_id;
          // console.log(taxonID);
          const data = await getTerms(taxonID)
          setDataBactery(data);
          console.log(data.data.Morphology);

        } else {
          console.error('Bacterium not found');
        }
        
        
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
          <pre>
            <strong>Last LPSN update</strong>              
            {/* {bactery.last_update} (DD-MM-YYYY) */}
          </pre>
          <pre>
            <strong>Domain</strong>                        {dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[1].ScientificName}
          </pre>
          <div className='penamaan2'>
            <pre style={{ "marginTop": "-10px !important" }}>
              <strong>Phylum</strong>                        {dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[2].ScientificName}
            </pre>
          </div>
          <pre>
            <strong>Class</strong>                         {dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[3].ScientificName}
          </pre>
          <pre>
            <strong>Order</strong>                         {dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[4].ScientificName}
          </pre>
          <pre>
            <strong>Family</strong>                        {dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[5].ScientificName}
          </pre>
          <pre>
            <strong>Genus</strong>                         {dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[6] && (<>{dataBactery.data["Name and taxonomic classification"].LineageEx.Taxon[6].ScientificName}</>)}
          </pre>
          <pre>
            <strong>Species</strong>                       {dataBactery.species}
          </pre>
          <pre>
            <strong>Full Scientific Name (LPSN)</strong>   {dataBactery.data["Occurence (geoference records)"].scientificName}
          </pre>
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
              <pre>
                <strong>Gram stain</strong>                    {dataBactery.data.Morphology["cell morphology"]["gram stain"]}
              </pre>
              {/* <pre>
                <strong>Gram stain</strong> {bactery.morphology.gram_stain2}{' '}
                <strong>Confidence in %</strong> {bactery.morphology.confidence}
              </pre> */}
              <pre>
                <strong>Cell shape</strong>                    {dataBactery.data.Morphology["cell morphology"]["cell shape"]}
              </pre>
              <pre>
                <strong>Motility</strong>                      {dataBactery.data.Morphology["cell morphology"]["motility"]}
              </pre>
              <pre>
                <strong>Incubation period</strong>             {dataBactery.data.Morphology["colony morphology"][0]["incubation period"]}
                <br></br>
                <span>@ref {dataBactery.data.Morphology["colony morphology"][0]["@ref"]}</span>
              </pre>
              <pre>
                <strong>Incubation period</strong>             {dataBactery.data.Morphology["colony morphology"][1]["incubation period"]}
                <br></br>
                <span>@ref {dataBactery.data.Morphology["colony morphology"][1]["@ref"]}</span>
              </pre>
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
          <pre>
            <strong>Culture Medium</strong>                {dataBactery.data["Culture and growth conditions"]["culture medium"][0]["name"]}
          </pre>
          <pre>
            <strong>Culture Medium Growth</strong>         {dataBactery.data["Culture and growth conditions"]["culture medium"][0]["growth"]}
          </pre>
          <pre>
            <strong>Culture Medium Link</strong>           <a href={dataBactery.data["Culture and growth conditions"]["culture medium"][0]["link"]}>{dataBactery.data["Culture and growth conditions"]["culture medium"][0]["link"]}</a>
          </pre>
          <pre>
            <strong>Culture Medium Composition</strong>    {dataBactery.data["Culture and growth conditions"]["culture medium"][0]["composition"]}
          </pre>
          <pre>
            <strong>Culture Medium</strong>                {dataBactery.data["Culture and growth conditions"]["culture medium"][1]["name"]}
          </pre>
          <pre>
            <strong>Culture Medium Growth</strong>         {dataBactery.data["Culture and growth conditions"]["culture medium"][1]["growth"]}
          </pre>
          <pre>
            <strong>Culture Medium Link</strong>           <a href={dataBactery.data["Culture and growth conditions"]["culture medium"][1]["link"]}>{dataBactery.data["Culture and growth conditions"]["culture medium"][1]["link"]}</a>
          </pre>
          {/* <pre>
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
          )} */}
        </div>
      </Collapse>


      {/* part4 */}
      {/* <h4>Name and taxonomic classification</h4> */}
      <br></br>
      {/* <Button
        onClick={() => setPhysioOpen(!physioOpen)}
        aria-controls="physio-content"
        aria-expanded={setPhysioOpen}
        variant="link"
      >
        <h4>Physiology and Metabolism</h4>
      </Button>
      <Collapse in={physioOpen}>
        <div id="physio-content">
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

      {/* part5 */}
      {/* <h4>Name and taxonomic classification</h4> */}
      <br></br>
      {/* <Button
        onClick={() => setIsolationOpen(!isolationOpen)}
        aria-controls="isolation-content"
        aria-expanded={setIsolationOpen}
        variant="link"
      >
        <h4>Isolation, sampling and environmental information</h4>
      </Button>
      <Collapse in={isolationOpen}>
        <div id="isolation-content">
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
