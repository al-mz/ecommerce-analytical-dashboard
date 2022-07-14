import os
import sys
import pathlib
from webbrowser import get
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
CUR_DIR = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(BASE_DIR))

import sqlalchemy as sa
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement
from dotenv import load_dotenv
import pandas as pd
from utils.load_config import load_config_file
import logging
from logging import ERROR, handlers

logging.root.handlers = []
def get_logger(save_to_file = os.path.join('logs', f'{pathlib.Path(__file__).stem}.log')):
    log = logging.getLogger('myLogger')
    if len(log.handlers) == 0:
        log.setLevel(logging.INFO)
        format = logging.Formatter('[%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s() - %(levelname)s] %(message)s')

        ch = logging.StreamHandler()
        ch.setFormatter(format)
        log.addHandler(ch)

        if isinstance(save_to_file, str):
            pathlib.Path(save_to_file).parent.mkdir(parents = True, exist_ok = True)
            fh = handlers.RotatingFileHandler(save_to_file, maxBytes=(1048576*5), backupCount=7)
            fh.setFormatter(format)
            log.addHandler(fh)
        elif save_to_file is not None:
            raise TypeError('save_to_file needs to be of type string')
    return log

# Set loggers for the script
logger = get_logger()
logger.handlers = []
logger = get_logger()


class Olist():

    def __init__(
        self,
        config_path) -> None:
        self.config = load_config_file(config_path)
        load_dotenv(dotenv_path=self.config['postgres_env'])
        self.create_postgres_engine()
        self.logger = get_logger()

    def load_inputs(self):

        # uncompress zip file
        self.unzip_file(os.path.join(self.config['data_path'], 'input', 'olist', 'olist.zip'))

        # reads in input csv files
        dfs = {}
        for dirname, _, filenames in os.walk('./data/input/olist'):
            for filename in filenames:
                if filename.endswith('.csv') and filename.startswith('olist'):
                    self.logger.info(f"Importing input data from csv files: {filename}")
                    file_name_without_ext = filename.split('.csv')[0]
                    dfs[file_name_without_ext] = pd.read_csv(os.path.join(dirname, filename))
        return dfs
    
    def create_postgres_engine(self):
        connection_str = os.environ["DATABASE_URL"]
        self.engine = sa.create_engine(connection_str)
        self.metadata = sa.MetaData()

    def populate_tables(self):
        
        # drop views schema
        with self.engine.connect() as con:
            with open(os.path.join(CUR_DIR, "drop_views.sql")) as file:
                query = sa.text(file.read())
                con.execute(query)

        self.logger.info("Creating Olist PostgreSQL Database ...")
        dfs = self.load_inputs()

        # load tabulated data into relational tables
        for i, table in enumerate(dfs):
            self.logger.info(f'Adding table {table} ... {(i+1)/len(dfs) * 100:.1f}%')
            df = dfs[table]

            if table == 'olist_orders_dataset':
                df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
                df.sort_values(by='order_purchase_timestamp', inplace=True)
                df['order_purchase_metric_date'] = pd.to_datetime(df.order_purchase_timestamp.dt.date)
                df['order_purchase_year'] = df.order_purchase_timestamp.dt.year
                df['order_purchase_month'] = df.order_purchase_timestamp.dt.month
                df['order_purchase_month_name'] = df.order_purchase_timestamp.dt.month_name()
                df['order_purchase_day_of_week_name'] = df.order_purchase_timestamp.dt.day_name()
                df['order_purchase_day_of_week_num'] = df.order_purchase_timestamp.dt.day_of_week
            
            if table =='olist_order_items_dataset':
                df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'])
            
            try:
                df.to_sql(table, con=self.engine, if_exists='fail', index=False)
            except:
                self.logger.info(f"Table {table} already exists, skipping it ...")


    def create_views(self):

        # Create views
        self.logger.info("Creating Olist PostgreSQL Views ...")
        with self.engine.connect() as con:
            with open(os.path.join(CUR_DIR, "views.sql")) as file:
                query = sa.text(file.read())
                con.execute(query)

    @staticmethod
    def unzip_file(path_to_zip_file):
        import zipfile
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(pathlib.Path(path_to_zip_file).parent.resolve())
        

if __name__=='__main__':

    olist = Olist(os.path.join(BASE_DIR, 'config', 'config.ini'))
    olist.populate_tables()
    olist.create_views()