package rythubadi.auth;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class RythubadiApplication {
    public static void main(String[] args) {
        SpringApplication.run(RythubadiApplication.class, args);
    }
}
