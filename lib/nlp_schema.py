schema = (
    """ CREATE TABLE Coin_Types (
        coin_symbol VARCHAR(10) PRIMARY KEY,
        coin_name VARCHAR(255) NOT NULL
    )
    """,
    """ CREATE TABLE Coin_History (
        coin_history_id SERIAL PRIMARY KEY,
        coin_type_id VARCHAR(10) REFERENCES Coin_Types(coin_symbol)
            ON DELETE CASCADE,
        coin_history_datetime timestamp with time zone NOT NULL
            DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
        price numeric (10,2) NOT NULL
    )
    """,
    """ CREATE TABLE Source_Types (
        source_type_id SERIAL PRIMARY KEY,
        source_type_name VARCHAR(255) NOT NULL
    )
    """,
    """ CREATE TABLE Sources (
        source_id SERIAL PRIMARY KEY,
        source_name VARCHAR(255) NOT NULL,
        source_type_id integer REFERENCES Source_Types(source_type_id)
            ON DELETE RESTRICT,
        source_rss_url VARCHAR(255) NOT NULL
    )
    """,
    """ CREATE TABLE Posts (
        post_id SERIAL PRIMARY KEY,
        post_url VARCHAR(511) NOT NULL,
        post_datetime timestamp with time zone NOT NULL
            DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
        source_id integer REFERENCES Sources(source_id)
            ON DELETE CASCADE,
        coin_type_id VARCHAR(10) REFERENCES Coin_Types(coin_symbol)
            ON DELETE CASCADE,
        post_processed boolean NOT NULL
    )
    """,
    """ CREATE TABLE Chunks (
        chunk_id SERIAL PRIMARY KEY,
        chunk VARCHAR(1023) NOT NULL,
        post_id integer REFERENCES Posts(post_id)
            ON DELETE CASCADE,
        coin_id VARCHAR(10) REFERENCES Coin_Types(coin_symbol)
            ON DELETE CASCADE
    )
    """
)
