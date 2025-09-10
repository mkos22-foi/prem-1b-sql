from premsql.generators import Text2SQLGeneratorHF
from premsql.executors import SQLiteExecutor
import customtkinter as ctk


executor = SQLiteExecutor()
generator = Text2SQLGeneratorHF(
    model_or_name_or_path="premai-io/prem-1B-SQL",
    experiment_name="NL2SQL_UI",
    device="cpu",
    type="NL2SQL_UI"
)


db_path = "database/database.db"
schema = """
players(player_id, name, birthdate, goalkeeper, defender, midfielder, forward, active, injured, phone)
coaches(coach_id, name, phone)
teams(team_id, name)
seasons(season_id, name, start_yr, end_yr)
competitions(competition_id, season_id, name, type, level)
trainings(training_id, team_id, date, start_time, duration_min, focus)
coachassignment(coach_id, training_id, head, assistant, fitness)
trainingattendance(player_id, training_id, notes)
teammembership(team_id, player_id, start_date, end_date)
matches(match_id, competition_id, team_id, opponent_team, time, location, our_goals, opponent_goals)
matchattendance(player_id, match_id, minutes_played, goals, assists, saves, yellow_cards, red_cards)"""

def displayLoading(loading):
    if loading:
        lblLoading.configure(text="Loading...")
    else:
        lblLoading.configure(text="")

def displayResult(text):
    txtResults.configure(state="normal")
    txtResults.delete("1.0", "end")
    txtResults.insert("1.0", text)
    txtResults.configure(state="disabled")


def onClick():
    question = txtEntry.get()
    if not question:
        displayResult("Please enter a question.")
        return

    displayLoading(True)
    displayResult("")
    lblLoading.update()

    prompt = f"""Your task is to convert natural-language question to SQL query for SQLite database. Only use tables and columns defined in database schema. Only generate one query!

    # Database schema:
    {schema}

    # Additional information:
    Columns head, assistant and fitness in table coachassignment are BOOLEAN values (0 or 1).
    Columns goalkeeper, defender, midfielder and forward in table players are BOOLEAN values (0 or 1).
    Columns active and injured in table players are BOOLEAN values (0 or 1).
    Use 1 for true and 0 for false. Only use those columns if they are in the question!

    # Natural-language question that needs to be translated into SQL query:
    {question}

    # Generated SQL query:
    """

    try:
        sql_query = generator.generate(
            data_blob={
                "prompt": prompt, 
                "db_path": db_path},
            do_sample=False,
            max_new_tokens=256
        )
        result = executor.execute_sql(
            sql=sql_query, 
            dsn_or_db_path=db_path
        )

        if result and not result["error"] and result["result"]:
            rows = []
            for row in result["result"]:
                values = []
                for col in row:
                    values.append(str(col))
                rows.append(", ".join(values))
            displayResult("\n".join(rows))
        else:
            displayResult("Sorry, I couldn't find anything...")

    except Exception as e:
        displayResult(f"Error: {e}")

    finally:
        displayLoading(False)
        lblLoading.update()


app = ctk.CTk()
app.title("Prem-1B-SQL")
app.geometry("1000x1200")
app.resizable(False, False)
app.configure(fg_color="#1f2421")

lblHead = ctk.CTkLabel(app, text="Club Management", font=("Arial", 80, "bold"), text_color="#95c07b")
lblHead.grid(row=0, column=0, padx=24, pady=(45, 40))

lblQuestion = ctk.CTkLabel(app, text="What do you want to know?", font=("Arial", 40), text_color="#e6e6e6")
lblQuestion.grid(row=1, column=0, pady=(6, 6))

txtEntry = ctk.CTkEntry(app, placeholder_text="Enter your question here...", width=760, font=("Arial", 30), fg_color="#262b28", text_color="#e6e6e6", border_width=2, border_color="#3a423e", placeholder_text_color="#9aa5a0")
txtEntry.grid(row=2, column=0, padx=24, pady=(14, 10))

btnSearch = ctk.CTkButton(app, text="Search", command=onClick, font=("Arial", 40, "bold"), width=220, height=60, fg_color="#7fb069", hover_color="#95c07b", text_color="black", border_color="#3a423e", border_width=1)
btnSearch.grid(row=3, column=0, pady=(15, 15))

lblLoading = ctk.CTkLabel(app, text="", font=("Arial", 30), text_color="#9aa5a0")
lblLoading.grid(row=4, column=0, pady=(0, 8))

lblResults = ctk.CTkLabel(app, text="Results:", font=("Arial", 40, "bold"), text_color="#e6e6e6")
lblResults.grid(row=5, column=0, pady=(5, 6))

txtResults = ctk.CTkTextbox(app, font=("Arial", 30), width=900, height=900, fg_color="#262b28", text_color="#e6e6e6", border_width=2, border_color="#7fb069")
txtResults.grid(row=6, column=0, padx=24, pady=(0, 24))
txtResults.configure(state="disabled")

app.grid_columnconfigure(0, weight=3)
app.grid_rowconfigure(6, weight=3)

app.mainloop()
