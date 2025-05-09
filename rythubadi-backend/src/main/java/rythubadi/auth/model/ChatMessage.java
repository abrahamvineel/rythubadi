package rythubadi.auth.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Data
public class ChatMessage {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "chat_session_id")
    private ChatSession chatSession;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sender_id")
    private User user;

    private String content;

    @Column(length = 512)
    private String attachmentURL;

    private AttachmentType type;

    private MessageStatus status;

    private String language;

    private boolean systemGenerated = false;

    private boolean isEdited = false;

    private boolean isArchived = false;

    private boolean isDeleted = false;

    @Column(columnDefinition = "TIMESTAMP")
    private LocalDateTime editedAt;

    @Column(columnDefinition = "TIMESTAMP")
    private LocalDateTime archivedAt;

    @Column(columnDefinition = "TIMESTAMP")
    private LocalDateTime deletedAt;
}
