from fastapi import APIRouter, HTTPException,File, UploadFile,Form
from typing import List,Optional
from app.api.controllers import send_template_email
from app.api.models import send_email, emailsOut
from app.api import db_manager
import random
from pydantic import EmailStr


emails = APIRouter()

@emails.post('/', response_model=emailsOut, status_code=201)
async def send_mail(sender:EmailStr=Form(...), recipient:List[EmailStr]=Form(...),content:str=Form(...),attachments:List[UploadFile]= File(...)):
    payload={"sender":sender,"recipient":recipient,"content":content}
    status=['Pending','Success']
    payload['status']=random.choice(status)
    send_template_email(payload['sender'],payload['recipient'],payload['content'],attachments)
    email_id = await db_manager.add_email(payload)

    response = {
        'id': email_id,
        **payload
    }

    return response

@emails.get('/', response_model=List[emailsOut])
async def get_emails():
    emails = await db_manager.get_all_emails()
    if not emails:
        raise HTTPException(status_code=404, detail="No emails sent")
    return emails

@emails.get('/{id}/', response_model=emailsOut)
async def get_email(id: int):
    email = await db_manager.get_email(id)
    if not email:
        raise HTTPException(status_code=404, detail="No such Email not found")
    return email

@emails.get('/{id}/details/', response_model=emailsOut)
async def get_emailDetails(id: int):
    emailDetails = await db_manager.get_email(id)
    if not emailDetails:
        raise HTTPException(status_code=404, detail="No such Email not found")
    return emailDetails




Pendingemails = APIRouter()

@Pendingemails.get('/', response_model=List[emailsOut])
async def get_pendingEmails():
    pendingEmails = await db_manager.get_pending_emails()
    '''
    Call mail function and send the pendingEmails result one by one to the fucntion
    '''
    if not pendingEmails:
        raise HTTPException(status_code=404, detail="No such Email not found")        
    return pendingEmails