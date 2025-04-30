package rythubadi.auth.controller;

import jakarta.websocket.server.PathParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import rythubadi.auth.dto.ChatSessionDTO;
import rythubadi.auth.model.ChatSession;
import rythubadi.auth.service.ChatService;

import java.util.List;
import java.util.UUID;

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
}
