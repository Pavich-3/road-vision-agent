# IoT Agent для моніторингу стану дорожнього покриття (Лабораторна №1)

## 1) Що робить проєкт
Це Agent-частина системи, яка імітує роботу датчиків: читає дані акселерометра і GPS з CSV-файлів та надсилає агреговані дані в MQTT-брокер. Дані серіалізуються у JSON через marshmallow.

## 2) Структура проєкту
```
src/
  main.py
  config.py
  file_datasource.py
  schema/
    accelerometer_schema.py
    gps_schema.py
    aggregated_data_schema.py
  domain/
    accelerometer.py
    gps.py
    aggregated_data.py
  data/
    accelerometer.csv
    gps.csv
docker/
  mosquitto/config/mosquitto.conf
  docker-compose.yaml
Dockerfile
requirements.txt
README.md
```
