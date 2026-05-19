import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_SERVER = os.environ.get('DB_SERVER')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DRIVER = os.environ.get('DB_DRIVER')

# File Paths
EXCEL_PATH = 'data/update_wpd_20260515.xlsx'
TEST_PATH = 'data/test.xlsx'

# DataFrame Constants
LIST_KEYCOLS = ['Well Name', 'Well Type']
LIST_COLS = ['DMS', 'Plan DDPTF', 'Plan DCPF', 'Plan WCPF', 'Actual DDPTF', 'Actual DCPF', 'Actual WCPF']
