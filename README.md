🏠 Application Components

1.  **Frontend (Client-side)**
    Responsible for the User Interface (UI) and user interactions.

    **Role**: Data input (postal code, size, number of bedrooms), data display (prediction results, sample data, model details), and handling user operations.

    **Technologies**:
    *   **HTML**: Defines the structure of the page.
    *   **CSS**: Defines the styles (appearance).
    *   **JavaScript**: Handles user interactions, manages input values, and sends requests to the backend API.

    **Image**: All elements displayed on the screen, such as dropdown menus, sliders, buttons, and result display panels, are frontend functionalities.

2.  **Backend (Server-side)**
    Responsible for data processing, machine learning model execution, and data persistence.

    **Role**:
    *   **API Provision**: Provides endpoints (URLs) to receive requests from the frontend (e.g., "Calculate rent for this property").
    *   **Machine Learning Model Hosting/Execution**: Loads the trained rent prediction model (e.g., Multiple Linear Regression model) and passes input data received from the frontend (postal code, size, number of bedrooms) to the model for prediction.
    *   **Data Management**: Manages static data such as sample data and model details, or dynamic data like user accounts in the future.

    **Technologies**:
    *   **Programming Language**: Python (Flask), Node.js (Express), C# (.NET), Java (Spring), etc.
    *   **Machine Learning Libraries (for Python)**: Scikit-learn (used for implementing the Multiple Linear Regression model), Pandas (for data processing).
    *   **Web Framework**: Configures API endpoints and handles server-side logic.

⚙️ Data Flow (During Prediction)

*   **Input**: The user enters property details (e.g., 56789, 1500 sq ft, 1 bed) on the frontend (browser) and clicks the "CALCULATE RENT" button.
*   **Request**: The frontend JavaScript sends an HTTP request (usually a POST request) to the backend API, including the input data.
*   **Prediction**: The backend server receives the request, passes the input values to the internally hosted machine learning model. The model outputs the predicted rent (e.g., $1,890).
*   **Response**: The backend returns an HTTP response containing the prediction result to the frontend.
*   **Display**: The frontend receives the response and displays the result on the screen.

**Conclusion**: The rent prediction application functions by the collaboration of the backend, which executes the prediction logic, and the frontend, which handles user interaction.

---

## Setup and Deployment

This section provides instructions for running the application locally or deploying it to Heroku.

### Prerequisites

*   Python 3.x
*   pip (Python package installer)
*   Git
*   Heroku CLI (for deploying to Heroku)

### Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/takashim0101/Home-Rental-Estimator.git
    cd Home-Rental-Estimator
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    python -m flask run
    ```
    Access `http://127.0.0.1:5000/` in your browser.

### Deployment to Heroku

To deploy to Heroku, you need a Heroku account and the Heroku CLI.

1.  **Install Heroku CLI and Log In**:
    Install the Heroku CLI from [Heroku Dev Center](https://devcenter.heroku.com/articles/heroku-cli) and log in with:
    ```bash
    heroku login
    ```

2.  **Install Gunicorn and update requirements.txt**:
    Gunicorn is the WSGI server for running Flask apps on Heroku.
    ```bash
    pip install gunicorn
    pip freeze > requirements.txt
    ```

3.  **Create a Procfile**:
    Create a file named `Procfile` (no extension) in the root directory of your project with the following content:
    ```
    web: gunicorn app:app
    ```

4.  **Initialize Git repository and commit**:
    If your project is not yet a Git repository or you haven't committed your changes:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```

5.  **Create a Heroku application**:
    ```bash
    heroku create <your-app-name>
    # Or, to auto-generate an app name
    heroku create
    ```

6.  **Deploy to Heroku**:
    ```bash
    git push heroku main
    ```
    (If you are using the `master` branch instead of `main`, use `git push heroku master`.)

7.  **Verify the application**:
    ```bash
    heroku open
    ```
    This will open your deployed application in your browser.
