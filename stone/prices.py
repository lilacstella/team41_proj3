import psycopg2

from stone import SQL_CREDS


def get_prices():
    connection = None
    try:
        connection = psycopg2.connect(**SQL_CREDS)
        cursor = connection.cursor()

        prices_dict = {}
        select_menu = "select * from menu_t"
        cursor.execute(select_menu)
        menu = cursor.fetchall()
        menulist = []
        for row in menu:
            menuitemdict = {"menu_item_name": row[0], "current_price": str(row[1])}
            menulist.append(menuitemdict)
        prices_dict["menuitems"] = menulist

        select_category = "select distinct category from inventory_t"
        cursor.execute(select_category)
        categories = cursor.fetchall()
        categorieslist = []
        for row in categories:
            categorieslist.append(row[0])
        prices_dict["categories"] = categorieslist
        if ("Seasonal" not in categorieslist):
            categorieslist.append("Seasonal")

        select_storageloc = "select distinct storagelocation from inventory_t"
        cursor.execute(select_storageloc)
        storage = cursor.fetchall()
        storagelist = []
        for row in storage:
            storagelist.append(row[0])
        prices_dict["storage"] = storagelist

        get_no_img = """select distinct t.item from 
        (select inventoryitem as item from inventory_t where category IN ('Topping-Meat', 'Topping-Veggies', 'Seasonal', 'Sauce', 'Drizzle', 'Drink', 'Dough', 'Cheese') and inventoryitem not in ('Regular Dough')
        ) t left join item_images i on t.item = i.item_name
        where i.item_name is NULL"""
        cursor.execute(get_no_img)
        no_img_items = [row[0] for row in cursor.fetchall()]
        prices_dict["no-img"] = no_img_items

        return prices_dict

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def add_menu_item(json_file):
    connection = None
    try:
        connection = psycopg2.connect(**SQL_CREDS)
        cursor = connection.cursor()

        add_item = "INSERT INTO menu_t VALUES (%s, %s);"
        menu_tuple = (json_file["menuitem"], json_file["price"])
        cursor.execute(add_item, menu_tuple)
        connection.commit()
        return True

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def add_inv_item(json_file):
    connection = None
    try:
        connection = psycopg2.connect(**SQL_CREDS)
        cursor = connection.cursor()
        add_item = "INSERT INTO inventory_t VALUES (%s, %s, %s, %s, %s);"
        menu_tuple = (json_file["inventoryitem"], json_file["category"], json_file["quantity"], json_file["units"],
                      json_file["storagelocation"])
        cursor.execute(add_item, menu_tuple)
        connection.commit()
        return True

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def change_price(json_file):
    connection = None
    try:
        connection = psycopg2.connect(**SQL_CREDS)
        cursor = connection.cursor()
        price_tuple = (json_file["price"], json_file["menuitem"])
        cursor.execute("UPDATE menu_t SET price = %s WHERE menuitem = %s", price_tuple)
        connection.commit()
        return True

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def add_img(json_file):
    connection = None
    try:
        connection = psycopg2.connect(**SQL_CREDS)
        cursor = connection.cursor()
        checkforimage = "SELECT * FROM item_images where item_name = %s"
        checktuple = (json_file["item_name"],)
        print(json_file["img_url"])
        cursor.execute(checkforimage, checktuple)
        results = cursor.fetchall()
        if (results == []):
            img_tuple = (json_file["item_name"], json_file["img_url"])
            cursor.execute("INSERT INTO item_images VALUES (%s, %s)", img_tuple)
            connection.commit()
        else:
            update_img = "UPDATE item_images SET img_url = %s WHERE item_name = %s"
            update_tuple = (json_file["img_url"], json_file["item_name"])
            cursor.execute(update_img, update_tuple)
            connection.commit()

        return True

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
