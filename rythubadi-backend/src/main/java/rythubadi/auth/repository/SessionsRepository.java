package rythubadi.auth.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import rythubadi.auth.model.Sessions;

public interface SessionsRepository extends JpaRepository<Sessions, String> {

    @Query("SELECT COUNT(s.emailId) FROM Sessions s WHERE s.emailId = :email AND s.expiry > CURRENT_TIMESTAMP")
    int findTokenValidity(@Param("email") String email);
}
