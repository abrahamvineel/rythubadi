package rythubadi.auth.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import rythubadi.auth.dto.ChatSessionDTO;
import rythubadi.auth.model.ChatSession;
import rythubadi.auth.model.User;
import rythubadi.auth.repository.ChatSessionRepository;
import rythubadi.auth.repository.UserRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ChatService {

    private final ChatSessionRepository chatSessionRepository;
    private final UserRepository userRepository;

    @Autowired
    public ChatService(ChatSessionRepository chatSessionRepository, UserRepository userRepository) {
        this.chatSessionRepository = chatSessionRepository;
        this.userRepository = userRepository;
    }

    public void createChatSession(String email) {
        Optional<User> user = userRepository.findByEmail(email);
        ChatSession session = new ChatSession();
        session.setUser(user.get());
        session.setTitle("Chat_" + UUID.randomUUID());
        chatSessionRepository.save(session);
    }

    public List<ChatSessionDTO> getChatSessions(String email) {
        Optional<User> user = userRepository.findByEmail(email);
        long userId = user.get().getId();
        return chatSessionRepository.findAllActiveSessionsByUserId(userId);
    }
}
