import mysql.connector

from datetime import datetime, timedelta
import os


def create_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),
        port = os.getenv("DB_PORT")
    )


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def add_entry(
        timedate, 
        user_name, 
        user_id, 
        address, 
        secret_key, 
        chain, 
        ticker, 
        name, 
        supply,
        amount,
        loan,
        owner
        ):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        add_entry_query = """
        INSERT INTO wallets (
            timedate, 
            user_name, 
            user_id, 
            address, 
            secret_key, 
            chain, 
            ticker, 
            name, 
            supply,
            amount,
            loan,
            owner
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        entry_data = (
            timedate, 
            user_name, 
            user_id, 
            address, 
            secret_key, 
            chain, 
            ticker, 
            name, 
            supply,
            amount,
            loan,
            owner
            )
        cursor.execute(add_entry_query, entry_data)
        connection.commit()

        close_connection(connection, cursor)

        return "Entry added successfully"
    except mysql.connector.Error as e:
        return f"Error: {e}"

 
def search_entry_by_user_id(user_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        search_query = """
        SELECT
            complete, 
            address,
            secret_key,
            chain, 
            ticker, 
            name, 
            supply,
            amount,
            loan,
            owner
        FROM wallets
        WHERE user_id = %s
        """
        cursor.execute(search_query, (user_id,))
        result = cursor.fetchone()

        close_connection(connection, cursor)

        if result:
            return {
                "complete": result["complete"],
                "address": result["address"],
                "secret_key": result["secret_key"],
                "chain": result["chain"],
                "ticker": result["ticker"],
                "name": result["name"],
                "supply": result["supply"],
                "amount": result["amount"],
                "loan": result["loan"],
                "owner": result["owner"]
            }
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"


def search_entry_by_address(address):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        search_query = """
        SELECT
            complete,
            timedate,
            user_name, 
            user_id, 
            secret_key,
            chain, 
            ticker, 
            name, 
            supply,
            amount,
            loan,
            owner
        FROM wallets
        WHERE address = %s
        """
        cursor.execute(search_query, (address,))
        result = cursor.fetchone()

        close_connection(connection, cursor)

        if result:
            return {
                "complete": result["complete"],
                "timedate": result["timedate"],
                "user_name": result["user_name"],
                "user_id": result["user_id"],
                "secret_key": result["secret_key"],
                "chain": result["chain"],
                "ticker": result["ticker"],
                "name": result["name"],
                "supply": result["supply"],
                "amount": result["amount"],
                "loan": result["loan"],
                "owner": result["owner"]
            }
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"


def delete_entry_by_user_id(user_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        delete_query = """
        DELETE FROM wallets
        WHERE user_id = %s
        """
        cursor.execute(delete_query, (user_id,))
        connection.commit()

        close_connection(connection, cursor)

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"


def fetch_all_entries():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        fetch_query = """
        SELECT
            timedate,
            address,
            user_name, 
            user_id, 
            secret_key,
            chain, 
            ticker,
            owner
        FROM wallets
        """
        cursor.execute(fetch_query)
        results = cursor.fetchall()

        close_connection(connection, cursor)

        if results:
            return [
                {
                    "user_name": result["user_name"],
                    "user_id": result["user_id"],
                    "timedate": result["timedate"],
                    "address": result["address"],
                    "secret_key": result["secret_key"],
                    "chain": result["chain"],
                    "ticker": result["ticker"],
                    "owner": result["owner"]
                } for result in results
            ]
        else:
            return []
    except mysql.connector.Error as e:
        return f"Error: {e}"

def mark_entry_as_complete_by_user_id(user_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        update_query = """
        UPDATE wallets
        SET complete = %s
        WHERE user_id = %s
        """
        cursor.execute(update_query, (True, user_id))
        connection.commit()

        close_connection(connection, cursor)

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"


def set_complete(address):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        update_query = """
        UPDATE wallets
        SET complete = %s
        WHERE address = %s
        """
        cursor.execute(update_query, (True, address))
        connection.commit()

        close_connection(connection, cursor)

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"


def set_incomplete(address):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        update_query = """
        UPDATE wallets
        SET complete = %s
        WHERE address = %s
        """
        cursor.execute(update_query, (False, address))
        connection.commit()

        close_connection(connection, cursor)

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"
