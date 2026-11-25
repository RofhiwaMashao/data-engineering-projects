import os
from sqlalchemy import create_engine
from helpers.logger import logger
from dotenv import load_dotenv

load_dotenv
import variables as var

execDir = os.path.abspath('')

### Postgres Database Engine connectors ###

params_to_pg = f"{os.getenv('DESTINATIONDBSERVERUSERNAME')}:{os.getenv('DESTINATIONDBSERVERPASSWORD')}@{os.getenv('DESTINATIONDBSERVERHOST')}:{5432}/{os.getenv('DESTINATIONDBSERVERDATABASE')}"
params_from_pg = f"{os.getenv('SOURCEDBSERVERUSERNAME')}:{os.getenv('SOURCEDBSERVERPASSWORD')}@{os.getenv('SOURCEDBSERVERHOST')}:{5432}/{os.getenv('SOURCEDBSERVERDATABASE')}"

def _build_pg_engine(params):
    return create_engine(
        f"postgresql+psycopg2://{params}",
        future=True,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_timeout=30,
        connect_args={
            "connect_timeout": 10,
            "application_name": os.getenv("JOBPROCNAME", "sharepoint_processor")
        }
    )

### Connection to Ingestion DB ###

try:
    logger.info("Opening connection to postgres server %s" % os.getenv('DESTINATIONDBSERVERHOST'))
    engine_to_postgres = _build_pg_engine(params_to_pg)

except Exception as e:
    logger.error(e)
    raise

try:
    logger.info("opening connection to postgres server %s" % os.getenv('SOURCEDBSERVERHOST'))
    engine_from_postgres = _build_pg_engine(params_from_pg)

except Exception as e:
    logger.error(e)
    raise