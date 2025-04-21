package rythubadi.auth.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.*;

import java.util.Date;

@Entity
@Table(name = "sessions")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class Sessions {

    @Id
    @Column(nullable = false)
    private String emailId;

    @Column(unique = true, nullable = false)
    private String token;

    @Column(nullable = false)
    private Date expiry;
}
