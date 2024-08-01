# todolist

Describe your project here.


# Installing guides

## Установка через собранный архив Docker Image:

1. Открываем терминал и переходим в папку с архивом.

2. Загружаем Docker Image:
    ```
    docker load -i todolist.image.tar
    ```

    > ![info]
    > [Как установить Docker.](https://docs.docker.com/engine/install/).


## Сборка проекта (если нет архива):

1. Build the docker image:
    ```
    docker buildx build . --tag todolist
    ```

    > ![info]
    > [Как установить докер.](https://docs.docker.com/engine/install/).


# Запуск приложения:

```bash
sudo docker run -e BOT_TOKEN=BOT_TOKEN \
    todolist
```

Также можно воспользоваться Docker Desktop:

1. Переходим в images:

![alt text](readme-statics/image.png)

Also you can create `.env` file and use it:

```bash
sudo docker run --env-file <path_to_your_env_file> todolist
```



# Dev Mode:

1. Install deps by using `rye`:
    ```bash
    rye sync
    ```

    > ![info]
    > [How To install rye](https://rye.astral.sh/guide/installation/).

2. Create `.env` file as in [example](.env.example):
3. Run it:
    ```
    source .env
    python src/main.py
    ```
**After editing build project:**

```
make build
make build-image
```
This will create `dist/` directory with two (or one) archives.
One with source code (`todolist.sourcecode.zip`) second with
docker image (`todolist.image.tar`, [how to use this archive](#installing-from-image-archive)).

> ![info]
> If you doesn't have Docker image archive will not creates.
> 
> [How To install docker](https://docs.docker.com/engine/install/).


**VScode debugger configuration file:**
```json
{
    "configurations": [
        {
            "name": "Main.py",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
```
Copy/Paste this to [`.vscode/launch.json`](.vscode/launch.json).