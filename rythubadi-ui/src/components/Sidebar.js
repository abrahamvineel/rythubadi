import axios from 'axios'
import './Sidebar.css'

function SideBar({email}) {

    const oldChats = [
    ]

    const createChatSession = async () => {

        try {
            await axios.post(`http://localhost:8080/api/chat/create/${email}`)
        } catch(error) {
           console.error("Unable to create a chat session ", error) 
        }
    }

    return (
        <div className="chats-container">
            <button className="new-chat" onClick={createChatSession}>New Chat</button>
            <div className="old=chats-container">
                <h3>Old Chats</h3>
                <ul>
                    {oldChats.map((chat) => {
                        return <li key={chat.id}>{chat.title}</li>
                    })}
                </ul>
            </div>
        </div>
    )
}

export default SideBar;