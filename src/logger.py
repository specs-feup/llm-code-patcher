import logging

def build_logger():
    logger = logging.getLogger("llm_code_patcher")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("llm_code_patcher.log")

    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    file_formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")

    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)

    return logger

logger = build_logger()