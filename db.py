import psycopg2

from decouple import config

class Database:  # универсальный класс для подключения к БД
    def __init__(self, dbname, user, password, host='localhost', port=5433):  # конструктор, вызывается при создании объекта
        self.connection = psycopg2.connect(  # открываем соединение с PostgreSQL
            dbname=dbname,  # имя базы данных
            user=user,  # имя пользователя БД
            password=password,  # пароль от БД
            host=host,  # адрес сервера (localhost = свой компьютер)
            port=port  # порт подключения
        )

    def execute(self, query, params=None):  # метод для выполнения любого SQL-запроса
        cursor = self.connection.cursor()  # создаём "курсор" - инструмент для отправки команд в БД
        cursor.execute(query, params)  # выполняем сам SQL-запрос с параметрами
        self.connection.commit()  # подтверждаем/сохраняем изменения в базе
        return cursor  # возвращаем курсор наружу (пригодится для чтения результата)

    def fetch_all(self, query, params=None):  # метод для запросов, которые ЧИТАЮТ данные (SELECT)
        cursor = self.execute(query, params)  # выполняем запрос через метод execute выше
        return cursor.fetchall()  # забираем ВСЕ найденные строки результата


class Leaderboard:  # специализированный класс именно для таблицы leaderboard
    def __init__(self, db):  # конструктор, принимает готовый объект Database
        self.db = db  # сохраняем этот объект, чтобы пользоваться им в других методах

    def add_score(self, nickname, score):  # метод для добавления нового результата игрока
        query = "INSERT INTO leaderboard (nickname, score) VALUES (%s, %s)"  # SQL-запрос на добавление строки
        self.db.execute(query, (nickname, score))  # выполняем запрос через объект Database, подставляя реальные значения

    def get_top_scores(self, limit=5):  # метод для получения топа игроков
        query = "SELECT nickname, score FROM leaderboard ORDER BY score DESC LIMIT %s"  # запрос: выбрать, отсортировать по убыванию, ограничить количество
        return self.db.fetch_all(query, (limit,))  # выполняем запрос через fetch_all, возвращаем список результатов