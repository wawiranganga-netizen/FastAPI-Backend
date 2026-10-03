from fastapi import FastAPI
from pydantic import BaseModel  
import sqlite3


app = FastAPI()


        
        
def db_connection():
    my_database = "eunice.db"
    connection = sqlite3.connect(my_database)
    connection.row_factory = sqlite3.Row
    return connection


    
def create_table():
    connection = db_connection()
    connection.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            email TEXT NOT NULL unique,
            school TEXT NOT NULL,
            Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    connection.commit()
    connection.close()
create_table()

class Student(BaseModel):
        name: str
        age: int
        gender: str
        email: str
        school: str
        
        


@app.get("/")
def home():
    return {"message": "Api is working perfectly"}

@app.post("/add_student")
def add_student(student: Student):
    
    student_data = student
    
    
    
    
    connection = db_connection()
    connection= connection.cursor()
    connection.execute(
        """ INSERT INTO students (name, age, gender, email, school) VALUES (?, ?, ?, ?, ?)""",
        
    (
        student_data.name,
        student_data.age,   
        student_data.gender,
        student_data.email,
        student_data.school
        
        
    ))
    connection.commit()
    connection.close()
    return{"message":"student added successfully "}