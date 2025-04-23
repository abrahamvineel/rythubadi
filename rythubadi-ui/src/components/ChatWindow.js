import ChatInput from "./ChatInput"
import { useNavigate } from "react-router-dom";
import './ChatWindow.css'

function ChatWindow({email}) {

    const messages = [
        {id: 1, sender: "user", text: "Hello"},
        {id: 2, sender: "bot", text: "Hello, how can i help you?"},
    ]

    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
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