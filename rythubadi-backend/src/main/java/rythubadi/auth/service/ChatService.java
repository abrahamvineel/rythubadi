package rythubadi.auth.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import rythubadi.auth.dto.ChatMessageDTO;
import rythubadi.auth.dto.ChatSessionDTO;
import rythubadi.auth.dto.MessageDetailsRequest;
import rythubadi.auth.dto.NewChatSessionDTO;
import rythubadi.auth.model.ChatMessage;
import rythubadi.auth.model.ChatSession;
import rythubadi.auth.model.User;
import rythubadi.auth.repository.ChatMessageRepository;
import rythubadi.auth.repository.ChatSessionRepository;
import rythubadi.auth.repository.UserRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ChatService {

    private final ChatSessionRepository chatSessionRepository;
    private final UserRepository userRepository;
    private final ChatMessageRepository chatMessageRepository;

    @Autowired
    public ChatService(ChatSessionRepository chatSessionRepository,
                       UserRepository userRepository,
                       ChatMessageRepository chatMessageRepository) {
        this.chatSessionRepository = chatSessionRepository;
        this.userRepository = userRepository;
        this.chatMessageRepository = chatMessageRepository;
    }

    public NewChatSessionDTO createChatSession(String email) {
        Optional<User> user = userRepository.findByEmail(email);
        ChatSession session = new ChatSession();
        session.setUser(user.get());
        session.setTitle("Chat_" + UUID.randomUUID());
        ChatSession currentSession = chatSessionRepository.save(session);
        return new NewChatSessionDTO(currentSession.getId());
    }

    public List<ChatSessionDTO> getChatSessions(String email) {
        Optional<User> user = userRepository.findByEmail(email);
        long userId = user.get().getId();
        return chatSessionRepository.findAllActiveSessionsByUserId(userId);
    }

    public List<ChatMessageDTO> getMessagesForChatSession(String chatId, String email) {
        Optional<User> user = userRepository.findByEmail(email);
        long userId = user.get().getId();
        UUID chatUUID = UUID.fromString(chatId);
        return chatMessageRepository.findMessagesByChatSessionId(chatUUID, userId);
    }

    public NewChatSessionDTO saveMessage(MessageDetailsRequest request) {
        UUID chatUUID;
        NewChatSessionDTO newChatSession = null;
        if(request.getChatId() == null) {
            newChatSession = createChatSession(request.getEmail());
            chatUUID = newChatSession.getChatId();
        } else {
            chatUUID = UUID.fromString(request.getChatId());
        }

        Optional<ChatSession> session = chatSessionRepository.findById(chatUUID);
        Optional<User> user = userRepository.findByEmail(request.getEmail());
        ChatMessage message = new ChatMessage();
        message.setChatSession(session.get());
        message.setUser(user.get());
        message.setContent(request.getMessage());
        chatMessageRepository.save(message);
        return newChatSession;
    }
}
