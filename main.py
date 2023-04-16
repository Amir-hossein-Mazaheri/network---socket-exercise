import os
import logging
from dotenv import load_dotenv

from src.PathScanner import PathScanner
from src.Server import Server

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


load_dotenv()

port = int(os.getenv("PORT", 5000))

app = Server()

app.listen(port)

app.start()
