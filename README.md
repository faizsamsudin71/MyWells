# MyWells Data Pipeline

This project is a Python-based data pipeline designed to ingest, validate, and update well drilling metrics from Excel spreadsheets into a Microsoft SQL Server database (`MyWells`).

## Features
- **Data Ingestion**: Reads drilling data from Excel spreadsheets.
- **Data Validation**: Uses Pydantic to ensure data types and required fields are correct before any database operations occur.
- **Database Synchronization**: Uses SQLAlchemy to connect to SQL Server, cross-reference existing well records, and verify target well types (e.g., `'APPRAISAL CUM DEV/DEVELOPMENT'`).
- **Safety & Preview Mechanism**: Generates a detailed preview Excel file (`data/update_preview.xlsx`) of pending database updates and requires manual CLI confirmation before committing changes to the database.
- **Robust Logging**: Comprehensive logging via custom configurations to track processing steps, database connection statuses, and highlight data integrity issues.

## Project Structure
- `main.py`: The main execution script. It orchestrates reading the Excel file, running validations, managing the database session, and executing the updates.
- `src/`: Contains modularized code for configurations, database operations, Pydantic models, SQLAlchemy schemas, logging, and pipeline functions.
- `tests/`: Test suite for the pipeline functions.
- `sample_pydantic_sqlachemy_code.py`: Reference code demonstrating the integration between Pydantic and SQLAlchemy.

## Prerequisites
- Python 3.x
- Microsoft ODBC Driver 17 for SQL Server

### Required Python Packages
- `pandas`
- `sqlalchemy`
- `pydantic`
- `pyodbc`
- `openpyxl` (for reading/writing Excel files)

## Usage

1. **Run the Update Pipeline**:
   Ensure your target Excel file (e.g., `data/test.xlsx`) is placed in the `data` folder. Then execute:
   ```bash
   python main.py
   ```
   
   - The script will process the data and log its progress.
   - If updates are identified, it will export an `data/update_preview.xlsx` file.
   - You will be prompted in the terminal to either commit (`yes`) or rollback (`no`) the changes.

## Database Models
The pipeline interacts with the following tables in the `MyWells` database:
- `Well`: Core identity and type of the well.
- `WellGeneralDetails`: Additional metadata and deletion status (`isDeleted`).
- `WellPhaseDrilling`: Drilling planning and actual metrics (e.g., `Plan DDPTF`, `Actual DDPTF`, etc.) which are the primary targets for updates.
