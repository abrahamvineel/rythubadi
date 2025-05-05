package rythubadi.auth.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import rythubadi.auth.dto.*;
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
    public NewChatSessionDTO createChatSession(@PathVariable String email) {
        return chatService.createChatSession(email);
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

    @PostMapping("/message")
    public NewChatSessionDTO saveMessage(@RequestBody MessageDetailsRequest request) {
        return chatService.saveMessage(request);
    }
}
