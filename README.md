# todolist

Describe your project here.


# Installing guides

## Local Mode:
1. Install dependencies. Suggest to use virtual environment:
    ```
    python3.12 -m venv venv
    . ./venv/bin/activate
    pip install -U pip
    pip install -r requirements.lock
    ```

2. Rename or copy [`.env.example`](.env.example) to `.env`, and add the bot token.
3. Run Postgres docker container, you can use `docker-compose.postgres.yaml` file:
    ```
    sudo docker compose -f docker-compose.postgres.yaml up -d
    ```
4. Run application:
    ```
    python src/main.py
    ```

## Dev Mode:

1. Install deps by using `rye`:
    ```bash
    rye sync
    ```

    > [!NOTE]  
    > [How To install rye](https://rye.astral.sh/guide/installation/).

2. Create `.env` file as in [example](.env.example):
3. Run it:
    ```
    python src/main.py
    ```


## AWS Mode (in developing):

```
cdk build
```


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