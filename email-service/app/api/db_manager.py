from app.api.models import send_email
from app.api.db import emails, database


async def add_email(payload: send_email):
    query = emails.insert().values(**payload)
    return await database.execute(query=query)

async def get_email(id):
    query = emails.select(emails.c.id==id)
    return await database.fetch_one(query=query)

async def get_all_emails():
    query = emails.select(emails)
    return await database.fetch_all(query=query)

async def get_pending_emails():
    print('inside')
    query = emails.select(emails.c.status=='Pending')
    return await database.fetch_all(query=query)

