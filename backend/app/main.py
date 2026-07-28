from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="PlanYourTrip API",
        description="Backend API for PlanYourTrip",
        version="0.1.0",
    )

    @app.get("/")
    async def root():
        return {"message": "Welcome to PlanYourTrip API"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


app = create_app()