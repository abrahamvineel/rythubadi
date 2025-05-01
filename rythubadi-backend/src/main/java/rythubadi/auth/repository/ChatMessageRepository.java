package rythubadi.auth.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import rythubadi.auth.model.ChatMessage;

import java.util.List;

public interface ChatMessageRepository extends JpaRepository<ChatMessage, Long> {
    List<ChatMessage> findMessagesByChatSessionId(String chatId);
}
