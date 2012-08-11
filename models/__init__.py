'''
You can create tables by doing like this:

> from sqlalchemy import create_engine

> engine = create_engine('<DB Address>', client_encoding='utf-8')

> def create_tables():
>     from models.base import Base
>     Base.metadata.create_all(engine, checkfirst=True)

> if __name__ == '__main__':
>     create_tables()
'''
