from app import login
from flask_login import current_user
from flask_login import UserMixin
from mysqlconnection import connectToMySQL
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# What is going on here?
# db = __import__('config').Config.db

# What is going on here?
db = ''


@login.user_loader
def load_user(id):
    return User.get_user_by_id(id)


class User(UserMixin):

    def __init__(self, user_dict):
        # Alphabetically...
        self.email = user_dict['email']
        self.favorite_cards = []
        self.id = user_dict['id']
        self.name_first = user_dict['name_first']
        self.name_last = user_dict['name_last']
        self.password_hash = user_dict['password_hash']
        self.registered_on = None
        self.username = user_dict['username']


    @classmethod
    def add_user(cls, new_user_dict):
        query = """
                INSERT INTO users (
                    username,
                    email
                    )
                VALUES (
                    %(username)s,
                    %(email)s
                    );
                """
        return connectToMySQL(db).query_db(query, new_user_dict)


    @classmethod
    def get_user_by_username(cls, user_dict):
        query = """
                SELECT * FROM users
                WHERE username = %(username)s;
                """
        result = connectToMySQL(db).query_db(query, user_dict)
        if result:
            user = User(result[0])
            return user


    @classmethod
    def get_user_by_id(cls, id):
        id_dict = {'id': id}
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query, id_dict)
        if result:
            user = User(result[0])
            return user


    def set_password(self, user_dict):
        password_hash = generate_password_hash(user_dict['password'])
        username_and_password = {
                                'username': user_dict['username'],
                                'password_hash': password_hash
                                }
        self.password_hash = username_and_password['password_hash']
        query = """
                UPDATE users
                SET password_hash = %(password_hash)s
                WHERE username = %(username)s;
                """
        return connectToMySQL(db).query_db(query, username_and_password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Card:

    def __init__(self, db_card):
        self.id = db_card['id']
        self.card_name = db_card['card_name']
        self.description = db_card['description']
        self.type = db_card['card_type']
        self.released_on = db_card['released_on']
        self.status = db_card['status']
        self.quantity = db_card['quantity']
        self.price = db_card['price']
        self.genus = db_card['card_genus']
        self.order = db_card['card_order']
        self.filename = db_card['filename']


    @classmethod
    def add_card(cls, new_card_dict):
        query = """
                INSERT INTO cards (
                    card_genus,
                    card_name,
                    card_order,
                    card_type,
                    description,
                    filename,
                    price,
                    quantity,
                    released_on,
                    status
                    )
                VALUES (
                    %(card_genus)s,
                    %(card_name)s,
                    %(card_order)s,
                    %(card_type)s,
                    %(description)s,
                    %(filename)s,
                    %(price)s,
                    %(quantity)s,
                    %(released_on)s,
                    %(status)s
                    );
                """
        return connectToMySQL(db).query_db(query, new_card_dict)


    @classmethod
    def get_all_cards(cls):
        query = """
                SELECT * FROM cards;
                """
        results = connectToMySQL(db).query_db(query)
        if results:
            return [Card(result) for result in results]


    @classmethod
    def get_one_card(cls, card_name_dict):
        query = """
                SELECT * FROM cards
                WHERE card_name = %(card_name)s;
                """
        result = connectToMySQL(db).query_db(query, card_name_dict)
        if result:
            return Card(result[0])


    @classmethod
    def does_card_name_exist(cls, card_edits_dict):
        query = """
                SELECT * FROM cards
                WHERE card_name = %(card_name)s;
                """
        return connectToMySQL(db).query_db(query, card_edits_dict)


    @classmethod
    def does_filename_exist(cls, card_edits_dict):
        query = """
                SELECT * FROM cards
                WHERE filename = %(filename)s;
                """
        return connectToMySQL(db).query_db(query, card_edits_dict)


    def update_card(self, card_edits_dict):
        query = """
                UPDATE cards
                SET
                    card_name = %(card_name)s,
                    description = %(description)s,
                    type = %(type)s,
                    released_on = %(released_on)s,
                    status = %(status)s,
                    quantity = %(quantity)s,
                    filename = %(filename)s
                WHERE card_name = %(original_card_name)s;
                """
        return connectToMySQL(db).query_db(query, card_edits_dict)


    @classmethod
    def delete_card(cls, card_name_dict):
        query = """
                DELETE FROM cards
                WHERE card_name = %(card_name)s;
                """
        return connectToMySQL(db).query_db(query, card_name_dict)


    @classmethod
    def like_card(cls, favorite_dict):
        query = """
                INSERT INTO favorite (user_id, card_id)
                VALUES (%(user_id)s, %(card_id)s);
                """
        return connectToMySQL(db).query_db(query, favorite_dict)


    @classmethod
    def unlike_card(cls, favorite_dict):
        query = """
                DELETE FROM favorite
                WHERE user_id = %(user_id)s AND card_id = %(card_id)s;
                """
        return connectToMySQL(db).query_db(query, favorite_dict)


    @classmethod
    def get_liked_cards(cls, user_dict):
        query = """
                SELECT * FROM cards
                LEFT JOIN favorite ON favorite.card_id = cards.id
                LEFT JOIN users ON favorite.user_id = users.id
                WHERE favorite.user_id = %(id)s;
                """
        rows_of_cards = connectToMySQL(db).query_db(query, user_dict)
        for favorite_card in rows_of_cards:
            card = Card(favorite_card)
            current_user.favorite_cards.append(card.id)
        return