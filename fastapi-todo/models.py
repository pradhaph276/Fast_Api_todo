from sqlalchemy import Column,String,Boolean,Integer;
from database import Base

class Todo(Base):
    __tablename__="todos"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(String)
    completed=Column(Boolean,default=False)
