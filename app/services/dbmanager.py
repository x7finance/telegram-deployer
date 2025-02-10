import mysql.connector
import os


class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def add_entry(self, **kwargs):
        try:
            self.connect()
            query = """
            INSERT INTO wallets (
                timedate, user_name, user_id, address, secret_key, dex, chain, ticker, name, supply,
                percent, description, twitter, telegram, website, buy_tax, sell_tax, loan, duration, owner, fee
            ) VALUES (%(timedate)s, %(user_name)s, %(user_id)s, %(address)s, %(secret_key)s, %(dex)s, %(chain)s, 
                      %(ticker)s, %(name)s, %(supply)s, %(percent)s, %(description)s, %(twitter)s, %(telegram)s, 
                      %(website)s, %(buy_tax)s, %(sell_tax)s, %(loan)s, %(duration)s, %(owner)s, %(fee)s)
            """
            self.cursor.execute(query, kwargs)
            self.connection.commit()
            return "Entry added successfully"
        except mysql.connector.Error as e:
            return f"Error: {e}"
        finally:
            self.close()

    def count_launches(self):
        try:
            self.connect()
            self.cursor.execute("SELECT SUM(count) FROM log")
            count = self.cursor.fetchone()["SUM(count)"]
            return count if count is not None else 0
        except mysql.connector.Error:
            return "N/A"
        finally:
            self.close()

    def delete_entry(self, user_id):
        try:
            self.connect()
            query = "DELETE FROM wallets WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            return f"Error: {e}"
        finally:
            self.close()

    def get_all_entries(self):
        try:
            self.connect()
            query = """
            SELECT complete, timedate, address, user_name, user_id, secret_key, chain, ticker, owner
            FROM wallets
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results if results else []
        except mysql.connector.Error as e:
            return f"Error: {e}"
        finally:
            self.close()

    def search_entry(self, user_id):
        try:
            self.connect()
            query = """
            SELECT complete, timedate, user_name, user_id, address, secret_key, dex, chain, ticker, 
                   name, supply, percent, description, twitter, telegram, website, buy_tax, sell_tax, 
                   loan, duration, owner, fee
            FROM wallets
            WHERE user_id = %s
            """
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result if result else False
        except mysql.connector.Error as e:
            return f"Error: {e}"
        finally:
            self.close()

    def set_complete(self, user_id):
        try:
            self.connect()
            update_query = (
                "UPDATE wallets SET complete = %s WHERE user_id = %s"
            )
            self.cursor.execute(update_query, (True, user_id))
            self.connection.commit()

            self.cursor.execute("SELECT count FROM log")
            log_row = self.cursor.fetchone()

            if log_row is None:
                self.cursor.execute("INSERT INTO log (count) VALUES (1)")
            else:
                self.cursor.execute("UPDATE log SET count = count + 1")
            self.connection.commit()

            return True
        except mysql.connector.Error as e:
            return f"Error: {e}"
        finally:
            self.close()
