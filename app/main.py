from fastapi import FastAPI

app = FastAPI(title='Clinical Control Backend')


@app.get('/', include_in_schema=False)
def read_root():
    return {'message': 'Hello, World!'}
