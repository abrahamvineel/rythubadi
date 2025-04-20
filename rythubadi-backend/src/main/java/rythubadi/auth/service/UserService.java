package rythubadi.auth.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import rythubadi.auth.dto.UserCreationRequest;
import rythubadi.auth.model.User;
import rythubadi.auth.repository.UserRepository;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public void createUser(UserCreationRequest user) {
        User u = new User();

        u.setEmail(user.getEmail());
        u.setPassword(user.getPassword());
        userRepository.save(u);
    }
}
