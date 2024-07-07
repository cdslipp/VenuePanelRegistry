# Use the official Node runtime as the base image
FROM node:18 as svelte-build

# Set the working directory for the Svelte build
WORKDIR /app

# Copy package.json and package-lock.json
COPY svelte-frontend/package.json svelte-frontend/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the Svelte application code
COPY svelte-frontend .

# Build the Svelte app
RUN npm run build

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory for the Flask app
WORKDIR /app

# Copy the requirements file and install Flask
COPY flask-backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask application code
COPY flask-backend .

# Copy the built Svelte app from the previous stage
COPY --from=svelte-build /app ./

# Expose the ports for Flask and Svelte
EXPOSE 4999 3000

# Set environment variables
ENV FLASK_APP=app.py

# Start both servers
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=4999 & node build"]
