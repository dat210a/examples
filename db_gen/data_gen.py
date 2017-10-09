from mysql import connector
from random import choice
from argon2 import PasswordHasher
import logging
import json
import requests

word_site = 'http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain'
conf_file = '<path to config file>'
ph = PasswordHasher()


def setup_logging():
    lg = logging.getLogger(__name__)
    lg.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='db_test_fill.log', encoding='utf-8', mode='a')
    fmt = logging.Formatter('[%(asctime)s]:%(module)s:%(levelname)s: %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(fmt)
    lg.addHandler(handler)
    return lg


def end_logging(log):
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)


def load_config(cfile):
    with open(cfile, 'r') as cf:
        return json.load(cf)


def get_word():
    # Returns a random word
    response = requests.get(word_site)
    words = response.content.splitlines()
    res = choice(words).decode('utf-8')
    return res


def gen_user(cur):
    """
    Generates and inserts a user with a random word as username and password.
    This example also inserts a random value into the 'deleted' column.
    The password is hashed before it's inserted into the database, but logged in plaintext for testing purposes.
    NOTE:
        SQL can be written as:
        INSERT INTO <table>
        VALUES (<values>)
        This only works if there is a value for every column in the table, and they are inserted in the same order
        as the columns are sorted in the table. Otherwise, you have to specify which columns and which order to insert
        the data
    """
    sql = "INSERT INTO users (user_name, user_password, deleted)" \
          "VALUES (%s, %s, %s)"
    uname = get_word()
    pword = get_word()
    lg.info('User with name {} and password {} generated.'.format(uname, pword))
    cur.execute(sql, (uname, ph.hash(pword), choice([0, 1])))


if __name__ == '__main__':
    lg = setup_logging()
    data = load_config(conf_file)
    # Establishing connection to the database
    db_connection = connector.connect(user=data['username'],
                                      password=data['password'],
                                      host=data['host'],
                                      database=data['database'])
    cur = db_connection.cursor()

    for i in range(1, 16):
        print('Generating user {}'.format(i))
        gen_user(cur)

    end_logging(lg)

