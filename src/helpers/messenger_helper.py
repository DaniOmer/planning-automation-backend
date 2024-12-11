import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
from loguru import logger

from config import *

class EmailData(BaseModel):
    to_email: str
    subject: str
    html_content: str
    text_content: str = None

class MessengerHelper:
    @property
    def conf_sib(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = SENDINBLUE_API_KEY
        return configuration
    
    @property
    def api_sib(self):
        return sib_api_v3_sdk.ApiClient(self.conf_sib)
    
    @property
    def api_email(self):
        return sib_api_v3_sdk.TransactionalEmailsApi(self.api_sib)

    @staticmethod
    def send_email(data: EmailData):
        try:
            email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": data.to_email}],
                sender={"email": SENDINBLUE_EMAIL, "name": SENDINBLUE_NAME},
                reply_to={"email": REPLY_TO_EMAIL, "name": SENDINBLUE_NAME},
                subject=data.subject,
                html_content=data.html_content,
                text_content=data.text_content or data.html_content
            )

            api_instance = MessengerHelper().api_email
            api_response = api_instance.send_transac_email(email)
            logger.info(f"Email sent successfully: {api_response}")
            return {"status": "success", "data": api_response}

        except ApiException as e:
            logger.error(f"Error sending email: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
