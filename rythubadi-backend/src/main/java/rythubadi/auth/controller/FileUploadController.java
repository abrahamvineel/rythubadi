package rythubadi.auth.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import rythubadi.auth.dto.FileUploadRequest;
import rythubadi.auth.dto.NewChatSessionDTO;
import rythubadi.auth.model.AttachmentType;
import rythubadi.auth.service.ChatService;

@RestController
@RequestMapping("/api/chat/files")
@AllArgsConstructor
public class FileUploadController {

    private ChatService chatService;

    @PostMapping("/upload")
    @ResponseStatus(HttpStatus.CREATED)
    public NewChatSessionDTO uploadFile(@RequestParam("file") MultipartFile file,
                                        @RequestParam("metadata") String request) throws JsonProcessingException {

        ObjectMapper objectMapper = new ObjectMapper();
        FileUploadRequest r = objectMapper.readValue(request, FileUploadRequest.class);

        String mimeType = file.getContentType();
        AttachmentType fileType = AttachmentType.mimeType(mimeType);
        r.setFileType(fileType);

        return chatService.saveFile(r, file);
    }
}
