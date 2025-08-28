# User Management API (FastAPI + MongoDB)

A production-style User Management API built with **FastAPI**, **Beanie ODM**, and **JWT** auth.

## Features
- Register, login, profile, RBAC, pagination
- MongoDB backend (works with MongoDB Compass)
- Seed admin user
- Tests with pytest

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## 🗄️ Database Setup (MongoDB + Compass)

This project uses **MongoDB** as its database, via the **Beanie ODM**.

### Local Setup (default)
- Make sure MongoDB is installed and running on your machine (`mongodb://localhost:27017`).
- The default database name is `userdb`.
- MongoDB Compass can connect locally with:
  ```
  mongodb://localhost:27017/userdb
  ```

### Remote Setup (for teammates using MongoDB Compass)
If you want teammates to connect remotely:

1. **Enable remote access**
   - Edit `/etc/mongod.conf` → set:
     ```yaml
     net:
       bindIp: 0.0.0.0
     security:
       authorization: enabled
     ```
   - Restart MongoDB:
     ```bash
     sudo systemctl restart mongod
     ```

2. **Create an admin user**
   ```js
   use admin
   db.createUser({
     user: "admin",
     pwd: "StrongPassword123!",
     roles: [ { role: "root", db: "admin" } ]
   })
   ```

3. **Restrict firewall to teammate IPs**
   Example (Ubuntu UFW):
   ```bash
   sudo ufw allow from 203.0.113.25 to any port 27017
   ```

4. **Share connection string**
   Teammates can connect with MongoDB Compass using:
   ```
   mongodb://admin:StrongPassword123!@<SERVER_IP>:27017/userdb?authSource=admin
   ```

5. **Use same string in `.env`**
   In `.env`, set:
   ```ini
   DATABASE_URL=mongodb://admin:StrongPassword123!@<SERVER_IP>:27017/userdb?authSource=admin
   ```

This way, **both Compass and FastAPI** use the same connection string.

## Seed admin
```bash
python -m app.seed_admin
```

## Run tests
```bash
pytest -q
```


## ⭐ Bonus Features Implemented

### 1. Refresh Tokens & Logout
- `/refresh` endpoint issues a new access token if a valid refresh token is provided.
- `access_token` (default 60min), `refresh_token` (7 days).

**Example:**
```bash
http POST :8000/login email=alice@example.com password=StrongPass!234
http POST :8000/refresh refresh_token=<REFRESH_TOKEN>
```

---

### 2. Password Reset (Change Password)
- `/users/change-password` (auth required).
- User provides `old_password` and `new_password`.
- Password is re-hashed securely.

**Example:**
```bash
http POST :8000/users/change-password "Authorization:Bearer <TOKEN>" old_password=OldPass new_password=NewPass123!
```

---

### 3. Docker Compose Setup
- Includes `Dockerfile` + `docker-compose.yml` for running API + MongoDB.

**Run:**
```bash
docker-compose up --build
```

- API → http://localhost:8000
- MongoDB → mongodb://localhost:27017 (can connect via Compass)
 
### 4. Time Spend
- Approx. 3-4 hours in total:
- 10 min → Setup (env, FastAPI, MongoDB)
- 2h → Coding register & login and User endpoints
- 1hr → Testing endpoints and GitHub setup and fixes