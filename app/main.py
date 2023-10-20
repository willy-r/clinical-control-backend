from fastapi import FastAPI

from app.api.routes.user import router as user_router
from app.api.routes.auth import router as auth_router

app = FastAPI(title='Clinical Control Backend')

# Routes
app.include_router(user_router)
app.include_router(auth_router)


@app.get('/', include_in_schema=False)
def read_root():
    return {'message': 'Hello, World!'}
