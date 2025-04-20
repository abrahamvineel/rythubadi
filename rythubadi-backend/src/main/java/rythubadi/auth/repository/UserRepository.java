package rythubadi.auth.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import rythubadi.auth.model.User;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}
