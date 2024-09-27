# Tutorial

Follow these steps to set up the project:

1. **Initialize a Git repository**:
    ```sh
    git init
    ```

2. **Add the remote repository**:
    ```sh
    git remote add origin https://github.com/fikridean/INNA-KM.git
    ```

3. **Fetch the latest changes from the remote repository**:
    ```sh
    git fetch
    ```

4. **Checkout the `dev` branch**:
    ```sh
    git checkout dev
    ```

5. **Navigate to the backend directory**:
    ```sh
    cd backend
    ```

6. **Copy the example environment file to create your own `.env` file**:
    ```sh
    cp app/.env.example app/.env
    ```

Make sure to fill in the necessary environment variables in the `.env` file before running the application.

- **Create a virtual environment**:
    ```sh
    python3 -m venv venv
    ```

- **Activate the virtual environment**:
    - For Linux/macOS:
        ```sh
        source venv/bin/activate
        ```
    - For Windows:
        ```sh
        venv\Scripts\activate
        ```

- **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

- **Run FastAPI**:
    ```sh
    fastapi dev app/main.py
    ```

- **Preview the documentation locally using MkDocs**:
    ```sh
    mkdocs serve
    ```

- **Setting up the Search feature**:
    For code to create the search index, please visit the [Search Index Section](/E/#setting-up-the-search-index).

For more information, please visit <a target=_blank href='https://github.com/fikridean/INNAKM'>INNAKM Github Repository</a>.