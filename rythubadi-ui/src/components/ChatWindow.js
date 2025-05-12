import ChatInput from "./ChatInput"
import axios from 'axios'
import { useNavigate } from "react-router-dom";
import { useState, useEffect, useCallback  } from 'react';
import './ChatWindow.css'

function ChatWindow({onNewChatCreated, email, chatId, refreshChats }) {

    const [messages, setMessages] = useState([]);

    const fetchMessages = useCallback (async () => {
        if(chatId) {
            try {
                const response = await axios.get(`http://localhost:8080/api/chat/user/${encodeURIComponent(chatId)}/${encodeURIComponent(email)}/messages`)
                setMessages(response.data);
            } catch(error) {
                console.error("Unable to fetch old chats ", error);
            }
        } else {
            setMessages([]);
        }
    }, [chatId, email]);

    const sendMessage = async (message) => {
        try {
            const response = await axios.post('http://localhost:8080/api/chat/message' , {
                email:email,
                chatId: chatId,
                message: message
            })

            if (response.data.chatId) {
                refreshChats();
                onNewChatCreated(response.data.chatId)
            }

            if (response.status === 200) {
                fetchMessages()
            }
        } catch(error) {
            console.log(error)
        }
    }

    useEffect(() => {
        fetchMessages();
    }, [chatId, email, fetchMessages])

    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('email');
        navigate("/")
    }

    const handleFileUploadSuccess = () => {
        fetchMessages();
    };

    return (
        <div className="chat-window">
        <div className="top-right-section">
           <h3>Rythubadi</h3>
          <h3>Welcome {email}</h3>
          <button onClick={handleLogout}>logout</button>
        </div>
            <div className="chat-messages">
                {messages.map((message) => {
                                       return <div className="chat-message" key={message.id}> 
                        <div className={`chat-message ${message.systemGenerated}`}>
                            <p>{message.content}</p>
                            {message.attachmentURL && (
                                message.type === 'IMAGE' ? (
                                    <img src={message.attachmentURL} alt="Attachment" style={{ maxWidth: '200px', maxHeight: '200px' }} />
                                ) : (
                                        <a href={message.attachmentURL} target="_blank" rel="noopener noreferrer">
                                        View Attachment
                                        </a>
                                    )
                                )}
                        </div>
                    </div>
                })}
            </div>
            <ChatInput chatId={chatId} 
                        onSendMessage={sendMessage}
                        onFileUploadSuccess={handleFileUploadSuccess}/>
        </div>
    )
}

export default ChatWindow;