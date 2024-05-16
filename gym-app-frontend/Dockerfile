# Use an official Node.js runtime as a parent image
FROM node:18.17.0-alpine

ARG NEXT_PUBLIC_API_URL

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install any needed packages
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Expose port 3000 to the outside world
EXPOSE 3000

# Run the application
# CMD ["npm", "run", "dev"]
