import ChatInput from "./ChatInput"
import axios from 'axios'
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from 'react';
import './ChatWindow.css'

function ChatWindow({email, chatId}) {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get(`http://localhost:8080/api/chat/user/${encodeURIComponent(chatId)}/${encodeURIComponent(email)}/messages`)
                setMessages(response.data);
            } catch(error) {
                console.error("Unable to fetch old chats ", error);
            }
        }
        fetchMessages();
    }, [messages])
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('email');
        navigate("/")
    }

    return (
        <div className="chat-window">
        <div className="top-right-section">
          <h3>Welcome {email}</h3>
          <button onClick={handleLogout}>logout</button>
        </div>
            <div className="chat-messages">
                {messages.map((message) => {
                   return <div className="chat-message"> 
                        <div className={`chat-message ${message.sender}`}>
                            <p>{message.text}</p>
                        </div>
                    </div>
                })}
            </div>
        <ChatInput />
        </div>
    )
}

export default ChatWindow;