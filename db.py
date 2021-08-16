import sqlite3
from uuid import uuid4


class VoteDB:

    def __init__(self):
        self.conn = sqlite3.connect('vote.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        create_topic = """
        CREATE TABLE IF NOT EXISTS topics (
        id varchar(50) primary key not null,
        name varchar(50) not null
        );"""
        create_votes = """
        CREATE TABLE IF NOT EXISTS votes(
        id integer primary key AUTOINCREMENT not null,
        topic varchar(50),
        choice_name varchar(50),
        choice_count int,
        FOREIGN KEY (topic) references topics(id)
        ) 
        """
        self.conn.execute(create_topic)
        self.conn.execute(create_votes)
        self.conn.commit()

    def add_topic(self, topic_name):
        uid = str(uuid4())
        query = """
        INSERT INTO topics (id, name)
        VALUES (?, ?)
        """
        self.conn.execute(query, (uid, topic_name))
        self.conn.commit()

    def add_choice(self, choice_name, topic_id):
        query = """
        INSERT INTO votes(topic, choice_name, choice_count)
        VALUES (?, ?, ?);
        """
        self.conn.execute(query, (topic_id, choice_name, 0))
        self.conn.commit()

    def vote(self, choice_id, topic_id):
        query = """
        UPDATE votes SET choice_count = choice_count + 1
        WHERE topic=? and id=?
        """
        self.conn.execute(query, (topic_id, choice_id))
        self.conn.commit()

    def get_topic(self, topic_id):
        query = """
        SELECT id, choice_name, choice_count
        FROM votes v 
        WHERE v.topic=?
        """
        get_topic_name = "SELECT name FROM Topics where Topics.id = ?"
        topic_name = self.conn.execute(get_topic_name, (topic_id,)).fetchone()[0]
        print(topic_name)
        cur = self.conn.execute(query, (topic_id,))
        self.conn.commit()
        ret = []
        for (cid, cname, count) in cur:
            ret.append((cid, cname, count))
        return ret, topic_name

    def get_topic_names(self):
        query = """
        SELECT * FROM topics; 
        """
        res = self.conn.execute(query)
        self.conn.commit()
        ret = []
        for (tid, name) in res:
            ret.append({
                "topic_id": tid,
                "topic_name": name
            })
        return ret

    def is_topic_exists(self, topic_id):
        topics = self.get_topic_names()
        exists = list(filter(lambda d: d['topic_id'] == topic_id, topics))
        return len(exists) > 0
