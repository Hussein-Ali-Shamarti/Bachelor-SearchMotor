import react from react;
import SearchBar from "./SearchBar";
import SearchHistory from "./SearchHistory";
import user1 from "../../Pictures-icones/user1.svg";
import question from "../../Pictures-icones/question.svg";


const MyPage =() =>{

  return(
    <div className="main-container">

        <SearchHistory/>

        <div className="main-content">
          <h2>Logo</h2>
          <SearchBar/>
          <button onclick="alert('Person clicked!')" className="user-icon">
            <img src={user1} alt="user Icon" width="30px" height="30px"/>
          </button>
          <button onclick="alert('Question clicked!')" className="question-icon">
            <img src={question} alt="question Icon" width="25px" height="25px"/>
          </button>
        </div>

    </div>
  );

};
export default MyPage;