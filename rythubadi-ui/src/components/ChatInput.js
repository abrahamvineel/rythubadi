import React, { useState } from 'react';
import axios from 'axios'
import './ChatInput.css'

function ChatInput({onNewChatCreated, email, chatId, refreshChats }) {
    const [message, setMessage] = useState('');

    const sendMessage = async () => {
        try {
            const response = await axios.post('http://localhost:8080/api/chat/message' , {
                email:email,
                chatId: chatId,
                message: message
            })

            if (response.data.chatId) {
                setMessage('');
                refreshChats();
                onNewChatCreated(response.data.chatId)
            }
        } catch(error) {
            console.log(error)
        }
    }
    return (
        <div className="chat-input">
            <textarea placeholder="Please type your message" 
                    value={message} onChange={(e) => setMessage(e.target.value)} rows={3}></textarea>
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default ChatInput;