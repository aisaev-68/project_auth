## Реферальная система

### Переменные среды
Переименовать файл .env.example в .env и установите свои данные

### Команды для сборки и запуска

1. Собрать образы и запустить сервисы (при запуске сервисов происходить миграция и заполнение баз тестовыми данным): 
```
docker-compose up -d --build # режим prod
```
2. Для выгрузки фикстур с командной строки наберите:
```
docker-compose exec megano python manage.py dumpdata product > tests/fixtures/product-fixtures.json
```

3. Тестирование:
```
docker-compose exec megano python manage.py test tests.test_all
```

4. Просмотр статуса службы:
```
docker-compose ps -a
```
5. Просмотр лога лога приложения
```
docker-compose logs megano
```

### Другие команды работы с docker

1. Перезапустить службу:
```
 docker-compose restart
```
2. Запустить службу:
```
docker-compose start <имя службы>
```
3. Остановить службу:
```
docker-compose stop <имя службы>
```
4. Закрыть службы и удалить контейнеры:
```
docker container stop $(docker container ls -aq) &&  
docker container rm $(docker container ls -aq) &&  
docker system prune --all --volumes
```

### Сайт
```
http://127.0.0.1:8000
```