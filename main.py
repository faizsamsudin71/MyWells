import pandas as pd
# pyrefly: ignore [missing-import]
from src.logger import setup_logger
# pyrefly: ignore [missing-import]
from src.config import EXCEL_PATH, TEST_PATH
# pyrefly: ignore [missing-import]
from src.database import get_db_session
# pyrefly: ignore [missing-import]
from src.pipeline import (
    get_rows_to_update,
    check_duplicates,
    fetch_wells_from_db,
    validate_dataframe,
    prepare_db_updates,
    generate_preview_excel,
    prompt_user_for_commit
)

logger = setup_logger(__name__)

def run_pipeline(excel_path: str) -> None:
    session = None
    try:
        df = pd.read_excel(excel_path)
        df_filtered = get_rows_to_update(df)
        if check_duplicates(df_filtered):
            df_filtered = df_filtered.drop_duplicates(subset=['Well Name'], keep='first')
            
        logger.info(f"Filtered df - Total: {len(df_filtered.columns)}, Unique: {len(df_filtered.columns.unique())}")

        session = get_db_session()

        validated_data = validate_dataframe(df_filtered)
        well_names_from_df = list({entry.WellName for entry in validated_data})

        well_lookup = fetch_wells_from_db(session, well_names_from_df)
        if well_lookup is None:
            logger.error("Cannot proceed: missing wells in database")
            session.rollback()
            return

        updated_records = prepare_db_updates(session, validated_data, well_lookup)
        generate_preview_excel(updated_records, well_lookup)

        if updated_records:
            prompt_user_for_commit(session)
        else:
            logger.info("No records to update.")

    except Exception as e:
        if session:
            session.rollback()
        logger.error(f"An error occurred during update: {e}")
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    logger.info("Starting Well Data Update Pipeline")
    # For testing, use: 
    run_pipeline(TEST_PATH)
    # run_pipeline(EXCEL_PATH)