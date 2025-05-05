import React, { useEffect, useState } from 'react';
import ChatWindow from "./ChatWindow"
import SideBar from "./Sidebar"
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios'

import './Homepage.css'

function Homepage() {
    const { chatId: chatIdFromParams } = useParams();
    const email = localStorage.getItem('email');
    const [selectedChatId, setSelectedChatId] = useState(chatIdFromParams || null)
    const [oldChats, setOldChats] = useState([]);
    const navigate = useNavigate();

    const fetchOldChats = async () => {
        try {
          const response = await axios.get(`http://localhost:8080/api/chat/user/${encodeURIComponent(email)}`);
          setOldChats(response.data);
        } catch (error) {
          console.error("Unable to fetch old chats ", error);
        }
    };

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
                selectedChatId={selectedChatId}
                oldChats={oldChats}
                refreshChats={fetchOldChats} 
                />
            <ChatWindow onNewChatCreated={handleNewlyCreatedChat} 
                chatId={selectedChatId} 
                email={email}
                refreshChats={fetchOldChats}/>
        </div>
    );
}

export default Homepage;