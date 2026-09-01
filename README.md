# NotifyFlow - Notification System

## Tech Stack
- Backend: Django REST Framework + PyMongo
- Database: MongoDB Atlas
- Frontend: React / Next.js (Assuming built separately)
- Email: Postmark
- WhatsApp: WhatsApp Cloud API
- Web Push: OneSignal

## Deployment (Render)
1. Add environment variables:
   `MONGODB_URI`, `MONGODB_DATABASE`, `SECRET_KEY`, `JWT_SECRET`, etc.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `cd backend && gunicorn config.wsgi:application`

## Environment Variables
See `.env.example` for all required environment variables.

## Admin Login
To log in as admin, an admin user must be created first.
Use the API directly or run a script to create an admin user:
```bash
python manage.py shell
```
```python
from accounts.services import AccountService
AccountService.register_user("Admin", "admin@example.com", "+1234567890", "admin123", role="ADMIN")
```
Then log in via the `/api/accounts/login/` endpoint with:
`email`: admin@example.com
`password`: admin123

## Supported Triggers
- `login`: Fired when user logs in.
- `logout`: Fired when user logs out.
- `not_logged_in_1_day`: Fired for inactivity.
- `not_logged_in_1_week`: Fired for longer inactivity.
