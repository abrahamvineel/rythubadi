package rythubadi.auth.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import rythubadi.auth.model.ChatSession;

import java.util.UUID;

public interface ChatSessionRepository extends JpaRepository<ChatSession, UUID> {
}
