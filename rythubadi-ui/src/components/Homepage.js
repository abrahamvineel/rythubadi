import React, { useEffect, useState } from 'react';
import ChatWindow from "./ChatWindow"
import SideBar from "./Sidebar"
import { useParams, useNavigate } from 'react-router-dom';

import './Homepage.css'

function Homepage() {
    const { chatId: chatIdFromParams } = useParams();
    const email = localStorage.getItem('email');
    const [selectedChatId, setSelectedChatId] = useState(chatIdFromParams || null)
    const navigate = useNavigate();

    useEffect(() => {
        setSelectedChatId(chatIdFromParams || null);
    }, [chatIdFromParams])

    const handleChatSelect = (chatId) => {
        setSelectedChatId(chatId);
        navigate(`/homepage/chat/${chatId}`);
    }

    const handleNewlyCreatedChat = (newChatId) => {
        setSelectedChatId(newChatId);
        navigate(`/homepage/chat/${newChatId}`);
    }

    return (
        <div class="homepage-container">
            <SideBar onChatSelect={handleChatSelect} 
                chatId={selectedChatId} email={email} 
                onNewChatCreated={handleNewlyCreatedChat}
                selectedChatId={selectedChatId}/>
            <ChatWindow chatId={selectedChatId} email={email}/>
        </div>
    );
}

export default Homepage;