from fastapi import FastAPI, Request, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok

from db import engine, SQLModel
from routes import authorization, exercises, users, workouts, workout_exercises, exercise_logs

app = FastAPI()

origins = ["*", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(authorization.router, tags=["Authorization"])
app.include_router(exercises.router, tags=["Exercises"])
app.include_router(workouts.router, tags=["Workouts"]) 
app.include_router(users.router, tags=["Users"])
app.include_router(exercise_logs.router, tags=["Exercise Logs"])
app.include_router(workout_exercises.router, tags=["Workout Exercises"])


# Uncomment to force HTTPS
# @app.middleware("http")
# async def enforce_https(request: Request, call_next):
#     if not request.url.scheme == "https":
#         raise HTTPException(status_code=400, detail="Use HTTPS instead of HTTP.")
#     return await call_next(request)

# if __name__ == "__main__":
#     # # Setup ngrok
#     # ngrok_tunnel = ngrok.connect(8000)
#     # print("Public URL:", ngrok_tunnel.public_url)
#     # Run Uvicorn
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)