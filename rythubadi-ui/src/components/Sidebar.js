import './Sidebar.css'

function SideBar() {
    const oldChats = [
        {id: 1, title: "Chat1"},
        {id: 2, title: "Chat2"},
        {id: 3, title: "Chat3"},
    ]

    return (
        <div className="chats-container">
            <button className="new-chat">New chat</button>
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