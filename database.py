import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()


# Creating tables
cur.execute("""CREATE TABLE IF NOT EXISTS players(
            player_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birthdate TEXT NOT NULL,
            goalkeeper BOOLEAN NOT NULL DEFAULT FALSE,
            defender BOOLEAN NOT NULL DEFAULT FALSE,
            midfielder BOOLEAN NOT NULL DEFAULT FALSE,
            forward BOOLEAN NOT NULL DEFAULT FALSE,
            active BOOLEAN NOT NULL DEFAULT FALSE,
            injured BOOLEAN NOT NULL DEFAULT FALSE,
            phone TEXT,
            CHECK (goalkeeper + defender + midfielder + forward = 1),
            CHECK (active + injured = 1))""")

cur.execute("""CREATE TABLE IF NOT EXISTS coaches(
            coach_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS teams(
            team_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS seasons(
            season_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            start_yr TEXT NOT NULL,
            end_yr TEXT NOT NULL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS competitions(
            competition_id INTEGER PRIMARY KEY,
            season_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            level TEXT NOT NULL,
            FOREIGN KEY(season_id) REFERENCES seasons(season_id))""")

cur.execute("""CREATE TABLE IF NOT EXISTS trainings(
            training_id INTEGER PRIMARY KEY,
            team_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration_min INTEGER NOT NULL,
            focus TEXT NOT NULL,
            FOREIGN KEY(team_id) REFERENCES teams(team_id))""")

cur.execute("""CREATE TABLE IF NOT EXISTS coachassignment(
            coach_id INTEGER NOT NULL,
            training_id INTEGER NOT NULL,
            head BOOLEAN NOT NULL DEFAULT FALSE,
            assistant BOOLEAN NOT NULL DEFAULT FALSE,
            fitness BOOLEAN NOT NULL DEFAULT FALSE,
            CHECK (head + assistant + fitness = 1),
            PRIMARY KEY(coach_id, training_id),
            FOREIGN KEY(coach_id) REFERENCES coaches(coach_id),
            FOREIGN KEY(training_id) REFERENCES trainings(training_id))""")

cur.execute("""CREATE TABLE IF NOT EXISTS trainingattendance(
            player_id INTEGER NOT NULL,
            training_id INTEGER NOT NULL,
            notes TEXT,
            PRIMARY KEY(player_id, training_id),
            FOREIGN KEY(player_id) REFERENCES players(player_id),
            FOREIGN KEY(training_id) REFERENCES trainings(training_id))""")

cur.execute("""CREATE TABLE IF NOT EXISTS teammembership(
            team_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            PRIMARY KEY(team_id, player_id),
            FOREIGN KEY(team_id) REFERENCES teams(team_id),
            FOREIGN KEY(player_id) REFERENCES players(player_id))""")

cur.execute("""CREATE TABLE IF NOT EXISTS matches(
            match_id INTEGER PRIMARY KEY,
            competition_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            opponent_team TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT NOT NULL,
            our_goals INTEGER NOT NULL DEFAULT 0 CHECK(our_goals >= 0),
            opponent_goals INTEGER NOT NULL DEFAULT 0 CHECK(opponent_goals >= 0),
            FOREIGN KEY(competition_id) REFERENCES competitions(competition_id),
            FOREIGN KEY(team_id) REFERENCES teams(team_id))""")

cur.execute("""CREATE TABLE IF NOT EXISTS matchattendance(
            player_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            minutes_played INTEGER NOT NULL DEFAULT 0,
            goals INTEGER NOT NULL DEFAULT 0,
            assists INTEGER NOT NULL DEFAULT 0,
            saves INTEGER NOT NULL DEFAULT 0,
            yellow_cards INTEGER NOT NULL DEFAULT 0 CHECK(yellow_cards BETWEEN 0 AND 2),
            red_cards INTEGER NOT NULL DEFAULT 0 CHECK(red_cards IN (0,1)),
            PRIMARY KEY(player_id, match_id),
            FOREIGN KEY(player_id) REFERENCES players(player_id),
            FOREIGN KEY(match_id) REFERENCES matches(match_id))""")

# Unos zapisa:
players = [
    # id, name, birthdate, GK, DF, MF, FW, Active, Injured, phone
    (1, "Mario Mccann", "1.1.2000.", 1, 0, 0, 0, 1, 0, "0919724501"),
    (2, "Remi Huffman", "1.2.2000.", 0, 1, 0, 0, 1, 0, "0919724502"),
    (3, "Aamir Haas", "1.3.1998.", 0, 0, 1, 0, 0, 1, "0919724503"),
    (4, "Tomasz Robbins", "1.4.1999.", 0, 0, 0, 1, 1, 0, "0919724504"),
    (5, "Brodie Webb", "1.5.2001.", 0, 1, 0, 0, 1, 0, "0919724505"),
    (6, "Haider O'Quinn", "1.6.1998.", 0, 0, 1, 0, 1, 0, "0919724506"),
    (7, "Caleb Lindsay", "1.7.2001.", 0, 0, 0, 1, 0, 1, "0919724507"),
    (8, "Gary Castillo", "7.1.2010.", 1, 0, 0, 0, 1, 0, "0919724508"),
    (9, "Virgil Pearson", "8.1.2010.", 0, 1, 0, 0, 0, 1, "0919724509"),
    (10, "Azaan Robertson", "9.1.2009.", 0, 0, 1, 0, 1, 0, "0919724510"),
    (11, "Phillip Yang", "10.1.2009.", 0, 0, 0, 1, 1, 0, "0919724511"),
    (12, "Jordan Frank", "11.1.2008.", 0, 1, 0, 0, 1, 0, "0919724512"),
    (13, "Damian Padilla", "12.1.2008.", 0, 0, 1, 0, 0, 1, "0919724513"),
    (14, "Sion Hill", "2.2.2010.", 0, 0, 0, 1, 1, 0, "0919724514"),
]
for player in players:
    cur.execute("""INSERT INTO players(player_id, name, birthdate, goalkeeper, defender, midfielder, forward, active, injured, phone) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", player)

coaches = [
    (1, "Coach Everly", "0991111111"),
    (2, "Coach Ishaq", "0992222222"),
    (3, "Coach Cameron", "0993333333"),
    (4, "Coach Umar", "0994444444"),
    (5, "Coach Dennis", "0995555555")
]
for coach in coaches:
    cur.execute("INSERT INTO coaches(coach_id, name, phone) VALUES(?, ?, ?)", coach)

teams = [
    (1, "Seniors"),
    (2, "U19")
]
for team in teams:
    cur.execute("INSERT INTO teams(team_id, name) VALUES(?, ?)", team)

seasons = [
    (1, "2024/25", "2024", "2025"),
    (2, "2025/26", "2025", "2026")
]
for season in seasons:
    cur.execute("INSERT INTO seasons(season_id, name, start_yr, end_yr) VALUES(?, ?, ?, ?)", season)

competitions = [
    (1, 1, "Croatian League", "League", "Senior"),
    (2, 1, "Croatian Cup", "Cup", "Junior"),
    (3, 2, "Croatian Cup", "Cup", "Senior"),
    (4, 2, "Croatian League", "League", "Junior")
]
for competition in competitions:
    cur.execute("INSERT INTO competitions(competition_id, season_id, name, type, level) VALUES(?, ?, ?, ?, ?)", competition)

trainings = [
    (1, 1, "1.1.2025", "20:00", 120, "Possession"),
    (2, 1, "2.1.2025", "21:00", 60, "Condition"),
    (3, 1, "4.1.2025", "10:00", 120, "Ball control"),
    (4, 1, "5.1.2025", "12:00", 120, "Tactics"),
    (5, 1, "6.1.2025", "9:00", 60, "Recovery"),
    (6, 2, "1.1.2025", "18:00", 120, "Possession"),
    (7, 2, "2.1.2025", "20:00", 60, "Condition"),
    (8, 2, "4.1.2025", "12:00", 120, "Ball control"),
    (9, 2, "5.1.2025", "10:00", 120, "Tactics"),
    (10, 2, "6.1.2025", "10:00", 60, "Recovery")
]
for training in trainings:
    cur.execute("INSERT INTO trainings(training_id, team_id, date, start_time, duration_min, focus) VALUES(?, ?, ?, ?, ?, ?)", training)

coachassignments = [
    # coach_id, training_id, head, assistant, fitness
    (1, 1, 1, 0, 0),
    (2, 1, 0, 1, 0),
    (3, 2, 0, 0, 1),
    (1, 3, 0, 1, 0),
    (2, 3, 1, 0, 0),
    (2, 4, 0, 1, 0),
    (1, 4, 1, 0, 0),
    (3, 5, 0, 0, 1),
    (1, 6, 1, 0, 0),
    (2, 6, 0, 1, 0),
    (3, 7, 0, 0, 1),
    (1, 8, 0, 1, 0),
    (2, 8, 1, 0, 0),
    (2, 9, 0, 1, 0),
    (1, 9, 1, 0, 0),
    (3, 10, 0, 0, 1),
]
for coachassigment in coachassignments:
    cur.execute("""INSERT INTO coachassignment(coach_id, training_id, head, assistant, fitness) VALUES(?, ?, ?, ?, ?)""", coachassigment)


trainingattendances = [
    (1,1, None),
    (2,1, "Did a great job"),
    (3,1, None),
    (1,2, ""),
    (2,2, None),
    (3,2, "Got injured"),
    (4,2, None),
    (5,2, None),
    (6,2, "Was late for 20min"),
    (7,2, "Got injured"),
    (1,3, None),
    (4,3, ""),
    (4,4, None),
    (5,5, None),
    (6,5, "Was late for 10min"),
    # ----
    (8,6, "Was late for 30min"),
    (10,6, None),
    (9,7, "Did a great job"),
    (8,7, None),
    (11,7, "His running speed improved"),
    (8,8, "None"),
    (9,8, "Got injured"),
    (10,8, "Had a fight with the coach"),
    (11,8, "None"),
    (12,8, None),
    (13,8, "Got injured"),
    (14,8, "Was late for 10min"),
    (12,9, None),
    (14,10, None),
    (9,10, "Got injured again"),
]
for trainingattendance in trainingattendances:
    cur.execute("INSERT INTO trainingattendance(player_id, training_id, notes) VALUES(?, ?, ?)", trainingattendance)

teammemberships = [
    (1, 1, "1.1.2024", None),
    (1, 2, "1.1.2024", None),
    (1, 3, "1.1.2022", None),
    (1, 4, "1.1.2023", None),
    (1, 5, "1.1.2025", None),
    (1, 6, "1.1.2022", None),
    (1, 7, "1.1.2025", None),
    #-----
    (2, 8, "1.1.2025", "1.1.2028"),
    (2, 9, "1.1.2025", "1.1.2028"),
    (2, 10, "1.1.2024", "1.1.2027"),
    (2, 11, "1.1.2024", "1.1.2027"),
    (2, 12, "1.1.2023", "1.1.2026"),
    (2, 13, "1.1.2023", "1.1.2026"),
    (2, 14, "1.1.2025", "1.1.2028")    
]
for teammembership in teammemberships:
    cur.execute("INSERT INTO teammembership(team_id, player_id, start_date, end_date) VALUES(?, ?, ?, ?)", teammembership)

matches = [
    (1, 1, 1, "Lokomotiva", "18:00", "Zagreb", 2, 1),
    (2, 1, 1, "Varaždin", "19:00", "Varaždin", 3, 3),
    (3, 3, 1, "Dinamo", "18:00", "Zagreb", 0, 5),
    (4, 3, 1, "Hajduk", "20:00", "Split", 1, 0),
    #-------
    (5, 2, 2, "Hajduk", "16:00", "Split", 2, 1),
    (6, 2, 2, "Dinamo", "17:00", "Zagreb", 1, 2),
    (7, 4, 2, "Varaždin", "18:00", "Varaždin", 0, 0),
    (8, 4, 2, "Lokomotiva", "15:00", "Zagreb", 0, 1)
]
for match in matches:
    cur.execute("INSERT INTO matches(match_id, competition_id, team_id, opponent_team, time, location, our_goals, opponent_goals) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", match)

matchattendances = [
    #P  M  M   G  A  S  Y  R
    (1, 1, 90, 0, 0, 3, 0, 0),
    (2, 1, 90, 0, 1, 0, 1, 0),
    (3, 1, 90, 0, 1, 0, 0, 0),
    (4, 1, 70, 1, 0, 0, 1, 0),
    (5, 1, 90, 1, 0, 0, 0, 0),
    (6, 1, 20, 0, 0, 0, 0, 0),

    (1, 2, 90, 0, 0, 1, 0, 0),
    (2, 2, 90, 0, 1, 0, 0, 0),
    (3, 2, 90, 0, 2, 0, 1, 0),
    (4, 2, 70, 1, 0, 0, 0, 0),
    (5, 2, 90, 2, 0, 0, 0, 0),
    (6, 2, 20, 0, 0, 0, 2, 1),

    (1, 3, 90, 0, 0, 0, 1, 0),
    (2, 3, 90, 0, 0, 0, 0, 0),
    (3, 3, 90, 0, 0, 0, 0, 0),
    (4, 3, 90, 0, 0, 0, 0, 0),
    (5, 3, 90, 0, 0, 0, 1, 0),

    (1, 4, 90, 0, 0, 5, 0, 0),
    (2, 4, 90, 0, 0, 0, 0, 0),
    (3, 4, 90, 0, 1, 0, 1, 0),
    (4, 4, 70, 0, 0, 0, 0, 0),
    (5, 4, 90, 1, 0, 0, 0, 0),

    #------------
    (8, 5, 90, 0, 0, 3, 0, 0),
    (9, 5, 90, 0, 1, 0, 1, 0),
    (10, 5, 90, 0, 1, 0, 0, 0),
    (11, 5, 70, 1, 0, 0, 1, 0),
    (12, 5, 90, 1, 0, 0, 0, 0),
    (14, 5, 20, 0, 0, 0, 0, 0),

    (8, 6, 90, 0, 0, 3, 0, 0),
    (9, 6, 90, 0, 1, 0, 0, 0),
    (10, 6, 90, 0, 0, 0, 1, 0),
    (11, 6, 70, 0, 0, 0, 1, 0),
    (12, 6, 90, 1, 0, 0, 0, 0),
    (14, 6, 20, 0, 0, 0, 2, 1),

    (8, 7, 90, 0, 0, 6, 0, 0),
    (9, 7, 90, 0, 0, 0, 1, 0),
    (10, 7, 90, 0, 0, 0, 0, 0),
    (11, 7, 90, 0, 0, 0, 1, 0),
    (12, 7, 90, 0, 0, 0, 0, 0),

    (8, 8, 90, 0, 0, 10, 0, 0),
    (9, 8, 90, 0, 0, 0, 1, 0),
    (10, 8, 90, 0, 0, 0, 1, 0),
    (11, 8, 70, 0, 0, 0, 0, 0),
    (12, 8, 90, 0, 0, 0, 1, 0),
]
for matchattendance in matchattendances:
    cur.execute("INSERT INTO matchattendance(player_id, match_id, minutes_played, goals, assists, saves, yellow_cards, red_cards) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", matchattendance)


conn.commit()
conn.close()
