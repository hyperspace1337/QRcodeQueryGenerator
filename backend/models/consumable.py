from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class ConsumableModel(Base):
    __tablename__ = "consumables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(100))
    erp_code: Mapped[str] = mapped_column(String(10))
    qty: Mapped[int] = mapped_column(Integer)
    department: Mapped[str] = mapped_column(String(100))


