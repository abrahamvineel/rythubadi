package rythubadi.auth.dto;

import lombok.*;

import java.util.UUID;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class NewChatSessionDTO {
    private UUID chatId;
}
