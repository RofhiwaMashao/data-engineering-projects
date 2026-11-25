import os
import sys
import psycopg2
from psycopg2 import sql
import pandas as pd
from io import StringIO
import numpy as np
import logging
from helpers.logger import logger
logger.setLevel(logging.INFO)

#Connection parameters
conn_params_dic = {
    "host":os.getenv("DESTINATIONDBSERVERHOST"),
    "database":os.getenv("DESTINATIONDBSERVER"),
    "user":os.getenv("DESTINATIONDBSERVERUSERNAME"),
    "password":os.getenv("DESTINATIONDBSERVERPASSWORD"),
    "port":os.getenv("DESTINATIONDBSERVERPORT", "5432"),
}

# Copy to postgres function
def copy_to_pg(dataframe, table_name, schema_name = 'Staging'):

    """
    Push data to Postgres using Copy utility. This allows us to push large volumes of data in fraction of the time.

    Args:
        data (df): Pass dataframe
        table_name (str): Pass relevant table name
        schema_name (str, optional): Pass relevant schema. Defaults to 'Staging'.
    """
    def connect(conn_params_dic):

        """
        Build connection to pg.

        Returns:
            con_str: connection

        """

        conn = None

        try:
            logger.info('Connecting to the PostgreSQL.......')
            conn = psycopg2.connect(**conn_params_dic)
            logger.info("Connection successful.")

        except Exception as e:
            logger.error(e)
            conn = None
            raise

        return conn

    ## Check if table exists on pg else create with varchar cols
    def create_table_if_not_exists(conn, dataframe, table, schema):

        """
        Creates a table in PostgreSQL if it does not exits.
        Handles mixed-case table/schema names safely by quoting identifiers.

        Args:
            conn (con_str): Pass relevant connectio string
            dataframe (df): Pass dataframe
            table (str): Pass relevant table name
            schema (str): Pass relevant schema
        """

        columns = ', '.join(f'"{col}" VARCHAR' for col in dataframe.columns)

        create_table_sql = f'"CREATE TABLE IF NOT EXISTS"{schema}"."{table} ({columns});'

        try:

            with conn.cursor() as cursor:
                cursor.execute(create_table_sql)
                conn.commit()

            logger.info(f'Table "{schema}"."{table}" check complete.')

        except Exception:
            logger.error(e)

    def truncate_table(conn, dataframe, table_name, schema_name):
        """
        Truncate table before load.
        Acts as REPLACE functionality from the to_sql method.

        Args:
            conn (con_str): Pass relevant connection string
            dataframe (df): Pass dataframe
            table_name (str): Pass relevant table name
            schema_name (str): Pass relevant schema
        """

        truncate_table_table_sql = f'TRUNCATE TABLE "{schema_name}"."{table_name}";'

        try:

            with conn.cursor() as cursor:
                cursor.execute(truncate_table_table_sql)
                conn.commit()

            logger.info(f'table "{schema_name}."{table_name}" has been truncated.')

        except Exception:
            conn.rollback()
            logger.exception(f'Truncation Failed on {schema_name}.{table_name}')

    ## Push to Pg
    def copy_from_dataFile_StringIO(conn, dataframe, table, schema='Staging'):
        """
        _summary_

        Args:
            conn (con_str): Pass relevant connection string
            dataframe (df): Pass dataframe
            tabel (str): Pass relevant table name
            schema (str, optional): Pass relevant schema. Defaultis to 'Staging'.
        """

        buffer = StringIO()
        dataframe.to_csv(buffer, header=False, index=False, sep='|')
        buffer.seek(0)

        logger.info(f'Starting data push ...')

        with conn.cursor() as cursor:
            try:
                copy_sql = sql.SQL("""
                    COPY {}.{} FROM STDIN WITH (FORMAT CSV, DELIMETER '|')
                    """).format(
                        sql.Identifier(schema),
                        sql.Identifier(table)
                    )

                cursor.copy_expert(copy_sql, buffer)
                conn.commit()

                logger.info(f'Data inserted into "{schema}"."{table}" successfully.')

            except Exception:
                conn.rollback()
                logger.exception(f'COPY fAILED FOR "{schema}"."{table}"')


    try:
        ## Connection
        conn = connect(conn_params_dic)

        ## Set search path
        with conn.cursor() as cur:
            cur.execute(f"SET search_path TO {schema_name};")

        ## Table check
        create_table_if_not_exists(conn, dataframe, table_name, schema_name)

        ## Truncate table
        truncate_table(conn, dataframe, table_name, schema_name)

        ## Push data
        copy_from_dataFile_StringIO(conn, dataframe,table_name, schema_name)

    except Exception as e:
        logger.error(e)
        raise

    finally:
        conn.commit()