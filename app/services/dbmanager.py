import os
import aiomysql


class DBManager:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = int(os.getenv("DB_PORT"))
        self.pool = None

    async def _get_pool(self):
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.database,
                port=self.port,
                autocommit=True,
            )
        return self.pool

    async def _execute_query(
        self,
        query,
        params=None,
        fetch_one=False,
        fetch_all=False,
        commit=False,
    ):
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(query, params or ())

                    if commit:
                        await conn.commit()

                    if fetch_one:
                        return await cur.fetchone()
                    if fetch_all:
                        return await cur.fetchall()
                    return None

        except Exception as e:
            print(f"Database error: {str(e)}")
            return None

    async def add_entry(self, **kwargs):
        query = """
        INSERT INTO deployer (
            timedate, user_name, user_id, address, secret_key, dex, chain, ticker, name, supply,
            percent, description, twitter, telegram, website, buy_tax, sell_tax, loan, duration, owner, fee
        ) VALUES (%(timedate)s, %(user_name)s, %(user_id)s, %(address)s, %(secret_key)s, %(dex)s, %(chain)s, 
                  %(ticker)s, %(name)s, %(supply)s, %(percent)s, %(description)s, %(twitter)s, %(telegram)s, 
                  %(website)s, %(buy_tax)s, %(sell_tax)s, %(loan)s, %(duration)s, %(owner)s, %(fee)s)
        """
        result = await self._execute_query(query, kwargs, commit=True)
        return (
            "Entry added successfully"
            if result is not None
            else "Error adding entry"
        )

    async def count_launches(self):
        query = "SELECT amount FROM log WHERE name = 'deployed'"
        result = await self._execute_query(query, fetch_one=True)
        return (
            result["amount"] if result and result["amount"] is not None else 0
        )

    async def delete_entry(self, user_id):
        query = "DELETE FROM deployer WHERE user_id = %s"
        result = await self._execute_query(query, (user_id,), commit=True)
        return result is not None

    async def get_all_entries(self):
        query = """
        SELECT complete, timedate, address, user_name, user_id, secret_key, chain, ticker, owner
        FROM deployer
        """
        return await self._execute_query(query, fetch_all=True) or []

    async def search_entry(self, user_id):
        query = """
        SELECT complete, timedate, user_name, user_id, address, secret_key, dex, chain, ticker, 
               name, supply, percent, description, twitter, telegram, website, buy_tax, sell_tax, 
               loan, duration, owner, fee
        FROM deployer
        WHERE user_id = %s
        """
        result = await self._execute_query(query, (user_id,), fetch_one=True)
        return result if result else False

    async def set_complete(self, user_id):
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(
                        "UPDATE deployer SET complete = %s WHERE user_id = %s",
                        (True, user_id),
                    )

                    await cur.execute(
                        "SELECT amount FROM log WHERE name = 'deployed'"
                    )
                    log_row = await cur.fetchone()

                    if log_row is None:
                        await cur.execute(
                            "INSERT INTO log (name, amount) VALUES ('deployed', 1)"
                        )
                    else:
                        await cur.execute(
                            "UPDATE log SET amount = amount + 1 WHERE name = 'deployed'"
                        )

                    return True
        except Exception as e:
            print(f"Error: {e}")
            return False
