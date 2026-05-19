from typing import Optional, List, Dict
from collections import Counter
import pandas as pd
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from src.logger import setup_logger
# pyrefly: ignore [missing-import]
from src.config import LIST_KEYCOLS, LIST_COLS
# pyrefly: ignore [missing-import]
from src.models import Well, WellPhaseDrilling, WellGeneralDetails
# pyrefly: ignore [missing-import]
from src.schemas import WellDrillingSchema

logger = setup_logger(__name__)

def get_rows_to_update(df: pd.DataFrame, list_keycols: Optional[List[str]] = None, list_cols: Optional[List[str]] = None) -> pd.DataFrame:
    if list_keycols is None:
        list_keycols = LIST_KEYCOLS
    if list_cols is None:
        list_cols = LIST_COLS

    cols_needed = list_keycols + list_cols
    filtered_df = df[cols_needed]
    
    dms_condition = (filtered_df['DMS'] != 'No')
    columns_condition = filtered_df[list_cols].notna().any(axis=1)
    
    condition = dms_condition & columns_condition
    return filtered_df[condition].copy()

def check_duplicates(df: pd.DataFrame, column: str = 'Well Name') -> bool:
    dups = df[df.duplicated(subset=[column], keep=False)][column].unique()
    if len(dups) > 0:
        logger.warning(f"Found duplicate {column}s: {list(dups)}")
        return True
    return False

def fetch_wells_from_db(session: Session, well_names: List[str]) -> Optional[Dict[str, Well]]:
    logger.info(f"Fetching {len(well_names)} wells from database")
    target_type = 'APPRAISAL CUM DEV/DEVELOPMENT'

    matched_wells = session.query(Well).join(
        WellGeneralDetails, Well.Id == WellGeneralDetails.WellId
    ).filter(
        Well.WellName.in_(well_names),
        Well.WellType == target_type,
        WellGeneralDetails.isDeleted == False
    ).all()

    found_names = {w.WellName for w in matched_wells}
    missing_names = list(set(well_names) - found_names)

    db_duplicates = [name for name, count in Counter(w.WellName for w in matched_wells).items() if count > 1]
    if db_duplicates:
        logger.error(f"DB Integrity Error: Multiple '{target_type}' records found for: {db_duplicates}")
        return None

    if missing_names:
        logger.warning(f"{len(missing_names)} well(s) not found as '{target_type}' and not active. Investigating...")
        diagnostic_wells = session.query(Well).filter(Well.WellName.in_(missing_names)).all()
        
        found_with_other_attributes = {}
        for w in diagnostic_wells:
            general_details = session.query(WellGeneralDetails).filter_by(WellId=w.Id).first()
            status = f"Type: '{w.WellType}'"
            if general_details:
                status += f", Deleted: {general_details.isDeleted}"
            found_with_other_attributes[w.WellName] = status

        truly_missing = set(missing_names) - set(found_with_other_attributes.keys())

        if found_with_other_attributes:
            mismatch_details = [f"{name} ({status})" for name, status in found_with_other_attributes.items()]
            logger.warning(f"Wells found with other attributes: {mismatch_details}")
            
        if truly_missing:
            logger.warning(f"Well names not found in DB at all: {truly_missing}")
            
        return None

    logger.info(f"Successfully validated all {len(matched_wells)} wells")
    return {w.WellName: w for w in matched_wells}

def validate_dataframe(df: pd.DataFrame) -> List[WellDrillingSchema]:
    try:
        validated_data = [WellDrillingSchema(**row) for row in df.to_dict('records') if row['DMS'] != 'No']
        logger.info(f"Validated {len(validated_data)} records")
        return validated_data
    except Exception as e:
        logger.error(f"Validation Error: {e}")
        raise ValueError(f"Data validation failed: {e}")

def prepare_db_updates(session: Session, validated_data: List[WellDrillingSchema], well_lookup: Dict[str, Well]) -> List[WellPhaseDrilling]:
    for entry in validated_data:
        well = well_lookup.get(entry.WellName)
        if well:
            drilling_record = session.query(WellPhaseDrilling).filter_by(WellId=well.Id).first()

            if not drilling_record:
                logger.warning(f"No existing drilling record found for well '{entry.WellName}' (ID: {well.Id}). Skipping.")
                continue

            drilling_record.DrillingMinStandard = entry.DrillingMinStandard
            drilling_record.PlanDdptf = entry.PlanDdptf
            drilling_record.PlanDcpf = entry.PlanDcpf
            drilling_record.PlanWcpf = entry.PlanWcpf
            drilling_record.ActualDdptf = entry.ActualDdptf
            drilling_record.ActualDcpf = entry.ActualDcpf
            drilling_record.ActualWcpf = entry.ActualWcpf

    session.flush()
    logger.info("Changes staged for review")

    target_ids = [w.Id for w in well_lookup.values()]
    
    results = session.query(WellPhaseDrilling, Well.WellName).join(
        Well, WellPhaseDrilling.WellId == Well.Id
    ).join(
        WellGeneralDetails, Well.Id == WellGeneralDetails.WellId
    ).filter(
        WellPhaseDrilling.WellId.in_(target_ids),
        WellGeneralDetails.isDeleted == False
    ).all() # list of tuple [(WellPhaseDrilling, Well.WellName), (WellPhaseDrilling, Well.WellName), ...]   
    
    updated_records = []
    logger.info(f"Reviewing {len(results)} staged updates:")
    for rec, well_name in results:
        logger.info(f"  -> WellName: {well_name} | New DMS: {rec.DrillingMinStandard}")
        updated_records.append(rec)
        
    return updated_records

def generate_preview_excel(updated_records: List[WellPhaseDrilling], well_lookup: Dict[str, Well], output_path: str = 'data/update_preview.xlsx') -> None:
    if not updated_records:
        return
        
    preview_list = []
    for rec in updated_records:
        row = {column.name: getattr(rec, column.name) for column in rec.__table__.columns}
        well_name = next((name for name, w in well_lookup.items() if w.Id == rec.WellId), "Unknown")
        row = {"Well Name": well_name, **row}
        preview_list.append(row)
    
    pd.DataFrame(preview_list).to_excel(output_path, index=False)
    logger.info(f"Detailed preview exported to {output_path}")

def prompt_user_for_commit(session: Session) -> None:
    user_input = input("\n[ACTION REQUIRED] Do these changes look correct? (type 'yes' to commit, 'no' to rollback): ")
    if user_input.lower() == 'yes':
        session.commit()
        logger.info("Changes saved successfully to database")
    else:
        session.rollback()
        logger.info("Update cancelled. Database remains unchanged.")
