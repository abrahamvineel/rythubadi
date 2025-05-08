package rythubadi.auth.dto;

import lombok.Data;

@Data
public class FileUploadDTO {

    private String fileName;
    private String preSignedUrl;
}
