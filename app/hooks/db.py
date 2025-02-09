import mysql.connector

import os


def create_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT"),
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
    dex,
    chain,
    ticker,
    name,
    supply,
    percent,
    description,
    twitter,
    telegram,
    website,
    buy_tax,
    sell_tax,
    loan,
    duration,
    owner,
    fee,
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
            dex,
            chain, 
            ticker, 
            name, 
            supply,
            percent,
            description,
            twitter,
            telegram,
            website,
            buy_tax,
            sell_tax,
            loan,
            duration, 
            owner,
            fee
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        entry_data = (
            timedate,
            user_name,
            user_id,
            address,
            secret_key,
            dex,
            chain,
            ticker,
            name,
            supply,
            percent,
            description,
            twitter,
            telegram,
            website,
            buy_tax,
            sell_tax,
            loan,
            duration,
            owner,
            fee,
        )
        cursor.execute(add_entry_query, entry_data)
        connection.commit()

        close_connection(connection, cursor)

        return "Entry added successfully"
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
    except mysql.connector.Error:
        return "N/A"


def delete_entry(user_id):
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


def get_all_entries():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        fetch_query = """
        SELECT
            complete,
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
                    "complete": result["complete"],
                    "user_name": result["user_name"],
                    "user_id": result["user_id"],
                    "timedate": result["timedate"],
                    "address": result["address"],
                    "secret_key": result["secret_key"],
                    "chain": result["chain"],
                    "ticker": result["ticker"],
                    "owner": result["owner"],
                }
                for result in results
            ]
        else:
            return []
    except mysql.connector.Error as e:
        return f"Error: {e}"


def search_entry(user_id):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        search_query = """
        SELECT
            complete,
            timedate,
            user_name,
            user_id, 
            address,
            secret_key,
            dex,
            chain, 
            ticker, 
            name, 
            supply,
            percent,
            description,
            twitter,
            telegram,
            website,
            buy_tax,
            sell_tax,
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
                "timedate": result["timedate"],
                "complete": result["complete"],
                "user_name": result["user_name"],
                "user_id": result["user_id"],
                "address": result["address"],
                "secret_key": result["secret_key"],
                "dex": result["dex"],
                "chain": result["chain"],
                "ticker": result["ticker"],
                "name": result["name"],
                "supply": result["supply"],
                "percent": result["percent"],
                "description": result["description"],
                "twitter": result["twitter"],
                "telegram": result["telegram"],
                "website": result["website"],
                "buy_tax": result["buy_tax"],
                "sell_tax": result["sell_tax"],
                "loan": result["loan"],
                "duration": result["duration"],
                "owner": result["owner"],
                "fee": result["fee"],
            }
        else:
            return False
    except mysql.connector.Error as e:
        return f"Error: {e}"


def set_complete(user_id):
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
