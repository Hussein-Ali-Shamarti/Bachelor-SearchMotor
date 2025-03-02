import react from "react";
import LeftPil from "../../Pictures-icones/LeftPil.svg";
import search from "../../Pictures-icones/search.svg";
import Nychat from "../../Pictures-icones/Nychat.svg";
import "../../styles/MyPageF/SearchHistory.css"


const SearchHistory = () => {

  return(

    <div className="sidebar">
      
      <button onclick="alert('Left-pil clicked!')" className="LeftPil">
        <img src={LeftPil} alt="LeftPil Icon" width="35px" height="35px"/>
      </button>
      <button onclick="alert('Search in history clicked!')" className="search">
        <img src={search} alt="search Icon" width="25px" height="25px"/>
      </button>
      <button onclick="alert('Ny chat clicked!')" className="Nychat">
        <img src={Nychat} alt="Nychat Icon" width="25px" height="25px"/>
      </button>
      
      
    </div>

  );

};
export default SearchHistory;