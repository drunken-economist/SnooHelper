from peewee import IntegerField, TextField, SqliteDatabase, Model, BooleanField, TimestampField

db = SqliteDatabase('redditslacker_master.db')


class BaseModel(Model):
    class Meta:
        database = db


class UserModel(BaseModel):
    username = TextField()
    removed_comments = IntegerField(default=0)
    removed_submissions = IntegerField(default=0)
    approved_comments = IntegerField(default=0)
    approved_submissions = IntegerField(default=0)
    bans = IntegerField(default=0)
    shadowbanned = BooleanField(default=False)
    tracked = BooleanField(default=False)
    subreddit = TextField()


class AlreadyDoneModel(BaseModel):
    thing_id = TextField(unique=True)
    timestamp = TimestampField()
    subreddit = TextField()