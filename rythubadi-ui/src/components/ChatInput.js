import React, { useState } from 'react';
import axios from 'axios'
import './ChatInput.css'

function ChatInput({onSendMessage }) {
    const [message, setMessage] = useState('');

    const sendMessage = () => {
        if(message.trim()) {
            onSendMessage(message);
            setMessage('')
        }
    }

    return (
        <div className="chat-input">
            <textarea placeholder="Please type your message" 
                    value={message} onChange={(e) => setMessage(e.target.value)}></textarea>
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default ChatInput;