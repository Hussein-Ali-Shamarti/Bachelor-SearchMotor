import react from "react";
import SearchBar from "./SearchBar";
import SearchHistory from "./SearchHistory";
import user from "../../assets/images/user.svg";
import question from "../../assets/images/question.svg";
import "../../assets/styles/MyPageF/MyPage.css";


const MyPage =() =>{

  return(
    <div className="main-container">

        <SearchHistory/>

        <div className="main-content">
          <h2>Logo</h2>
          <SearchBar/>
          <button onclick="alert('Person clicked!')" className="user-icon">
            <img src={user} alt="user Icon" width="30px" height="30px"/>
          </button>
          <button onclick="alert('Question clicked!')" className="question-icon">
            <img src={question} alt="question Icon" width="25px" height="25px"/>
          </button>
        </div>

    </div>
  );

};
export default MyPage;