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

## 3) Як створити venv
```
python -m venv .venv
```

## 4) Як встановити залежності
```
pip install -r requirements.txt
```

## 5) Як запустити локально
Перейдіть у директорію `src`, щоб відносні шляхи до CSV були коректні:
```
cd src
python main.py
```

## 6) Як запустити через docker-compose
```
docker compose -f docker/docker-compose.yaml up --build
```

## 7) Як перевірити повідомлення через MQTT Explorer
1. Відкрийте MQTT Explorer.
2. Підключіться до брокера:
   - Host: `localhost`
   - Port: `1883`
3. Підпишіться на топік `agent_data_topic`.

## 8) Приклад JSON-повідомлення
```json
{
  "accelerometer": {
    "x": 12,
    "y": 5,
    "z": 101
  },
  "gps": {
    "longitude": 30.5234,
    "latitude": 50.4501
  },
  "time": "2026-03-10T12:34:56.789123"
}
```
