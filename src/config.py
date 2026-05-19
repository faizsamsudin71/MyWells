import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_SERVER = os.environ.get('DB_SERVER', 'server.aemenersol.com')
DB_PORT = os.environ.get('DB_PORT', '1433')
DB_NAME = os.environ.get('DB_NAME', 'MyWells')
DB_USERNAME = os.environ.get('DB_USERNAME', 'aem')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Enersol@123!@#')
DB_DRIVER = os.environ.get('DB_DRIVER', 'ODBC+Driver+17+for+SQL+Server')

# File Paths
EXCEL_PATH = 'data/update_wpd_20260515.xlsx'
TEST_PATH = 'data/test.xlsx'

# DataFrame Constants
LIST_KEYCOLS = ['Well Name', 'Well Type']
LIST_COLS = ['DMS', 'Plan DDPTF', 'Plan DCPF', 'Plan WCPF', 'Actual DDPTF', 'Actual DCPF', 'Actual WCPF']
