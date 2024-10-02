# Donation Project using Revolut with Flask and Node.js 💸✨

Welcome to the Donation Project! This project leverages Flask for the backend, Node.js for various functionalities, and integrates with Revolut for handling donations. 🎉

## Table of Contents 📜
1. [Introduction](#introduction)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [Usage](#usage)

## Introduction 📚
The Donation Project aims to provide a seamless way for users to make donations using Revolut. It combines the simplicity of Flask and the versatility of Node.js to offer a dependable and efficient service.

## Features ✨
- **User Authentication** 🔐
- **Donation Processing with Revolut** 💳
- **Admin Dashboard** 🛠️
- **Transaction History** 📈
- **Responsive Design** 📱💻

## Tech Stack 🖥️🚀
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python), Node.js (JavaScript)
- **Database**: SQLite (or your choice of database)
- **Payment Gateway**: Revolut

## Installation 🛠️
1. Clone the repository:
   ```bash
   git clone https://github.com/loyal812/donation-project.git
   cd donation-project
   ```

2. Set up the Flask backend:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the Node.js project:
   ```bash
   cd ../frontend
   npm install
   ```

4. Configure Revolut API keys in your environment variables.

5. Run the Flask backend server:
   ```bash
   flask run
   ```

6. Run the Node.js server:
   ```bash
   node app.js
   ```

## Usage 🎮
1. Navigate to your project directory.
2. Start the servers as mentioned in the installation section.
3. Open your web browser and visit `http://localhost:5000` for the Flask backend.
4. Interact with the frontend by visiting `http://localhost:3000` (or wherever your Node.js server is running).
