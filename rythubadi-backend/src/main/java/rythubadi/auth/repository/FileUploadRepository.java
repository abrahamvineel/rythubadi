package rythubadi.auth.repository;

import rythubadi.auth.dto.FileDTO;
import rythubadi.auth.model.File;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FileUploadRepository extends JpaRepository<File, Long> {
    @Query("select new org.fileupload.dto.FileDTO(f.fileName, f.uploadDate, f.fileSizeInBytes) from File f where f.userEmail = :userEmail")
    List<FileDTO> findFileByUserEmail(@Param("userEmail") String userEmail);

    @Query("select f.url from File f where f.fileName = :fileName")
    String findURLByFileName(@Param("fileName") String fileName);
}
