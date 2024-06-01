# SportEvents
A web application designed to connect people doing sports. Users can find and join sports events around them, or create their own events to invite others.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3 installed
- Node.js installed

## Building and Running
Follow these steps to get your development environment set up:

**Clone the repository:**
   ```bash
   git clone https://github.com/jakmro/Sportevent.git
   cd Sportevent
   ```

**Run the Application**
To start the application, run:
```bash
make
```
This will install all required libraries, set up the database, create a `.env` file, and start the server on `http://localhost:8000`.

## Services
### API Keys
**Google API Key**: This application uses Google Maps for location services. To obtain a Google API key:
1. Visit [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Navigate to "APIs & Services" > "Credentials".
4. Click "Create Credentials" and follow the prompts to generate a new API key.
5. Insert your key into the `.env` file as follows:
    ```
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
    ```

### Email Configuration
**Setting Up Email Notifications**: To enable email functionalities:
1. Use your Gmail account and navigate to [Google Account Security](https://myaccount.google.com/security) to generate an app-specific password.
2. Add your email and the generated password to the `.env` file:
    ```
    EMAIL_ADDRESS=YOUR_GMAIL_ADDRESS
    EMAIL_PASSWORD=YOUR_GMAIL_GENERATED_PASSWORD
    ```
