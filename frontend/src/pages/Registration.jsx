//KODE MAL FRONTEND


// Importerer nødvendige React-funksjoner og andre verktøy
import React, { useState, useEffect } from 'react'; 
import './YourStylesheet.css'; // Importer din egen stilarkfil her (hvis aktuelt)

// Hovedkomponenten
const Registration = () => {
  // Bruker state for å lagre og oppdatere data
  const [stateVariable, setStateVariable] = useState("Initial Value");

  // Bruker useEffect for å kjøre kode ved spesifikke hendelser
  useEffect(() => {
    console.log("Komponenten er montert eller oppdatert!");
    // Legg til eventuelle logikker her
  }, [stateVariable]); // Kjør når stateVariable oppdateres

  // En funksjon som kan brukes for spesifikke interaksjoner
  const handleButtonClick = () => {
    setStateVariable("Ny verdi");
  };

  // Returnerer HTML-lignende JSX som definerer hvordan komponenten ser ut
  return (
    <div className="my-component-container">
      <h1>Min React-komponent</h1>
      <p>Verdien av stateVariable er: {stateVariable}</p>
      <button onClick={handleButtonClick}>Trykk på meg</button>
    </div>
  );
};

// Eksporterer komponenten for bruk i andre filer
export default Registration;
