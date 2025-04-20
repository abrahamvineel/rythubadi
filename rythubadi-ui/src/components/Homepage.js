import ChatWindow from "./ChatWindow"
import SideBar from "./Sidebar"

import './Homepage.css'

function Homepage() {
    return (
        <div class="homepage-container">
            <SideBar />
            <ChatWindow />
        </div>
    );
}

export default Homepage;