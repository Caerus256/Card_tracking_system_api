# Card Status Tracking System

## Overview

This project implements a simple Card Status Tracking System using Flask, a web framework for Python. The system allows users to retrieve the status of a card based on either the card ID or the user's mobile number. It utilizes a SQLite database to store and manage card status information. The system processes CSV files to populate the initial data and provides two API endpoints: `/get_card_status` to retrieve card status information and `/print_db` to print the current database state.

## Approach

### 1. Language and Framework Choice

- **Flask:** Flask is a lightweight web framework that is easy to set up and well-suited for small to medium-sized projects. It provides the necessary tools for building web applications without unnecessary complexity. Given the simplicity of the Card Status Tracking System, Flask is a suitable choice.

- **Python:** Python is a versatile and widely-used programming language. It is known for its readability and ease of use, making it a good choice for rapid development. In this project, Python is used for the server-side logic.

### 2. Data Processing

- CSV files are processed using the Pandas library to create DataFrames, which are then cleaned and transformed. The mobile numbers are standardized, and timestamps are formatted for consistency.

### 3. Database

- SQLite is chosen as the database due to its simplicity and ease of integration with Python. The system creates tables for different card statuses (pickup, exceptions, delivered, returned) and stores the data accordingly.

### 4. API Endpoints

- `/get_card_status`: Retrieves card status information based on either card ID or user mobile number. It queries the SQLite database, sorts the results based on the timestamp, and returns the latest status.

- `/print_db`: Prints the current state of the database. This endpoint is primarily for debugging and understanding the database content.

## Possible Improvements

1. **Security:**
    - Implementing user authentication and authorization mechanisms to ensure that only authorized users can access certain endpoints.

2. **Logging:**
    - Adding logging mechanisms to track system activities, monitor potential issues, and facilitate debugging.

3. **Scaling:**
    - For larger-scale applications, consider migrating to a more robust database system (e.g., PostgreSQL)

## Build and Run
    - The application has been dockerized for simplified deployment and consistency across environments. Follow the steps below to use the Docker image:

    # Build the Docker image
    docker build -t {Flask app name} .

    # Run the Docker container 
    docker run -p 5000:5000 {Flask app name}

    Now you can access the application at `localhost:5000` and utilize the API endpoints to retrieve data.

## Conclusion

This Card Status Tracking System provides a simple and functional solution for tracking the status of cards. The choice of Flask and SQLite aligns with the project's size and requirements. The system can be further enhanced by addressing security concerns, improving error handling, and implementing testing practices. The Dockerization adds the benefits of portability, isolation, and ease of deployment, making it convenient for different environments.
