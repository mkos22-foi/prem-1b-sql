from premsql.generators import Text2SQLGeneratorHF
from premsql.executors import SQLiteExecutor

executor = SQLiteExecutor()

generator = Text2SQLGeneratorHF(
    model_or_name_or_path="premai-io/prem-1B-SQL",
    experiment_name="NL2SQL",
    device="cpu",
    type="NL2SQL"
)

question = "Show me names of all players"
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

prompt = f"""
Your task is to convert natural-language question to SQL query for SQLite database. Only use tables and columns defined in database schema. Only generate one query!

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

def generating_sql(prompt_):
    return generator.generate(
        data_blob={
            "prompt": prompt_,
            "db_path": db_path
        },
        do_sample = False,
        max_new_tokens=256,
        executor=executor
    )

def executing_sql(sql_):
    return executor.execute_sql(
        sql=sql_,
        dsn_or_db_path=db_path
    )

def print_response(result_):
     for row in result_['result']:
         values = []
         for col in row:
             values.append(str(col))
         print(", ".join(values))

sql_query = generating_sql(prompt)
print("\n")
print("---------- Generated SQL query ----------")
print(sql_query)
print("\n")
print("---------- Execution of generated SQL query ----------")
sql_result = executing_sql(sql_query)
print(sql_result)
print("\n")
print("---------- Cleaner output ----------")
print_response(sql_result)
print("\n")





