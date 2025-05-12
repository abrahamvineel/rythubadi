package rythubadi.auth.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;

@Entity
@Table(name = "file")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class File {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    private String userEmail;
    private int fileSizeInBytes;
    private AttachmentType fileType;
    @Column(length = 512)
    private String url;
    private Date uploadDate;
    private String fileName;
}
