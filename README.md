# Gym Tracking App

## Overview

The Gym Tracking App is a comprehensive solution for tracking users' workouts, including reps, sets, weight, and type of exercise. Users can choose from a pre-defined database of exercises and log their workouts to track their progress over time. I chose to work on this project to build an app that supports tracking band supported exercises.

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: Next.js, React
- **Database**: PostgreSQL
- **Migrations**: Alembic
- **Containerization**: Docker
- **Hosting**: Render.com

## Features

- User Authentication and Authorization
- API JSON conversion scripting
- Exercise Database Management
- Workout Logging (reps, sets, weight, type of exercise)
- Responsive User Interface

## Database Schema

![alt text](<docs/images/Screenshot 2024-05-15 at 8.14.45 PM.png>)

Main Models/Tables:

- **User:** Tracks user data including username and password.
- **Exercise:** Includes preset and custom exercises to be tracked by the user.
- **ExerciseLog:** Tracks date of specific exercise completed with number of reps and weight used.
- **WorkoutExercise:** Planned exercise that connects a specific exercise to a planned workout for that exercise setting the goal reps, sets, and weight.
- **Workout:** Connects a user to a list of workout exercises to build a workout routine for a custom created workout progrma.

Supporting Models/Tables:

- **Role:** Table holding values for different role types ([User, Admin])
- **WorkoutCategory:** Table holding values for different WorkoutCategory categories
- **MovementCategory:** Table holding values for different MovementCategory categories
- **MajorMuscle:** Table holding values for different MajorMuscle categories
- **Equipment:** Table holding values for different equipment type

## Installation

Follow these steps to set up the development environment for the Gym Tracking App.

### Prerequisites

- Python 3.12+
- Node.js 14+
- Docker
- PostgreSQL
- Render.com account

### Backend Setup

1. **Clone the repository**:  
   Run the following commands in terminal.

   ```sh
   git clone https://github.com/mike-jacks/gym-app.git
   cd gym-app/backend
   ```

2. **Create and activate a virtual environment**:

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. **Create a secret key in terminal to use in your .env**

   ```sh
   openssl rand -hex 16
   ```

5. **Set up environemnt variables**:  
   Create a \`.env\` file and configure the necessary environment variables. Don't forget to copy and paste you secret key.

   ```sh
   # filename: .env
   POSTGRES_URL=postgresql://postgres:postgres@localhost:5433/gymapp
   SECRET_KEY=<CUSTOM_SECRET_KEY>
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   ```

6. **Startup Database:**

   ```sh
   docker-compose up -d db
   ```

### Front End Setup

1. Navigate to the frontend directory:

   ```sh
   cd ../gym-app-frontend
   ```

2. Install next.js dependencies:

   ```sh
   npm install
   ```

3. Set up environment variables:  
   Create a .env file in the frontend directory with the following content:

   ```sh
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Running Backend and Frontend Locally

1. Within the \`backend\` folder, start the backend server with the following command:

   ```sh
   uvicorn main:app --reload
   ```

2. Within the \`gym-app-frontend\` folder, start the frontend server with the following command:

   ```sh
   npm run dev
   ```

### Alternative Docker Setup

1. Navigate to the root directory:

   ```sh
   cd ..
   ```

2. Build and run the Docker containers:

   ```sh
   docker-compose up -d --build
   ```

   You should now have 3 docker containers running:

   - A frontend containter.
   - A backend container.
   - A postgres db container.

## Deployment

### Hosting on Render.com

1. Create a a github repsitory for this project and commit and push the files to your github repository.
2. Create a new Web Service on Render.com for PostgreSQL. You will use the username, password, hostname, and db name of this database to replace the .env values when creating the backend web service next.
3. Create a new Web Service on Render.com for the backend, and choose \`Build and Deploy from a Git Repository\`. Select your repository to create the web service from. Set the Root Directory to be \`backend\`. Add the following options:

   - _Runtime:_ \`Python 3\`
   - _Build Command:_ \`pip install -r requirements.txt\`
   - _Start Command:_ \`uvicorn main:app --host 0.0.0.0 --port 8000\`
   - _Environment Variables:_ Set up as required in your .env file
   - Select your instance type

4. Create a new Web Service on Render.com for the frontend, and choose \`Build and Deploy from a Git Repository\`. Select your repository to create the web service from. Set the Root Directory to be \`gym-app-frontend\`. Add the following options:
   - _Runtime:_ \`Node\`
   - _Build Command:_ \`npm install; npm run build;\`
   - _Start Command:_ \`npm run start\`
   - _Environment Variables:_ Set \`NEXT_PUBLIC_API_URL\` to the value of the URL of your Backend URL created above \`https://<project_name>.onrender.com\`.
   - Select your instance type

### Continuous Deployment

By setting up Render.com to connect to your github repository, Set up continuous deployment by connecting your GitHub repository to Render.com. This ensures that any changes pushed to the repository are automatically deployed.

![alt text](<docs/images/Screenshot 2024-05-15 at 6.55.09 PM.png>)
