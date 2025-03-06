import { useLocation } from "react-router-dom";

const Sidebar = () => {
    let location = useLocation();
    const show = location.pathname == "/mypage";
    //TODO: get chat history from service / shared state

    // TODO: populate with chats-list (history)
    // TODO: add click handlers. Clicking a list item -> open chat

    return (
        (show &&
        <div class="site-nav"> 
            <div class="inside">
            <span class="hamburger"></span>
            <button class="menubutton" onclick="this.classList.toggle('showmenu')">Menu</button>
            <ul>
                <li><a href="template_default.html">Template-default</a></li>
                <li><a href="welcome.html">Welcome</a></li>
                <li class="current"><a href="">"?"</a></li>
                <li><a href="get_started.html">Get started /Oversikt</a></li>
                <li><a href="result_list.html">Search knapp - result_list</a></li>
                <li><a href="kontakt.html">Kontakt</a></li>
            </ul>
            </div>
        </div> )
    );
}

export default Sidebar;