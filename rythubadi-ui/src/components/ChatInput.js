import React, { useState } from 'react';
import axios from 'axios'
import './ChatInput.css'

function ChatInput({chatId, onSendMessage }) {
    const [message, setMessage] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);

    const sendMessage = () => {
        if(message.trim()) {
            onSendMessage(message);
            setMessage('')
        }
    }

    const handleUpload = async () => {
        if (!selectedFile) {
        alert("please select file");
        return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);
        const storedEmail = localStorage.getItem("email");
        const parsedEmail = JSON.parse(storedEmail);
        const token = localStorage.getItem("jwt");
        const metadata = {
            userEmail: parsedEmail.email,
            fileSizeInBytes: selectedFile.size,
            fileType: selectedFile.type,
            chatId: chatId
        }

        formData.append('metadata', JSON.stringify(metadata));

        try {
            const response = await axios.post("http://localhost:8081/files/upload",
            formData, {
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "multipart/form-data",
                }
            })
            if (response.status === 401) {
                throw new Error("Unauthorized: Invalid session");
            }
            else if (!response.ok) {
                throw new Error("Failed to fetch files");
            }
            alert("file uploaded successfully");
            setSelectedFile(null);
        }  catch(error) {
            console.error("upload failed", error);
            }
    }

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };


    return (
        <div className="chat-input">
            <textarea placeholder="Please type your message" 
                    value={message} onChange={(e) => setMessage(e.target.value)}></textarea>
            <button onClick={sendMessage}>Send</button>
            <div className="file-container">
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleUpload}>Upload</button>
            </div>
        </div>

        
    );
}

export default ChatInput;