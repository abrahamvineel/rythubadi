package rythubadi.auth.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import rythubadi.auth.dto.UserCreationRequest;
import rythubadi.auth.exceptions.EmailAlreadyExistsException;
import rythubadi.auth.model.User;
import rythubadi.auth.repository.UserRepository;

import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    @Autowired
    public UserService(UserRepository userRepository,
                       BCryptPasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public void createUser(UserCreationRequest user) throws EmailAlreadyExistsException {

        String email = user.getEmail();;

        if(userRepository.findByEmail(email).isPresent()) {
            throw new EmailAlreadyExistsException("User is already present with this email");
        }
        User u = new User();

        u.setEmail(email);
        String hashedPassword = passwordEncoder.encode(user.getPassword());
        u.setPassword(hashedPassword);
        userRepository.save(u);
    }

    public User findByEmail(String emailId) {
        Optional<User> user = userRepository.findByEmail(emailId);
        if(user.isPresent()) {
            return user.get();
        }
        return null;
    }
}
