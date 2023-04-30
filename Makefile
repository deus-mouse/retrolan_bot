sudo docker build -t rb-image .

- Без монтирования черного списка:
sudo docker run --rm --name rb-container -d rb-image

- С монтированием черного списка:
    1) найти путь до rb-blacklist.xlsx на хостовой машине
        host:
            /home/deusmouse/code/retrolan_bot/rb-blacklist.xlsx

    2) найти путь до rb-blacklist.xlsx внутри контейнера
        - запустить контейнер:
            sudo docker run --rm --name rb-container -d rb-image
        - попасть в контейнер:
            docker exec -t -i rb-container /bin/bash

        docker:
            /usr/src/retrolan-bot/rb-blacklist.xlsx

        - убить контейнер:
            sudo docker stop rb-container
            sudo docker rm rb-container

    3) запустить контейнер с указанием путей host:docker
        docker run -it -v /home/deusmouse/code/retrolan_bot/rb-blacklist.xlsx:/usr/src/retrolan-bot/rb-blacklist.xlsx --name rb-container -d rb-image
