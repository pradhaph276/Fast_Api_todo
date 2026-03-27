from fastapi import FastAPI, Depends, HTTPException
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, Base, engine
from models import Todo
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE POST Task
@app.post("/todos", response_model=TodoSchema)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# Get all Todos

@app.get("/todos", response_model=List[TodoSchema])
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos


#Get Signle Id
@app.get("/todos/{todo_id}", response_model=TodoSchema)
def get_single_todo(todo_id: int, db: Session = Depends(get_db)):
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    return todo

# update single todo Id
@app.put("/todos/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, updated_data: TodoCreate, db: Session = Depends(get_db)):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    update_data = updated_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)

    return todo

#  delete methods
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    db.delete(todo)
    db.commit()

    return {"message": "Todo Deleted Successfully"}
