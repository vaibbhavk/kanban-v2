# A Kanban application for managing and tracking tasks for a project in a professional or personal setting.

### Front-End - Vue, Bootstrap

### Back-End - Flask, SQLite, Redis

Run Locally -

- Clone the project.

```cmd
  git clone https://github.com/vaibbhavk/kanban-v2.git
```

- Go to the project root directory

```cmd
    cd kanban-v2
```

- Make sure you have these installed in your system: Node.js, Python, and Redis.

- You must have the credentials of SMTP server for sending mails.

### To run the server:-

- Go to the 'api' directory from the project root directory.

- Create a virtual environment

```cmd
    py -3 -m venv venv_name
```

- Activate the virtual environment

```cmd
    venv_name\Scripts\activate.bat
```

- Install the dependencies using pip

```cmd
    pip install -r requirements.txt
```

- Start the server

```cmd
    python main.py
```

- Server will be running on `http://localhost:5000/`. To know about the API endpoints, see the [documentation](https://app.swaggerhub.com/apis/vaibbhavk/kanban-api/2.0.0).

### To run the client:-

- Go to the 'frontend' directory from the project root directory.

- Install the dependencies using npm

```cmd
    npm install
```

- Start the client

```cmd
    npm run serve
```

- Client will be running on `http://localhost:3000/`.



## Environment Variables

To run the server, you will need to add the following environment variables to your .env file

`NO_ENV_FOR_NOW`
## Author

- [@vaibbhavk](https://www.github.com/vaibbhavk)
