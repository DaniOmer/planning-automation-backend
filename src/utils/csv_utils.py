import io
import pandas as pd
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

def validate_csv_columns(df: pd.DataFrame, required_columns: list):
    """
    Validate if all required columns are present in the CSV data.
    
    :param df: Pandas DataFrame containing CSV data
    :param required_columns: List of columns required in the CSV file
    :raises ValueError: If any required column is missing
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns in CSV: {', '.join(missing_columns)}. "
            f"Expected: {', '.join(required_columns)}"
        )

async def import_csv(
    file: UploadFile,
    session: AsyncSession,
    entity_class,
    create_service,
    required_columns: list,
    additional_data: dict = None
):
    """
    Generic utility function to import data from a CSV file into the database.

    :param file: UploadFile object containing the CSV file
    :param session: SQLAlchemy AsyncSession for database interaction
    :param entity_class: ORM model class for the entity being imported
    :param create_service: Service function to create an entity instance in the database
    :param required_columns: List of required columns in the CSV file
    :param additional_data: Additional data to include in each row (e.g., foreign key IDs)
    :return: Success message
    :raises HTTPException: If CSV processing fails
    """
    additional_data = additional_data or {}

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        validate_csv_columns(df, required_columns)

        for _, row in df.iterrows():
            entity_data = {col: row.get(col, None) for col in required_columns}
            entity_data.update(additional_data)

            await create_service(entity_class(**entity_data), session)

        return {"detail": "Data successfully imported from CSV"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {str(e)}")