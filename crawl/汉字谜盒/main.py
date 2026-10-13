from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app=FastAPI(tittle="汉字谜盒")
app.mount("/static", StaticFiles(directory="./crawl/汉字谜盒/static"), name="static")



@app.get("/")
def root():
    return FileResponse("./crawl/汉字谜盒/static/index.html")


@app.get("/api/sessions")
def 


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=800)
