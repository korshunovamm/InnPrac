
# Игра лабораторная работа
## Установка
### Установка Docker
Для него вам потребуется установить [Docker](https://docs.docker.com/get-docker/), [Docker Compose](https://docs.docker.com/compose/install/)
и [git](https://git-scm.com/downloads)
если он еще не установлен.

1. Клонируйте репозиторий:
```bash
git clone https://workshop.samcs.ru/bitbucket/scm/lbg/lab_work_backend.git
```
2. Перейдите в директорию, в которую клонирован код (по умолчанию lab_work_backend)
3. Запустите команду:
```bash
docker-compose up --build
```
4. После запуска сервера, он будет доступен по адресу [http://localhost:8888](http://localhost:8888)
5. `Ctrl+C` остановит сервер
6. Для удаления контейнеров и образов, запустите команду:
```bash
docker-compose down --rmi all
```
7. чтобы удалить только контейнеры, запустите команду:
```bash
docker-compose down
```