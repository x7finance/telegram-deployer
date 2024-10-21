import mysql.connector

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
        percent,
        loan,
        duration,
        owner,
        fee
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
            percent,
            loan,
            duration, 
            owner,
            fee
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            percent,
            loan,
            duration,
            owner,
            fee
            )
        cursor.execute(add_entry_query, entry_data)
        connection.commit()

        close_connection(connection, cursor)

        return "Entry added successfully"
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
            percent,
            loan,
            duration,
            owner,
            fee
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
                "percent": result["percent"],
                "loan": result["loan"],
                "duration": result["duration"],
                "owner": result["owner"],
                "fee": result["fee"]
            }
        else:
            return False
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
            percent,
            loan,
            duration,
            owner,
            fee
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
                "percent": result["percent"],
                "loan": result["loan"],
                "duration": result["duration"],
                "owner": result["owner"],
                "fee": result["fee"]
            }
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"


def search_entry_by_user_name(name):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        search_query = """
        SELECT
            complete,
            address,
            timedate,
            user_name, 
            user_id, 
            secret_key,
            chain, 
            ticker, 
            name, 
            supply,
            percent,
            loan,
            duration,
            owner,
            fee
        FROM wallets
        WHERE user_name = %s
        """
        cursor.execute(search_query, (name,))
        result = cursor.fetchone()

        close_connection(connection, cursor)

        if result:
            return {
                "complete": result["complete"],
                "address": result["address"],
                "timedate": result["timedate"],
                "user_name": result["user_name"],
                "user_id": result["user_id"],
                "secret_key": result["secret_key"],
                "chain": result["chain"],
                "ticker": result["ticker"],
                "name": result["name"],
                "supply": result["supply"],
                "percent": result["percent"],
                "loan": result["loan"],
                "duration": result["duration"],
                "owner": result["owner"],
                "fee": result["fee"]
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
    

def delete_entry_by_wallet(address):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        delete_query = """
        DELETE FROM wallets
        WHERE address = %s
        """
        cursor.execute(delete_query, (address,))
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
        
        check_log_query = "SELECT count FROM log"
        cursor.execute(check_log_query)
        log_row = cursor.fetchone()

        if log_row is None:
            insert_log_query = "INSERT INTO log (count) VALUES (1)"
            cursor.execute(insert_log_query)
        else:
            increment_log_query = "UPDATE log SET count = count + 1"
            cursor.execute(increment_log_query)
        connection.commit()

        close_connection(connection, cursor)

        return True
    except mysql.connector.Error as e:
        return f"Error: {e}"

def count_launches():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        select_query = "SELECT SUM(count) FROM log"
        cursor.execute(select_query)
        count = cursor.fetchone()[0]

        close_connection(connection, cursor)
        return count
    except mysql.connector.Error as e:
        return "N/A"