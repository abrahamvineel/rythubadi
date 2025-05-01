import axios from 'axios'
import { useState, useEffect } from 'react';
import './Sidebar.css'

function SideBar({email, onChatSelect}) {
    const [oldChats, setOldChats] = useState([]);

    useEffect(() => {
        const fetchOldChats = async () => {
            try {
                const response = await axios.get(`http://localhost:8080/api/chat/user/${encodeURIComponent(email)}`)
                setOldChats(response.data);
            } catch(error) {
                console.error("Unable to fetch old chats ", error);
            }
        };

        fetchOldChats();
    }, [email]);

    const loadChatSessions = async () => {
        try {
            await axios.get(`http://localhost:8080/api/chat/user/${encodeURIComponent(email)}`)
        } catch(error) {
           console.error("Unable to load chat sessions ", error) 
        }
    }
    loadChatSessions()

    const createChatSession = async () => {

        try {
            await axios.post(`http://localhost:8080/api/chat/create/${email}`)
        } catch(error) {
           console.error("Unable to create a chat session ", error) 
        }
    }

    return (
        <div className="chats-container">
            <button className="new-chat" onClick={createChatSession}>New Chat</button>
            <div className="old-chats-container">
                <h3>Old Chats</h3>
                <ul>
                    {oldChats.map((chat) => {
                        return <li key={chat.id} onClick={() => onChatSelect(chat.id)}>{chat.title}</li>
                    })}
                </ul>
            </div>
        </div>
    )
}

export default SideBar;