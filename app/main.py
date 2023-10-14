from fastapi import FastAPI

from app.api.routes.user import router as user_router

app = FastAPI(title='Clinical Control Backend')

# Routes
app.include_router(user_router)


@app.get('/', include_in_schema=False)
def read_root():
    return {'message': 'Hello, World!'}
