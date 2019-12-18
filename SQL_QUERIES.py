
SQL_QUERIES = {
    "create_user_table": "CREATE TABLE IF NOT EXISTS Account(\
            Id SERIAL PRIMARY KEY,\
            Username VARCHAR(32) NOT NULL UNIQUE,\
            Email VARCHAR(64) NOT NULL UNIQUE,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            IsStoreOwner INTEGER DEFAULT 1,\
            Password VARCHAR(32) NOT NULL );",

    "create_store_table": "CREATE TABLE IF NOT EXISTS Store(\
            Id SERIAL PRIMARY KEY,\
            ApiKey VARCHAR(128),\
            Password VARCHAR(128),\
            StoreName VARCHAR(64) NOT NULL UNIQUE,\
            IsActivated INTEGER DEFAULT -1,\
            CreatedOn timestamp without time zone DEFAULT now(),\
            LocationId INTEGER ,\
            UserId INTEGER NOT NULL,\
            CONSTRAINT user_store\
                FOREIGN KEY (UserId) REFERENCES Account (Id)\
                ON DELETE CASCADE,\
            CONSTRAINT loc_store\
                FOREIGN KEY (LocationId) REFERENCES Location (Id)\
                ON DELETE CASCADE);",

    "create_product_table": "CREATE TABLE IF NOT EXISTS Product(\
            Id VARCHAR(256) PRIMARY KEY,\
            ProductName VARCHAR(64) NOT NULL,\
            ProductPrice FLOAT NOT NULL,\
            ProductDescription VARCHAR(1024), \
            CreatedOn timestamp without time zone DEFAULT now(),\
            ImgSource VARCHAR(512),\
            CategoryId INTEGER,\
            StoreId INTEGER NOT NULL,\
            CONSTRAINT cat_product\
                FOREIGN KEY (CategoryId)\
                REFERENCES Category (Id)\
                ON DELETE CASCADE,\
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
            ProductId VARCHAR(256) NOT NULL,\
            CONSTRAINT product_variant\
                FOREIGN KEY (ProductId)\
                REFERENCES Product (Id)\
                ON DELETE CASCADE);",

    "create_location_table":"CREATE TABLE IF NOT EXISTS Location(\
            Id SERIAL PRIMARY KEY,\
            Country VARCHAR(64),\
            City VARCHAR(64),\
            County VARCHAR(64),\
            Neighborhood VARCHAR(64),\
            Address VARCHAR(64));",
    
    "create_category_table":"CREATE TABLE IF NOT EXISTS Category(\
            Id SERIAL PRIMARY KEY,\
            CategoryName VARCHAR(64),\
            IsDefault INTEGER,\
            BrandName VARCHAR(64),\
            Sector VARCHAR(64));",
#anothercolumn VARCHAR(64),
    "create_user": "INSERT INTO Account (Username, Email, Password) VALUES (%s, %s, %s) RETURNING Id, Username",

    "check_user":"",

    "new_store": "INSERT INTO Store (StoreName, LocationId, UserId, ApiKey, Password) VALUES (%s, %s, %s, %s, %s)",

    "add_product": "INSERT INTO Product (Id, ProductName, ProductPrice, ProductDescription, StoreId) \
                    VALUES (%s, %s, %s, %s, %s)",

    "add_variant": "INSERT INTO ProductVariant (Id, Option1, Option2, Option3, Stock, Sku, CompareAtPrice, ProductId) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",

    "update_user": "UPDATE Account SET Username =%s, Email=%s WHERE Id=%s",

    "change_password": "",

    "update_store": "",

    "get_tables": "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES",

    "new_location": "INSERT INTO Location (Country, City, County, Neighborhood, Address) VALUES (%s, %s, %s, %s, %s)"

}