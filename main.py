from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.regex_routes import router as regex_router
from routes.bulk_regex_routes import router as bulk_regex_router
from routes.jsonpath_routes import router as jsonpath_router

app = FastAPI(
    title="Power Query Extensions API",
    description="Extend Power Query capabilities using Python backend",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(regex_router, prefix="/regex", tags=["Regex"])
app.include_router(bulk_regex_router, prefix="/regex/bulk", tags=["Bulk Regex"])
app.include_router(jsonpath_router, prefix="/jsonpath", tags=["JSONPath"])

@app.get("/")
async def root():
    return {"message": "Power Query Extensions API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
