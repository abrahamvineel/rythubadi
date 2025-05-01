import ChatInput from "./ChatInput"
import { useNavigate } from "react-router-dom";
import './ChatWindow.css'

function ChatWindow({email, chatId}) {

    const messages = [
    ]

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