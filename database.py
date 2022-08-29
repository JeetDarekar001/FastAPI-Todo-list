from sqlalchemy import create_engine

SQLALCHEMY_DATABSE_URL="sqlite:///./todos.db"
engine=create_engine(
    SQLALCHEMY_DATABSE_URL,
    connect_args={"check_same_thread":False}
)