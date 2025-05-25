# T-shirt Fulfillment AI Agent - Main entry point

from tshirt_fulfillment.src.interfaces.api.fastapi_app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
