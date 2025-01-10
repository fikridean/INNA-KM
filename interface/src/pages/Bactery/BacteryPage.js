import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getTerms, getTaxa } from '../../services/api';
import TaxonomyContent from './TaxonomyContent';
import MorphologyContent from './MorphologyContent';
import CultureContent from './CultureContent';
import PhysiologyContent from './PhysiologyContent';
import IsolationContent from './IsolationContent';
import SafetyContent from './SafetyContent';
import SequenceContent from './SequenceContent';
import './BacteryPage.css'; // Import file CSS

const BacteryPage = () => {
  const { bacteryName } = useParams();
  const bacteryNameWithoutSlug = bacteryName.replace(/-/g, ' ');
  const [isLoading, setIsLoading] = useState(true);
  const [dataBactery, setDataBactery] = useState([]);

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const listbactery = await getTaxa();
        const matchedBacterium = listbactery.data.find(
          (bacterium) => bacterium.species === bacteryNameWithoutSlug
        );
        if (matchedBacterium) {
          const ncbiTaxonId = matchedBacterium.ncbi_taxon_id;
          const data = await getTerms(ncbiTaxonId);
          setDataBactery(data);
        } else {
          console.error('Bacterium not found');
        }
      } catch (error) {
        console.error('Failed to fetch bookings:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBookings();
  });

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="page-container">
      <h1 className="page-title">{dataBactery.species}</h1>

      <TaxonomyContent data={dataBactery} />
      <MorphologyContent data={dataBactery} />
      <CultureContent data={dataBactery} />
      <PhysiologyContent data={dataBactery} />
      <IsolationContent data={dataBactery} />
      <SafetyContent data={dataBactery} />
      <SequenceContent data={dataBactery} />
    </div>
  );
};

export default BacteryPage;
