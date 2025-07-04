# 🏋️ Fitness Studio Booking API

## 📌 Features

- View fitness classes
- Book slots
- Get bookings by email
- IST to UTC timezone-aware scheduling

## 🚀 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Seed data
python seed.py

# Run the server
python run.py
```

## 📮 Sample API Usage

### GET /classes
```bash
curl http://localhost:5000/classes?tz=Asia/Kolkata
```

### POST /book
```bash
curl -X POST http://localhost:5000/book -H "Content-Type: application/json" -d '{
  "class_id": 1,
  "client_name": "John",
  "client_email": "john@example.com"
}'
```

### GET /bookings
```bash
curl http://localhost:5000/bookings?email=john@example.com
```

## ✅ Timezone Support

- Classes stored in UTC
- Supports custom timezone using `?tz=...` (defaults to IST)
