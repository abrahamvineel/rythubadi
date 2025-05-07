package rythubadi.auth.dto;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
public class FileDTO {
    private String fileName;
    private Date uploadDate;
    private int fileSizeInBytes;

    public FileDTO(String fileName, Date uploadDate, int fileSizeInBytes) {
        this.fileName = fileName;
        this.uploadDate = uploadDate;
        this.fileSizeInBytes = fileSizeInBytes;
    }
}
