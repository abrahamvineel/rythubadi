package rythubadi.auth.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import rythubadi.auth.dto.FileUploadRequest;
import rythubadi.auth.service.ChatService;
import rythubadi.auth.service.FileUploadService;
import rythubadi.auth.model.FileType;

@RestController
@RequestMapping("/api/chat/files")
@AllArgsConstructor
public class FileUploadController {

    private ChatService chatService;

    @PostMapping("/upload")
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file,
                                             @RequestParam("metadata") String request) throws JsonProcessingException {

        ObjectMapper objectMapper = new ObjectMapper();
        FileUploadRequest r = objectMapper.readValue(request, FileUploadRequest.class);

        String mimeType = file.getContentType();
        FileType fileType = FileType.mimeType(mimeType);
        r.setFileType(fileType);

        chatService.saveFile(r, file);

        return ResponseEntity.status(HttpStatus.CREATED).body("File uploaded");
    }

}
