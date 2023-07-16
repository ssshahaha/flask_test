from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import AppConfig

# engine = create_engine(AppConfig.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# DB = SessionLocal()


engine = create_engine(AppConfig.SQLALCHEMY_DATABASE_URI, max_overflow=0, pool_size=50)
SessionLocal = sessionmaker(bind=engine)
DB = scoped_session(SessionLocal)

# # debug sqlalchemy
# from sqlalchemy import event
# @event.listens_for(engine, "before_cursor_execute")
# def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     print("Start Query: %s" % statement % parameters)


__all__ = ['DB']
