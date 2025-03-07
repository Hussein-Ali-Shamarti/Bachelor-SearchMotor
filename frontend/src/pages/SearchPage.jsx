import React, { useState, useEffect } from "react";
import "../assets/styles/SearchPage.css";
import SearchWithResults from "../components/SearchWithResults";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";
import { db, auth } from "../FirebaseConfig";
import { collection, addDoc, serverTimestamp } from "firebase/firestore";

const SearchPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const searchQuery = queryParams.get("query");
  const [user, setUser] = useState(null);

  // Sjekk om bruker er logget inn
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        setUser(user);
      } else {
        setUser(null);
      }
    });
    return () => unsubscribe();
  }, []);

  // Lagre søk i Firestore
  const saveSearch = async () => {
    if (user && searchQuery) {
      try {
        await addDoc(collection(db, "searchHistory"), {
          userId: user.uid,
          searchQuery: searchQuery,
          timestamp: serverTimestamp()
        });
        console.log("Søket er lagret i Firestore!");
      } catch (error) {
        console.error("Feil ved lagring av søk:", error);
      }
    }
  };

  // Kjør lagring når komponenten laster
  useEffect(() => {
    if (searchQuery) {
      saveSearch();
    }
  }, [searchQuery, user]);

  return (
    <div className="search-page-container">
      <Header />
      <h1>AI-Powered Search</h1>
      <SearchWithResults initialQuery={searchQuery} />
    </div>
  );
};

export default SearchPage;
