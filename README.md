# Restaurant Inventory Management App

A mobile-optimized web application for tracking restaurant inventory and sending SMS notifications when items need to be restocked.

## Features

- Track inventory items across multiple categories
- Perform inventory checks and mark items as "OK", "Low Stock", or "Out of Stock"
- Send SMS notifications to managers about items that need attention
- Mobile-responsive design for easy use on smartphones and tablets

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   gunicorn src.main:app
   ```

## Environment Variables

For production deployment, you may want to set the following environment variables:

- `SECRET_KEY`: A random string for security
- `TWILIO_ACCOUNT_SID`: Your Twilio account SID (for SMS)
- `TWILIO_AUTH_TOKEN`: Your Twilio auth token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number

## Deployment on Render

This application is configured for easy deployment on Render.com:

1. Connect this GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.main:app`
4. Add any necessary environment variables
5. Deploy!
