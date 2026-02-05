from sqlalchemy import Column, Integer, String, BigInteger, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Visualizer(Base):
    __tablename__ = "VISUALIZER"

    id = Column(Integer, primary_key=True, index=True)
    algo = Column(String(50), nullable=False)
    items = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=False)
    start_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False)
    total_time_ms = Column(BigInteger, nullable=False)
    time_complexity = Column(String(20), nullable=False)
    graph_data = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
