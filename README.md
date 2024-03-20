# CooksCorner
CooksCorner is an innovative offering designed to provide a convenient and inspiring experience in the world of cooking. Offering a variety of categories including an extensive list of recipes, CooksCorner creates a user-friendly platform for culinary enthusiasts. Immerse yourself in culinary delights with breathtaking photography, explore detailed recipe descriptions, and manage your culinary experience by saving, liking, and even creating your own dishes.
CooksCorner is your gateway to hassle-free and inspiring culinary adventures.

This repository is responsible for the backend part of the application.
### Technologies
---
- Python
- Django Rest Framework
- Cloudinary
- Swagger UI
- Nginx
- Docker

### Install
---
#### Without docker
1. Clone repository to your local machine:
```
git clone ssh/https-key
```
2. Create virtual environment and activate virtual environment:
- On `Windows`:
```
python -m env venv
```
```
venv\Scripts\activate.bat
```
- On `Linux/MacOs`
```
python3 -m env venv
```
```
source venv/bin/activate
```
3. Add `.env` file to the root and fill with your data next variables:
```
CLOUD_NAME = YOUR_CLOUD_NAME
CLOUD_API_KEY = YOUR_CLOUD_API_KEY
CLOUD_API_SECRET = YOUR_CLOUD_API_SECRET
SECRET_KEY = YOUR_SECRET_KEY
DEBUG = True
EMAIL_HOST_USER = YOUR_EMAIL
EMAIL_HOST_PASSWORD = YOUR_HOST_PASSWORD
EMAIL_LINK = 'http://127.0.0.1:8000/cookscorner/users/email-verify/?token='
EMAIL_LINK_PASSWORD = 'http://127.0.0.1:8000/cookscorner/users/change-password/?token='
```
4. Install all dependecies:
```
pip install -r requirements.txt
```
5. Run the project on your local host:
```
python/python3 manage.py runserver
```
### Authors
---
[Nursultan Kozhogulov, 2024](https://github.com/Nursultank00)