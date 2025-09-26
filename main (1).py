from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    gender: str
    email: str

students: List[Dict[str, Union[str, int]]] = []
next_student_id = 1

@app.get("/students", response_model=List[Student], tags=["Students"])
def get_students():
    return students

@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int):
    for student in students:
        if student.get("id") == student_id:
            return student
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")

@app.post("/students", response_model=Student, status_code=201, tags=["Students"])
def add_student(student: Student):
    global next_student_id
    
    student_data = student.dict()
    student_data["id"] = next_student_id
    next_student_id += 1
    
    students.append(student_data)
    
    return student_data

@app.put("/students/{student_id}", response_model=Student, tags=["Students"])
def update_student(student_id: int, updated_details: Student):
    for index, student in enumerate(students):
        if student.get("id") == student_id:
            new_data = updated_details.dict()
            new_data["id"] = student_id
            students[index] = new_data
            return new_data
    
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")

@app.delete("/students/{student_id}", status_code=204, tags=["Students"])
def delete_student(student_id: int):
    global students
    
    original_length = len(students)
    students = [student for student in students if student.get("id") != student_id]
    
    if len(students) < original_length:
        return
    else:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")