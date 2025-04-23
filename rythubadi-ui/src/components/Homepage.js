import ChatWindow from "./ChatWindow"
import SideBar from "./Sidebar"
import { useLocation } from 'react-router-dom';
import { useNavigate } from "react-router-dom";

import './Homepage.css'

function Homepage() {
    const location = useLocation();
    const email = location.state?.email;

    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('email');
        navigate("/")
    }
    return (
        <div class="homepage-container">
        <div className="top-right-section">
          <h3>Welcome {email || 'User'}</h3>
          <button onClick={handleLogout}>logout</button>
        </div>
            <SideBar />
            <ChatWindow />
        </div>
    );
}

export default Homepage;