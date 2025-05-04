import axios from 'axios'
import { useState, useEffect } from 'react';
import './Sidebar.css'

function SideBar({email, onChatSelect, onNewChatCreated, selectedChatId }) {
    const [oldChats, setOldChats] = useState([]);

    const fetchOldChats = async () => {
        try {
          const response = await axios.get(`http://localhost:8080/api/chat/user/${encodeURIComponent(email)}`);
          setOldChats(response.data);
        } catch (error) {
          console.error("Unable to fetch old chats ", error);
        }
      };

    useEffect(() => {
        fetchOldChats();
      }, [email]);

    const createChatSession = async () => {

        try {
            const response = await axios.post(`http://localhost:8080/api/chat/create/${email}`)
            console.log('resp ', response);
            if(response.data && response.data.chatId) {
                onNewChatCreated(response.data.chatId);
                fetchOldChats();
            }
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
                        return <li key={chat.id} onClick={() => onChatSelect(chat.id)}
                        className={chat.id === selectedChatId ? 'selected' : ''}>{chat.title}</li>
                    })}
                </ul>
            </div>
        </div>
    )
}

export default SideBar;