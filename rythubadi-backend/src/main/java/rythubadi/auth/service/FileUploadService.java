package rythubadi.auth.service;

import rythubadi.auth.dto.FileDTO;
import rythubadi.auth.dto.FileUploadRequest;
import rythubadi.auth.model.File;
import rythubadi.auth.model.FileType;
import rythubadi.auth.repository.FileUploadRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.Date;
import java.util.List;
import java.util.Set;

@Service
public class FileUploadService {

    private Set<FileType> blackList;

    private FileUploadRepository repository;

    private S3Service s3Service;

    public FileUploadService(Set<FileType> blackList, FileUploadRepository repository, S3Service s3Service) {
        this.blackList = blackList;
        this.repository = repository;
        this.s3Service = s3Service;
    }

    public void uploadFile(FileUploadRequest fileUploadRequest, MultipartFile uploadedFile) {
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
    }

    public List<FileDTO> getFiles(String userEmail) {
        return repository.findFileByUserEmail(userEmail);
    }

    public String downloadFile(String fileName) {
        return repository.findURLByFileName(fileName);
    }
}
