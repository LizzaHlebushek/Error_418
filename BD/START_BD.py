import subprocess

def build_docker_image():
    """Строим Docker образ"""
    try:
        print("Building Docker image...")
        # Выполняем команду для сборки образа
        subprocess.run(["docker", "build", "-t", "my_postgres_db", "."], check=True)
        print("Docker image built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while building Docker image: {e}")
        exit(1)

def run_docker_container():
    """Запускаем Docker контейнер"""
    try:
        print("Running Docker container...")
        # Выполняем команду для запуска контейнера
        subprocess.run(["docker", "run", "-d", "-p", "5432:5432", "--name", "my_postgres2", "my_postgres_db"], check=True)
        print("Docker container started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Docker container: {e}")
        exit(1)

def run_python_script(script_name):
    """Запускаем другой Python скрипт"""
    try:
        print(f"Running Python script: {script_name}...")
        # Выполняем команду для запуска Python скрипта
        subprocess.run(["python3", script_name], check=True)
        print(f"Python script {script_name} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Python script {script_name}: {e}")
        exit(1)

if __name__ == "__main__":
    build_docker_image()
    run_docker_container()
    run_python_script("create_table2.py")  # Запуск скрипта F.py