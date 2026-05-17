from services.sentinel_price import *
from database.db_manager import DBManager

db = DBManager()

if __name__ == "__main__":
    executar_monitor(db)

#streamlit run dashboard/app.py , para rodar o dashboard
