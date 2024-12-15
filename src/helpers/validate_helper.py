import csv
from io import StringIO
from datetime import datetime
from typing import List, Tuple
from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ValidationHelper:
    """Helper class for foreign key validation"""

    @staticmethod
    async def validate_id(model, record_id: int, session: AsyncSession, field_name: str):
        """
        Validate if a record exists in the database.

        Args:
            model: SQLAlchemy model class
            record_id: ID to validate
            session: SQLAlchemy AsyncSession
            field_name: Field name for error messages (e.g., "Class", "Subject")

        Returns:
            Instance of the model if found.

        Raises:
            HTTPException: 404 if the record is not found, 500 for unexpected errors.
        """
        logger.info(f"Validating {field_name} with ID: {record_id}")
        try:
            query = select(model).where(model.id == record_id)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if not instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{field_name} with ID {record_id} not found"
                )
            return instance
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Unexpected error validating {field_name} with ID {record_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error validating {field_name} with ID {record_id}"
            )
        
    @staticmethod
    def validate_csv_content(
        csv_content: str,
        required_columns: List[str],
        date_fields: List[Tuple[str, str]]
    ) -> Tuple[List[dict], List[str]]:
        """
        Validates the content of a CSV file.

        :param csv_content: The CSV content as a string.
        :param required_columns: List of required columns.
        :param date_fields: List of tuples containing the name of the date field and the expected date format.
        :return: A tuple containing two elements:
            - A list of valid rows (parsed data).
            - A list of errors encountered (messages).
        """
        # Convert the CSV content into a StringIO object so it can be read like a file
        reader = csv.DictReader(StringIO(csv_content))
        errors = []
        valid_rows = []

        # Validate required columns
        if not set(required_columns).issubset(reader.fieldnames or []):
            missing_columns = set(required_columns) - set(reader.fieldnames or [])
            errors.append(f"CSV file is missing required columns: {', '.join(missing_columns)}")
            return [], errors

        # Validate each row
        for idx, row in enumerate(reader, start=1):
            try:
                # Check for required fields
                for column in required_columns:
                    if not row.get(column, "").strip():
                        raise ValueError(f"Missing required field '{column}' on row {idx}.")

                # Validate date fields
                for date_field, date_format in date_fields:
                    date_value = row.get(date_field, "").strip()
                    if date_value:
                        try:
                            row[date_field] = datetime.strptime(date_value, date_format).date()
                        except ValueError:
                            raise ValueError(f"Invalid date format on row {idx}: '{date_value}'. Expected format: {date_format}.")

                valid_rows.append(row)

            except Exception as e:
                errors.append(f"Error on row {idx}: {e}")

        return valid_rows, errors

