# AI-Expense-Tracker-for-smart-finance
AI-Powered Expense Tracker
This is not just another expense tracker. This application leverages a suite of six specialized machine learning models to provide deep, actionable insights into your financial health. From predicting disposable income to detecting overspending and recommending personalized budgets, this tool is designed to be your intelligent financial co-pilot

Table of Contents
The AI Core: Six Intelligent Models
Tech Stack & Architecture
Setup and Installation
Future Improvements
Contact
The AI Core: Six Intelligent Models
The power of this application lies in its ensemble of machine learning models, each trained for a specific financial analysis task.

1. Random Forest Regressor – Expense Prediction Model
This model is designed to predict users' disposable income based on key financial indicators such as income, rent, savings efficiency, and essential/non-essential expenses. By leveraging the Random Forest Regressor, it provides accurate, continuous predictions of how much money a user will have left after covering their expenses. This helps in proactive financial planning and budgeting.

2. XGBoost Classifier – Overspending Detection Model
The XGBoost Classifier is used to flag users who are likely overspending. It analyzes behavioral and financial features like total expenses, rent-to-income ratio, and savings efficiency to classify users into two categories: Overspending or Not Overspending. This model enables real-time alerts, encouraging users to manage expenses before it becomes a problem.

3. Isolation Forest – Anomaly Detection in Financial Behavior
This model automatically detects users with unusual financial behavior by analyzing patterns in their income, expenses, savings efficiency, and expense ratios. It flags anomalies such as excessive spending or poor saving habits — even without needing predefined labels. Unlike a regression model, it doesn’t predict values. Instead, it classifies data points as normal or anomalous using unsupervised learning.

4. Decision Tree Classifier – Savings Target Efficiency
This model is a binary classification decision tree trained to predict if a person meets their savings goals. Instead of predicting exact savings amounts (regression), it predicts a simple yes/no outcome — did they achieve their target or not? This is better for quick, actionable insights. The model achieves near-perfect accuracy by focusing mainly on disposable income and potential savings, showing these are critical signals for saving success.

5. XGBoost Regressor – Financial Health Score
This model uses XGBoost’s gradient boosting regression to predict a composite Financial Health Score over monthly user data. Unlike simple regressors, XGBoost builds an ensemble of decision trees iteratively to capture complex, nonlinear relationships between income, expenses, debt, and savings efficiency, achieving an R² of 0.97. This approach is essential for modeling the nuanced and fluctuating nature of individual financial health.

6. Random Forest Regressor – Personalized Spending Recommender
This model uses machine learning to help users plan their budgets more effectively. It uses a dataset of user financials, engineers features like savings gap and expense ratios, and then groups users into behavioral clusters. A Random Forest Regressor predicts how much a user should aim to save, and finally, it generates spending recommendations (Rent, Groceries, Savings, etc.) tailored to the user’s income level and habits.

Tech Stack & Architecture
This project utilizes a modern, full-stack architecture to deliver a seamless experience.

Frontend: Streamlit (For rapid, data-centric UI development)
Backend: Django & Django REST Framework (For robust business logic and API creation)
Database: MySQL (For reliable and scalable data storage)
Machine Learning: Scikit-learn, XGBoost, Pandas, NumPy
Application Flow
The user interacts with the Streamlit frontend.
Streamlit sends API requests to the Django backend.
Django queries the MySQL database for the required user financial data.
Django loads the appropriate pre-trained ML model (.pkl or .joblib file).
The data is passed to the model, which returns a prediction, classification, or score.
Django sends the result back to the Streamlit frontend, which visualizes the insight for the user.
Setup and Installation
This is a full-stack application. Follow these steps carefully to set up the environment.

Prerequisites
Python 3.8+
Git
MySQL Server: You must have a MySQL server instance installed and running on your machine.
1. Clone the Repository
git clone [https://github.com/Srinidhi945/AI-Powered-Expense-Tracker.git](https://github.com/Srinidhi945/AI-Powered-Expense-Tracker.git)
cd AI-Powered-Expense-Tracker
2. Backend Setup (Django & MySQL)
This sets up the database, dependencies, and API server.

Navigate to Backend & Create Virtual Environment:

cd Expense-Tracker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Python Dependencies:

pip install -r requirements.txt
Set Up MySQL Database:
Log in to your MySQL server.

Create a new database for the project: CREATE DATABASE budget_db;

Create a .env file in the /backend directory to store your database credentials securely. Add the following content in setting.py, replacing the placeholder values:

DB_NAME=budget_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
Ensure your Django settings.py is configured to read from this .env file.

Run Database Migrations:

python manage.py migrate
Make migration

python manage.py makemigrations
Start the Django Server: The backend will run on http://127.0.0.1:8000

python manage.py runserver
Frontend Setup (Streamlit) This sets up the user interface. Open a new terminal for this part.
Navigate to Frontend & Install Dependencies: From the project root directory

cd frontend
pip install -r requirements.txt
Start the Streamlit App: The frontend will run on http://localhost:8501

streamlit run main.py
Usage With both servers running, open your browser and navigate to http://localhost:8501 to use the application.
Future Improvements
Real-time Data Ingestion: Connect to bank accounts via APIs like Plaid for automatic transaction updates.

Enhanced Visualizations: Use more advanced charting libraries for deeper data exploration.

Mobile Application: Develop a native mobile app for on-the-go expense tracking.

Cloud Deployment: Deploy the entire stack to a cloud provider like AWS or GCP.
