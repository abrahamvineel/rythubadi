package rythubadi.auth.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import rythubadi.auth.dto.ChatMessageDTO;
import rythubadi.auth.dto.ChatSessionDTO;
import rythubadi.auth.service.ChatService;

import java.util.List;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private final ChatService chatService;

    @Autowired
    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @PostMapping("/create/{email}")
    public void createChatSession(@PathVariable String email) {
        chatService.createChatSession(email);
    }

    @GetMapping("/user/{email}")
    public List<ChatSessionDTO> getChatSessions(@PathVariable String email) {
        return chatService.getChatSessions(email);
    }

    @GetMapping("/user/{chatId}/{email}/messages")
    public List<ChatMessageDTO> getMessagesForChatSession(@PathVariable String chatId,
                                                          @PathVariable String email) {
        return chatService.getMessagesForChatSession(chatId, email);
    }
}
