FROM eclipse-mosquitto:2.0.10
RUN touch /mosquitto/passwd
RUN mosquitto_passwd -b /mosquitto/passwd dso_server mqtt1234
EXPOSE 1883