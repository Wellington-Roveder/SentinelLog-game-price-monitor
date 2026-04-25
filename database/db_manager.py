import sqlite3
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

class DBManager:
    def __init__(self, db_name = os.getenv('DB_NAME')):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.c  = self.conn.cursor()
        self._create_table()

    
    def _create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS pricescrapers(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          produto TEXT NOT NULL, 
                          valor REAL NOT NULL,
                          data_verificacao TEXT NOT NULL,
                          loja_barata TEXT NOT NULL)''')
        self.conn.commit()

    def salvar_preco(self, produto, valor, loja):
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            self.c.execute('''
                INSERT INTO pricescrapers (produto, valor, data_verificacao, loja_barata)
                VALUES (?, ?, ?, ?)''', (produto, valor, data_atual, loja))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e 

    def buscar_historico(self, produto):
        self.c.execute('''SELECT valor, data_verificacao, loja_barata
            FROM pricescrapers 
            WHERE produto = ? 
            ORDER BY id DESC''', (produto,))
        return self.c.fetchall()         
            

    def fechar_conexao(self):
        self.conn.close() 






    
        
    