import os
import shutil
import tarfile
import asyncio
import asyncssh
import sys
from loguru import logger

async def connect_to_server(REMOTE_HOST, REMOTE_PORT, USERNAME_HOST, USERNAME_PASS):
    # Подключение к серверу
    try:
        conn = await asyncssh.connect(REMOTE_HOST, port=REMOTE_PORT, username=USERNAME_HOST, 
                               password=USERNAME_PASS, known_hosts=None)
        logger.success("Successfully connected to the server.")
        await print_os_info(conn)  # Вызываем функцию для вывода информации об ОС
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to the server: {e}")
        sys.exit(1)

async def print_os_info(conn):
    # Вывод информации об операционной системе
    try:
        result = await conn.run('uname -a')
        logger.info(f"Operating System Information:\n{result.stdout.strip()}")
    except Exception as e:
        logger.error(f"An error occurred while getting OS info: {e}")

async def execute_script(conn, script_path):
    # Выполнение скрипта на удаленном сервере
    try:
        async with conn:
            result = await conn.run(f'bash {script_path}', check=True)
            logger.success(f"Script {script_path} executed successfully.")
    except Exception as e:
        logger.error(f"An error occurred while executing script {script_path}: {e}")
        sys.exit(1)

async def install_configure_environment(conn, SCRIPTS_DIR):
    # Установка и настройка окружения на удаленном сервере
    scripts = os.listdir(SCRIPTS_DIR)
    if not scripts:
        logger.info("No scripts found in the specified directory.")
        return
    
    tasks = [execute_script(conn, os.path.join(SCRIPTS_DIR, script)) for script in scripts]
    await asyncio.gather(*tasks)

async def send_files_to_server(conn, OUTPUT_DIR, INPUT_DIR):
    try:
        async with conn.start_sftp_client() as sftp:
            remote_files = await sftp.listdir(OUTPUT_DIR)
            logger.info(f"Remote files in {OUTPUT_DIR}: {remote_files}")

            # Архивируем файлы для передачи
            tar_path = 'files.tar'
            with tarfile.open(tar_path, "w") as tar:
                tar.add(INPUT_DIR, arcname=os.path.basename(INPUT_DIR))

            # Отправляем архив на сервер
            await sftp.put(tar_path, os.path.join(OUTPUT_DIR, tar_path))

            # Разархивируем архив на сервере
            result = await conn.run(f'tar -xf {os.path.join(OUTPUT_DIR, tar_path)} -C {OUTPUT_DIR}', check=True)
            logger.success("Files extracted on the server successfully.")

            # Удаляем архив
            os.remove(tar_path)
            await conn.run(f'rm {os.path.join(OUTPUT_DIR, tar_path)}', check=True)

        logger.success("Files sent to the server successfully.")
    except Exception as e:
        logger.error(f"An error occurred while sending files to the server: {e}")
        sys.exit(1)


async def post_deploy_configuration(conn, SCRIPTS_DIR_DEPLOY):
    scripts = os.listdir(SCRIPTS_DIR_DEPLOY)
    if not scripts:
        logger.info("No scripts found in the specified directory.")
        return
    
    tasks = [execute_script(conn, os.path.join(SCRIPTS_DIR_DEPLOY, script)) for script in scripts]
    await asyncio.gather(*tasks)