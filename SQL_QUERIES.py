
SQL_QUERIES = {
    "create_user_table": "CREATE TABLE IF NOT EXISTS Account(\
            Id SERIAL PRIMARY KEY,\
            Username VARCHAR(50) NOT NULL UNIQUE,\
            Email VARCHAR(50) NOT NULL,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            Password VARCHAR(25) NOT NULL );",

    "create_store_table": "CREATE TABLE IF NOT EXISTS Store(\
            Id SERIAL PRIMARY KEY,\
            Name VARCHAR(50) NOT NULL,\
            Address VARCHAR(100) NOT NULL,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            UserId INTEGER NOT NULL,\
            CONSTRAINT user_store\
                FOREIGN KEY (UserId)\
                REFERENCES Account (Id)\
                ON DELETE CASCADE);",

    "create_product_table": "CREATE TABLE IF NOT EXISTS ProductInfo(\
            Id SERIAL PRIMARY KEY,\
            ProductName VARCHAR(50) NOT NULL,\
            ProductCategory VARCHAR(50) NOT NULL,\
            ProductPrice FLOAT NOT NULL,\
            ProductDiscount FLOAT NOT NULL,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            StoreId INTEGER NOT NULL,\
            CONSTRAINT store_product\
                FOREIGN KEY (StoreId)\
                REFERENCES Store (Id)\
                ON DELETE CASCADE);",

    "create_variant_table":"CREATE TABLE IF NOT EXISTS ProductVariantInfo(\
            Id SERIAL PRIMARY KEY,\
            Color VARCHAR(15),\
            Size VARCHAR(10),\
            Material VARCHAR(25),\
            Stock INTEGER NOT NULL,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            ProductId INTEGER NOT NULL,\
            CONSTRAINT product_variant\
                FOREIGN KEY (ProductId)\
                REFERENCES ProductInfo (Id)\
                ON DELETE CASCADE);",

    "create_user":"",

    "check_user":"",

    "new_store": "",

    "add_product": "",

    "add_variant": "",

    "change_email": "",

    "change_password": "",

    "update_store": "",

}