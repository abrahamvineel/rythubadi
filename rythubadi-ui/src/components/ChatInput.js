import React, { useState, useRef } from 'react';
import axios from 'axios'
import './ChatInput.css'

function ChatInput({chatId, onSendMessage }) {
    const [message, setMessage] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);
    const fileInputRef = useRef(null)
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
        const token = localStorage.getItem("jwt");
        const metadata = {
            userEmail: storedEmail,
            fileSizeInBytes: selectedFile.size,
            fileType: selectedFile.type,
            chatId: chatId
        }

        formData.append('metadata', JSON.stringify(metadata));

        try {
            const response = await axios.post("http://localhost:8080/api/chat/files/upload",
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

    const triggerFileInput = () => {
        fileInputRef.current.click(); 
    };

    return (
        <div className="chat-input">
            <textarea placeholder="Please type your message" 
                    value={message} onChange={(e) => setMessage(e.target.value)}></textarea>
            <button onClick={sendMessage}>Send</button>
            <div className="file-container">
                <input type="file" style={{ display: 'none' }} onChange={handleFileChange} ref={fileInputRef}/>
                <button className="attach-files" onClick={triggerFileInput}>Attach Files</button>
                <button className="upload" onClick={handleUpload}>Upload</button>
            </div>
        </div>

        
    );
}

export default ChatInput;