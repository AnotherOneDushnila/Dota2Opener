import logging
import os


def log(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(base_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        log_file = os.path.join(logs_dir, f"{name}.log")

        formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

        file_handler = logging.FileHandler(log_file)
        cmd_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        cmd_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(cmd_handler)

    return logger

