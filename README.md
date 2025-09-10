# Prem-1B-SQL: Natural Language to SQL Queries

This project is part of my **Bachelor’s thesis** at the Faculty of Organization and Informatics.  
It implements a system that uses the **Prem-1B-SQL model** to translate natural language into SQL queries, which are then executed on a custom-built database.

---

## 📂 Project Structure
- **`database/`**  
  - `database.py` -> script for creating the database  
  - `database.db` -> the database file itself  
- `main.py` -> runs the model in the terminal (prints results directly)
- `main_UI.py` -> runs the model with a simple graphical interface
- `requirements.txt` -> contains all the dependencies required for the project

---

## ⚙️ Setup & Installation
This project was developed in a virtual environment.  
All required dependencies are listed in **`requirements.txt`**.  

To run the project:  
```bash
# 1. Create a virtual environment
# 2. Install dependencies
pip install -r requirements.txt
```

---

## 📖 Reference
This project is based on [PremAI’s PremSQL](https://github.com/premAI-io/premsql).
