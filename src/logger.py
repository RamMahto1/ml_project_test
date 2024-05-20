import os
from datetime import datetime
import logging


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.logs"
dir_path = os.path.join(os.getcwd(),"logs", LOG_FILE)
os.makedirs(dir_path,exist_ok=True)


LOG_FILE_PATH = os.path.join(dir_path, LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(name)s %(lineno)s - %(levelname)s %(message)s",
    level=logging.INFO,
)

