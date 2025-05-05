package rythubadi.auth.dto;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MessageDetailsRequest {

    private String chatId;
    private String email;
    private String message;
}
