import ChatWindow from "./ChatWindow"
import SideBar from "./Sidebar"
import { useLocation } from 'react-router-dom';

import './Homepage.css'

function Homepage() {
    const location = useLocation();
    const email = location.state?.email;
    return (
        <div class="homepage-container">
            <SideBar email={email}/>
            <ChatWindow email={email}/>
        </div>
    );
}

export default Homepage;