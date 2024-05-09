from sqlalchemy import Engine, create_engine


def init_db_engine(
    db_user: str, db_password: str, db_host: str, db_port: str, db_name: str
) -> Engine:
    """Initializes sqlalchemy engine that connects to postgis database

    Args:
        db_user (str): the user name
        db_password (str): the password
        db_host (str): the url of the database host
        db_port (str): the port of the connection
        db_name (str): the name of the database

    Returns:
        Engine: connection to postgis database
    """
    return create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
