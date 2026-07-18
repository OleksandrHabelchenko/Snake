Snake Game

Classic Snake game built with Python, tkinter and OOP — now with a PostgreSQL-backed leaderboard running in Docker.

Technologies


Python 3.14
tkinter
Pillow
playsound
PostgreSQL (running in a Docker container)
psycopg2
Custom lightweight ORM (Database + Leaderboard classes)


Features


Snake with eyes and tongue
Background image and music
Sound effects
Restart with R key
Score is saved to a PostgreSQL database on Game Over
Player enters a nickname, which is stored alongside their score
Custom Database/Leaderboard classes handle all SQL queries (INSERT, SELECT)


How to run


Install dependencies:


pip install -r requirements.txt


Start PostgreSQL in Docker:


docker run --name my-postgres -e POSTGRES_PASSWORD=yourpassword -p 5433:5432 -d postgres


Create the database and table:


docker exec -it my-postgres psql -U postgres
CREATE DATABASE snake_game;
\c snake_game
CREATE TABLE leaderboard (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


Create a .env file based on .env.example and fill in your own values.
Run the game:


python snake_OOP.py

About

Originally a simple Snake game, extended with a self-written mini-ORM (no Django/SQLAlchemy) to practice raw SQL and database connection handling in Python.

Author

Oleksandr Habelchenko — GitHub
