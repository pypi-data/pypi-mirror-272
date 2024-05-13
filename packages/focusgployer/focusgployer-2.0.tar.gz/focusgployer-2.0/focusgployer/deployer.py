import os
import asyncio
import asyncssh
import sys
import argparse
from loguru import logger
import shutil
import tarfile


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


def main():
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Deployer script')
    parser.add_argument('REMOTE_HOST', type=str, help='Remote host address')
    parser.add_argument('REMOTE_PORT', type=int, help='Remote host port')
    parser.add_argument('USERNAME_HOST', type=str, help='Username for SSH connection')
    parser.add_argument('USERNAME_PASS', type=str, help='Password for SSH connection')
    parser.add_argument('SCRIPTS_DIR', type=str, help='Path to scripts directory')
    parser.add_argument('INPUT_DIR', type=str, help='Path to input directory')
    parser.add_argument('OUTPUT_DIR', type=str, help='Path to output directory')
    parser.add_argument('SCRIPTS_DIR_DEPLOY', type=str, help='Path to scripts directory for deployment')

    args = parser.parse_args()

    # Создаем цикл событий для выполнения асинхронных функций
    loop = asyncio.get_event_loop()

    # Подключение к серверу
    conn = loop.run_until_complete(connect_to_server(args.REMOTE_HOST, args.REMOTE_PORT, args.USERNAME_HOST,
                                                     args.USERNAME_PASS))

    # Установка и настройка окружения на удаленном сервере
    loop.run_until_complete(install_configure_environment(conn, args.SCRIPTS_DIR))

    # Отправка файлов на сервер
    loop.run_until_complete(send_files_to_server(conn, args.OUTPUT_DIR, args.INPUT_DIR))

    # Настройка после развертывания на сервере
    loop.run_until_complete(post_deploy_configuration(conn, args.SCRIPTS_DIR_DEPLOY))

    # Закрыть соединение
    conn.close()

    # Завершить цикл событий
    loop.close()


if __name__ == '__main__':
    main()
