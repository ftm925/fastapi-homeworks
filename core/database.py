from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey

db_url = "sqlite:///appdb.db"

# Create database connectiosn
engine = create_engine(db_url, connect_args={"check_same_thread": False})
session_local = sessionmaker(engine, autoflush=False, autocommit=False)

# Define tables
Base = declarative_base()

class Expense(Base):

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    cost = Column(Float, nullable=False)
    description = Column(String(50), nullable=False)    

    def __repr__(self)->str:
        return f"Expense(id={self.id}, cost={self.cost}, description={self.description})"
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def get_db():
    db = session_local()
    try:    
        #return database session
        yield db

    finally:
        #close session finally
        db.close()
