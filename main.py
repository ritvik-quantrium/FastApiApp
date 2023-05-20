from fastapi import FastAPI,Path,Query
from pydantic import BaseModel
from typing import Optional,List



from api import courses ,users,sections



app = FastAPI(
    title="Fast API Testing",
    description="Various API example because yes",
    version = "0.0.1",
    contact={
        "name":"I hate my name",
        "email":"respect_my_privacy@whocares.gov",
    },
    license_info={
        "name":"Not a lawyer"
    }

)

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(sections.router)


