import psycopg2 
from datetime import datetime
from dotenv import load_dotenv
from database.connection import connection_pool


load_dotenv()


class DBManager:

    def __init__(self):
        self._create_table()
        self._create_table_jogos()

    def _create_table(self):
        conn = None
        cursor = None

        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pricescrapers(
                    id SERIAL PRIMARY KEY,
                    produto TEXT NOT NULL,
                    valor REAL NOT NULL,
                    data_verificacao TEXT NOT NULL,
                    loja_barata TEXT NOT NULL
                )
            ''')

            conn.commit()

        finally:
            if cursor:
                cursor.close()

            if conn:
                connection_pool.putconn(conn)

    def salvar_preco(self, produto, valor, loja):
        conn = None
        cursor = None

        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()

            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            cursor.execute('''
                INSERT INTO pricescrapers
                (produto, valor, data_verificacao, loja_barata)
                VALUES (%s, %s, %s, %s)
            ''', (produto, valor, data_atual, loja))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            if cursor:
                cursor.close()

            if conn:
                connection_pool.putconn(conn)

    def buscar_historico(self, produto):
        conn = None
        cursor = None

        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT valor, data_verificacao, loja_barata
                FROM pricescrapers
                WHERE produto = %s
                ORDER BY id DESC
            ''', (produto,))

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()

            if conn:
                connection_pool.putconn(conn)

    def _create_table_jogos(self):
        conn = None
        cursor = None

        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jogos (
                    id_jogo SERIAL PRIMARY KEY,
                    nome_jogo TEXT NOT NULL UNIQUE
                )
            ''')

            conn.commit()

        finally:
            if cursor:
                cursor.close()

            if conn:
                connection_pool.putconn(conn)

    def salvar_jogo(self, nome_jogo):
        conn = None
        cursor = None

        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()

            cursor.execute(
                '''
                INSERT INTO jogos (nome_jogo)
                VALUES (%s)
                RETURNING id_jogo
                ''',
                (nome_jogo,)
            )

            id_gerado = cursor.fetchone()[0]

            conn.commit()

            return id_gerado

        except psycopg2.errors.UniqueViolation as e:
            conn.rollback()
            raise
            


        except Exception as e:
            conn.rollback()
            raise e

        finally:
            if cursor:
                cursor.close()

            if conn:
                connection_pool.putconn(conn)

    def buscar_jogo(self):
        conn = None
        cursor = None

        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT *
                FROM jogos
                ORDER BY id_jogo DESC
            ''')

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()

            if conn:
                connection_pool.putconn(conn)


    def buscar_tudo(self):
        conn = None
        cursor = None 
        
        try:
            conn = connection_pool.getconn()
            cursor = conn.cursor()

            cursor.execute('''SELECT * FROM pricescrapers''')

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()

            if conn:
                connection_pool.putconn(conn)