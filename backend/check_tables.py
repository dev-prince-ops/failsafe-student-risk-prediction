# backend/check_tables.py

from app.models import User, Student, Intervention

print(User.__tablename__)
print(Student.__tablename__)
print(Intervention.__tablename__)