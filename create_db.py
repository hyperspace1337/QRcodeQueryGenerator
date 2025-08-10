from database import Base, engine
from models import Consumable

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

print("Таблицы созданы!")