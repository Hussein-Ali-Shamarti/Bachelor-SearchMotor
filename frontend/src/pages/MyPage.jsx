import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import SearchWithResults from "../components/SearchWithResults";
import Sidebar from "../components/Sidebar";
import { db, auth, app } from "../FirebaseConfig";
import { collection, query, where, getDocs, orderBy, addDoc, serverTimestamp } from "firebase/firestore";

import user from "../assets/images/user.svg";
import question from "../assets/images/question.svg";
import   "../assets/styles/MyPage.css";
import Popup from "../components/Popup";
const MyPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const [searchQuery, setSearchQuery] = useState(queryParams.get("query") || "");
  const [searchHistory, setSearchHistory] = useState([]);
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

  // Hent søkehistorikk fra Firestore når brukeren er logget inn
  useEffect(() => {
    const fetchSearchHistory = async () => {
      if (user) {
        try {
          const searchRef = collection(db, "searchHistory");
          const q = query(
            searchRef,
            where("userId", "==", user.uid),
            orderBy("timestamp", "desc")
          );
          const querySnapshot = await getDocs(q);
          const searches = querySnapshot.docs.map((doc) => ({
            searchQuery: doc.data().searchQuery,
            timestamp: new Date(doc.data().timestamp?.seconds * 1000).toLocaleString()
          }));
          setSearchHistory(searches);
        } catch (error) {
          console.error("Feil ved henting av søkehistorikk:", error);
        }
      }
    };

    fetchSearchHistory();
  }, [user]);

  // Legg til søk i Firestore og oppdater lokalt
  const addToSearchHistory = async (query) => {
    if (user) {
      try {
        const searchRef = collection(db, "searchHistory");
        await addDoc(searchRef, {
          userId: user.uid,
          searchQuery: query,
          timestamp: serverTimestamp()
        });
        setSearchHistory((prevSearchHistory) => [
          { searchQuery: query, timestamp: new Date().toLocaleString() },
          ...prevSearchHistory
        ]);
      } catch (error) {
        console.error("Feil ved lagring av søk:", error);
      }
    }
  };

  const handleSelectSearchQuery = (query) => {
    setSearchQuery(query);
  };

  return (
    <div className="mypage">
      <Header />
      <Sidebar sidebarVisible="true" searchHistory={searchHistory} handleSelectSearchQuery={handleSelectSearchQuery} />
      <main className="site-content">
        
        <SearchWithResults initialQuery={searchQuery} addToSearchHistory={addToSearchHistory} />
        <button onclick="alert('Person clicked!')" className="user-icon">
            <img src={user} alt="user Icon" width="30px" height="30px"/>
          </button>
          
          <Popup/>
      </main>
    </div>
  );
};

export default MyPage;
