from peewee import *

db = SqliteDatabase('vote_orm.db')


class BaseModel(Model):
    class Meta:
        database = db


class Topics(BaseModel):
    id = CharField(max_length=60, null=False, primary_key=True)
    name = CharField(max_length=50, null=False)

    @classmethod
    def exists(cls, topic_id) -> bool:
        return cls.select().where(cls.id == topic_id).count() > 0


class Votes(BaseModel):
    id = AutoField(primary_key=True, null=False)
    topic = ForeignKeyField(Topics, backref='topic')
    choice_name = TextField()
    choice_count = IntegerField(default=0)
