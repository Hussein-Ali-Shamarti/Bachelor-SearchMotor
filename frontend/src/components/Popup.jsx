import React, {useState} from "react";
import questionIcon from "../assets/images/question.svg";
import "../assets/styles/Popup.css";

const Popup = () =>{

    const [isOpen, setIsOpen] = useState(false);

    return(

        <div className="popup-conteiner">
            <button onClick={() => setIsOpen(true)} className="icon-button">
            <img src={questionIcon} alt="Question Icon" className="questionIcon" />
            </button>

            {isOpen && (
              <div className="popup-overlay">
                <div className="popup-content">
                  <h2>Popup-vindu</h2>
                  <p>Her er litt info i popup-vinduet!</p>
                  <button onClick={() => setIsOpen(false)} className="close-button">
                    Lukk
                  </button>
                </div>
              </div>
            )}
        </div>

    );

};

export default Popup;
