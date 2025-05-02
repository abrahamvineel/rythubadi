package rythubadi.auth.dto;

import lombok.*;
import rythubadi.auth.model.AttachmentType;
import rythubadi.auth.model.MessageStatus;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class ChatMessageDTO {

    private String content;

    private String attachmentURL;

    private AttachmentType type;

    private MessageStatus status;

    private boolean systemGenerated;
}
