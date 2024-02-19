import os
from snowflake_llm import config
from langchain_community.utilities import SQLDatabase
from urllib.parse import quote_plus

def _get_connection_url(database=None, schema=None):
    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    username = os.getenv('SNOWFLAKE_USERNAME')
    password = os.getenv('SNOWFLAKE_PASSWORD')
    database = database or config.DB_NAME
    schema = schema or config.SCHEMA_NAME
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    role = os.getenv('SNOWFLAKE_ROLE')
    snowflake_url = f"snowflake://{username}:{quote_plus(password)}@{snowflake_account}/{database}/{schema}?warehouse={warehouse}&role={role}"
    return snowflake_url


def get_lagchain_connection(database=None, schema=None):
    snowflake_sqlalchemy_20_monkey_patches()
    url = _get_connection_url(database, schema)
    return SQLDatabase.from_uri(url)

def snowflake_sqlalchemy_20_monkey_patches():
    """
        this monkey patch is needed to make the snowflake-sqlalchemy to
        work with sqlalchemy 2.0 or higher which is needed for
        langchain versions. 
        
    """
    import sqlalchemy.util.compat

    # make strings always return unicode strings
    sqlalchemy.util.compat.string_types = (str,)
    sqlalchemy.types.String.RETURNS_UNICODE = True

    import snowflake.sqlalchemy.snowdialect

    snowflake.sqlalchemy.snowdialect.SnowflakeDialect.returns_unicode_strings = True

    # make has_table() support the `info_cache` kwarg
    import snowflake.sqlalchemy.snowdialect

    def has_table(self, connection, table_name, schema=None, info_cache=None):
        """
        Checks if the table exists
        """
        return self._has_object(connection, "TABLE", table_name, schema)

    snowflake.sqlalchemy.snowdialect.SnowflakeDialect.has_table = has_table

# usage: call this function before creating an engine:

