package rythubadi.auth.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import rythubadi.auth.dto.FileUploadDTO;
import rythubadi.auth.dto.FileUploadRequest;
import rythubadi.auth.model.AttachmentType;
import rythubadi.auth.model.File;
import rythubadi.auth.repository.FileUploadRepository;

import java.util.Date;
import java.util.Set;

@Service
public class FileUploadService {

    private Set<AttachmentType> blackList;

    private FileUploadRepository repository;

    private S3Service s3Service;

    public FileUploadService(Set<AttachmentType> blackList, FileUploadRepository repository, S3Service s3Service) {
        this.blackList = blackList;
        this.repository = repository;
        this.s3Service = s3Service;
    }

    public FileUploadDTO uploadFile(FileUploadRequest fileUploadRequest, MultipartFile uploadedFile) {
        File file = new File();
        String fileName = s3Service.uploadFile(uploadedFile);
        String preSignedUrl = s3Service.generatePreSignedUrl(fileName);
        if (!blackList.contains(fileUploadRequest.getFileType())) {
            file.setUserEmail(fileUploadRequest.getUserEmail());
            file.setFileSizeInBytes(fileUploadRequest.getFileSizeInBytes());
            file.setFileType(fileUploadRequest.getFileType());
            file.setUrl(preSignedUrl);
            file.setUploadDate(new Date(System.currentTimeMillis()));
            file.setFileName(fileName);
            repository.save(file);
        }
        FileUploadDTO fileUploadDTO = new FileUploadDTO();
        fileUploadDTO.setFileName(fileName);
        fileUploadDTO.setPreSignedUrl(preSignedUrl);
        return fileUploadDTO;
    }
}
