
SQL_QUERIES = {
    "create_user_table": "CREATE TABLE IF NOT EXISTS Account(\
            Id SERIAL PRIMARY KEY,\
            Username VARCHAR(50) NOT NULL UNIQUE,\
            Email VARCHAR(50) NOT NULL UNIQUE,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            Password VARCHAR(25) NOT NULL );",

    "create_store_table": "CREATE TABLE IF NOT EXISTS Store(\
            Id SERIAL PRIMARY KEY,\
            StoreName VARCHAR(50) NOT NULL UNIQUE,\
            Address VARCHAR(100) NOT NULL,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            UserId INTEGER NOT NULL,\
            IsActivated INTEGER DEFAULT -1,\
            CONSTRAINT user_store\
                FOREIGN KEY (UserId)\
                REFERENCES Account (Id)\
                ON DELETE CASCADE);",

    "create_product_table": "CREATE TABLE IF NOT EXISTS Product(\
            Id INTEGER PRIMARY KEY,\
            ProductName VARCHAR(50) NOT NULL,\
            ProductPrice FLOAT NOT NULL,\
            ProductDescription VARCHAR(1024), \
            CreatedOn timestamp without time zone DEFAULT now(),\
            StoreId INTEGER NOT NULL,\
            CONSTRAINT store_product\
                FOREIGN KEY (StoreId)\
                REFERENCES Store (Id)\
                ON DELETE CASCADE);",

    "create_variant_table":"CREATE TABLE IF NOT EXISTS ProductVariant(\
            Id SERIAL PRIMARY KEY,\
            Option1 VARCHAR(32),\
            Option2 VARCHAR(32),\
            Option3 VARCHAR(32),\
            Stock INTEGER NOT NULL,\
            Sku VARCHAR(32),\
            CompareAtPrice FLOAT,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            ProductId INTEGER NOT NULL UNIQUE,\
            CONSTRAINT product_variant\
                FOREIGN KEY (ProductId)\
                REFERENCES Product (Id)\
                ON DELETE CASCADE);",

    "create_user": "INSERT INTO Account (Username, Email, Password) VALUES (%s, %s, %s) RETURNING Id, Username",

    "check_user":"",

    "new_store": "INSERT INTO Store (StoreName, Address, UserId) VALUES (%s, %s, %s)",

    "add_product": "",

    "add_variant": "",

    "change_email": "",

    "change_password": "",

    "update_store": "",

    "get_tables": "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES",

}