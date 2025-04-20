import './ChatInput.css'

function ChatInput() {
    return (
        <div className="chat-input">
            <input type="text" placeholder="Please type your message"></input>
            <button>Send</button>
        </div>
    );
}

export default ChatInput;