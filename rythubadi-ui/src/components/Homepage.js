import React, { useState } from 'react';
import ChatWindow from "./ChatWindow"
import SideBar from "./Sidebar"
import { useLocation } from 'react-router-dom';

import './Homepage.css'

function Homepage() {
    const location = useLocation();
    const email = location.state?.email;
    const [selectedChatId, setSelectedChatId] = useState(null)

    const handleChatSelect = (chatId) => {
        console.log('handleChatSelect ', chatId)
        setSelectedChatId(chatId);
    }
    return (
        <div class="homepage-container">
            <SideBar onChatSelect={handleChatSelect} chatId={selectedChatId} email={email}/>
            <ChatWindow chatId={selectedChatId} email={email}/>
        </div>
    );
}

export default Homepage;