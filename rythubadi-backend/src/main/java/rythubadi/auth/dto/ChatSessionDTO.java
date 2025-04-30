package rythubadi.auth.dto;

import lombok.*;

import java.util.UUID;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class ChatSessionDTO {

    private UUID id;
    private String title;
}
