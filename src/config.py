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

TARGET_WELL_NAMES = [
    "BAYAN-223",
    "BESA-02",
    "BPA-4",
    "CERI-1",
    "CHRA-03 ST1",
    "EW-124 ST3",
    "LIMBAYONG-4 RDR",
    "PATAWALI-2",
    "SAPA-12",
    "SAPA-14",
    "SAPA-19ST1",
    "SAPA-24",
    "SM-102",
    "SUJT-C05",
    "KME-2",
    "ANJUNG-A3"
]

