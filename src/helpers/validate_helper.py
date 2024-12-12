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
