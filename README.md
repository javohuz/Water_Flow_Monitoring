# Suv Oqimini Monitoring Loyihasi / Water Flow Monitoring Project

Bu loyiha real vaqtli suv oqimini kuzatish uchun yaratilgan bo‘lib, Django orqali backend, HTML/CSS/JS orqali frontend va sensorli tizim bilan ishlash uchun moslashtirilgan.

This project is designed to monitor water flow in real-time, with a Django backend and HTML/CSS/JS frontend, optionally integrated with sensor systems.

---

## Clone & Ishga Tushurish / Run the Project

### Klonlash / Cloning:
```bash
git clone https://github.com/javohuz/Water_Flow_Monitoring.git
cd suv_nazorat/backend
```

### Virtual Muhit / Virtual Environment:
```bash
python3 -m venv venv
```

### Aktivlashtirish / Activate:
**Linux/Mac:**
```bash
source venv/bin/activate
```
**Windows:**
```bash
venv\Scripts\activate
```

### Kutubxonalarni o'rnatish / Install Requirements:
```bash
pip install -r requirements.txt
```

### Migratsiyalar / Database Migration:
```bash
python manage.py migrate
```

### Serverni ishga tushurish / Run the Development Server:
```bash
python manage.py runserver
```

Admin panel: http://127.0.0.1:8000/admin/  
Asosiy sahifa: http://127.0.0.1:8000/

---

## Funktsiyalar / Features:

- Suv sathini o‘lchash va avtomatik hisoblash (h, A, P, R, V, Q)
- Har 5 daqiqada yangi o‘lchov (real vaqtli yozuv)
- Soatlik, haftalik va oylik o‘rtacha natijalar
- Jadval va grafik orqali ko‘rsatish
- Telegram orqali avtomatik ogohlantirish (past yoki yuqori suv sathi holatida)

---
