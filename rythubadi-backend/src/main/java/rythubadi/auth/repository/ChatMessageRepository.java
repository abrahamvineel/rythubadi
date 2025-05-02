package rythubadi.auth.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import rythubadi.auth.dto.ChatMessageDTO;
import rythubadi.auth.model.ChatMessage;

import java.util.List;

public interface ChatMessageRepository extends JpaRepository<ChatMessage, Long> {
    @Query("select new rythubadi.auth.dto.ChatMessageDTO(cm.content, cm.attachmentURL, cm.type, cm.status, cm.systemGenerated) from ChatMessage cm " +
            "where cm.chatSession.id = :chatId and cm.user.id = :userId and cm.isDeleted = false")
    List<ChatMessageDTO> findMessagesByChatSessionId(@Param("chatId") String chatId, @Param("userId") long userId);
}