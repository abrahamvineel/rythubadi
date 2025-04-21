package rythubadi.auth.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import rythubadi.auth.model.Sessions;
import rythubadi.auth.repository.SessionsRepository;

import java.util.Date;

@Service
public class SessionsService {
    private final SessionsRepository sessionsRepository;

    @Autowired
    public SessionsService(SessionsRepository sessionsRepository) {
        this.sessionsRepository = sessionsRepository;
    }


    public void saveToken(String email, String token, Date expiry) {
        Sessions session = new Sessions();
        session.setEmailId(email);
        session.setToken(token);
        session.setExpiry(expiry);
        sessionsRepository.save(session);
    }

    public Boolean validateToken(String email) {
        int validSessionCount = sessionsRepository.findTokenValidity(email);
        return validSessionCount > 0;
    }
}
