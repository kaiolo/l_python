from fastapi import FastAPI

app=FastAPI()
@app.get("/")
def root():
    return {"message" : "Hello Word"}

@app.get("/users")
def get_users():
    return [{"id":1,"name":"xu"},{"id":2,"name":"kai"}]

if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=800)