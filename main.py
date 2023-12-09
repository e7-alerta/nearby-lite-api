from fastapi import FastAPI

from web import nearby

app = FastAPI()
app.include_router(nearby.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)
