# Creaing Vertual Environment
```bash
python -m venv venv
```

# Installing Requirements
```bash
pip install -r requirements.txt
```

# Running the Server
```bash
python manage.py runserver
```

# Creating SuperUser
```bash
python manage.py createsuperuser
```

# Already Created SuperUser
- username: `admin`
- password: `admin`

# JSON Web Token Authentication -> access_token, refresh_token
## Must add a Header in request
###  Header Name: Authorization
## Example:
### `Authorization: JWT access_token`

# API Endpoints
## Related to books
### http://127.0.0.1:8000/books/
### http://127.0.0.1:8000/books/1
## Related to book reviews
### http://127.0.0.1:8000/books/1/reviews
### http://127.0.0.1:8000/books/1/reviews/1
## Related to book rating
### http://127.0.0.1:8000/books/1/ratings
### http://127.0.0.1:8000/books/1/reviews/1
## Related to profiles
### http://127.0.0.1:8000/profiles/  -> login required
### http://127.0.0.1:8000/profiles/1  -> login required(Moderator and Admin Only)
### http://127.0.0.1:8000/profiles/me  -> login required(Current User's Profile Info)
## Related to login
### http://127.0.0.1:8000/auth/jwt/create -> login
### http://127.0.0.1:8000/auth/jwt/refresh -> login
## Related to users
### http://127.0.0.1:8000/auth/users -> signup(Creating a New User)
### http://127.0.0.1:8000/auth/users -> login required(Moderator and Admin Only)
### http://127.0.0.1:8000/auth/users/1 -> login required(Moderator and Admin Only)
### http://127.0.0.1:8000/auth/users/me/ -> login required(Current User Info)