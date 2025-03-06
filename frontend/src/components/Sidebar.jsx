import { useLocation } from "react-router-dom";
import LeftPil from "../assets/images/LeftPil.svg";
import Nychat from "../assets/images/Nychat.svg";
import search from "../assets/images/search.svg";

const Sidebar = ({ sidebarVisible, searchHistory, handleSelectSearchQuery }) => {


    return (
        sidebarVisible && (
            <div className="site-nav">
                
                <button onClick={() => alert('Left-pil clicked!')} className="LeftPil">
                    <img src={LeftPil} alt="LeftPil Icon" width="35px" height="35px" />
                </button>
                <button onClick={() => alert('Search in history clicked!')} className="search-icon">
                    <img src={search} alt="search Icon" width="25px" height="25px" />
                </button>
                <button onClick={() => alert('Ny chat clicked!')} className="Nychat-icon">
                    <img src={Nychat} alt="Nychat Icon" width="25px" height="25px" />
                </button>

                <div>
                    <u>SearchHistory:</u>
                    {/*TODO: group by day, and limit*/} 
                    {searchHistory.map((historyItem, index) => (
                        <div key={index} className="chat-item" onClick={() => handleSelectSearchQuery(historyItem.searchQuery)} >
                            {historyItem.timestamp} - {historyItem.searchQuery}
                        </div>
                    ))}
                </div>
            </div>
        )
    );
}

export default Sidebar;