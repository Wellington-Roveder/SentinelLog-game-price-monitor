from psycopg2.pool import ThreadedConnectionPool
from utils.logger import configurar_logger
from dotenv import load_dotenv
import os

load_dotenv()
logger = configurar_logger()


connection_pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_SENHA"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")

)
