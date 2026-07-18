from db import Database, Leaderboard
from decouple import config

db = Database(
    dbname=config('DB_NAME'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    host=config('DB_HOST'),
    port=config('DB_PORT', cast=int)
)
leaderboard = Leaderboard(db)

leaderboard.add_score('Alex', 150)
leaderboard.add_score('Test', 90)

top_players = leaderboard.get_top_scores()
print(top_players)