import ChatInput from "./ChatInput"
import './ChatWindow.css'

function ChatWindow() {

    const messages = [
        {id: 1, sender: "user", text: "Hello"},
        {id: 2, sender: "bot", text: "Hello, how can i help you?"},
    ]
    return (
        <div className="chat-window">
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