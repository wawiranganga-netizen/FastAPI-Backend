# Root cause of the runtime error in app.py

The app was crashing when the `add_student` route tried to insert a row into SQLite.

This has been fixed in [app.py](C:/Users/WAWIR/OneDrive/Desktop/backend/app.py) by keeping the SQLite connection and cursor separate.

## What is happening

In `add_student`, the code does this:

```python
connection = db_connection()
connection = connection.cursor()
connection.execute(
    """ INSERT INTO students (name, age, gender, email, school) VALUES (?, ?, ?, ?, ?)""",
    (
        student_data.name,
        student_data.age,
        student_data.gender,
        student_data.email,
        student_data.school
    )
)
connection.commit()
connection.close()
```

This is the problem:

- `db_connection()` returns a SQLite connection object.
- `connection.cursor()` returns a cursor object, not the original connection.
- The code reassigns `connection` to the cursor.
- After that, `connection.commit()` is called on the cursor, but `sqlite3.Cursor` does not have a `commit()` method.

That leads to the runtime error:

```python
AttributeError: 'sqlite3.Cursor' object has no attribute 'commit'
```

## Why this makes the app fail

The `add_student` function is executed when the API receives a POST request. Once the code reaches the commit, Python raises an exception and the request fails before the student is saved.

## Correct fix

Keep the connection and cursor separate:

```python
connection = db_connection()
cursor = connection.cursor()
cursor.execute(
    "INSERT INTO students (name, age, gender, email, school) VALUES (?, ?, ?, ?, ?)",
    (
        student_data.name,
        student_data.age,
        student_data.gender,
        student_data.email,
        student_data.school,
    ),
)
connection.commit()
cursor.close()
connection.close()
```

This keeps the `connection.commit()` call on the database connection object, where it is valid.
