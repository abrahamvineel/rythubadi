package rythubadi.auth.repository;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.query.Param;
import rythubadi.auth.dto.ChatSessionDTO;
import rythubadi.auth.model.ChatSession;

import java.util.UUID;
import java.util.List;

public interface ChatSessionRepository extends JpaRepository<ChatSession, UUID> {

    @Query("select new rythubadi.auth.dto.ChatSessionDTO(cs.id, cs.title) from ChatSession cs where cs.user.id = :userId AND cs.isDeleted = false")
    List<ChatSessionDTO> findAllActiveSessionsByUserId(@Param("userId") long userId);
}
