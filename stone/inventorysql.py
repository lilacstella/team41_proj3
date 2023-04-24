import psycopg2
import json

#returns inventory in JSON
def get_current_inventory():
    connection = None
    try:
        connection = psycopg2.connect(user="csce315331_team_41_master",
                                       password="goldfishwithnuts",
                                       host="csce-315-db.engr.tamu.edu",
                                       database="csce315331_team_41")
        cursor = connection.cursor()
        select_inventory = "SELECT * FROM Inventory_t;"
        cursor.execute(select_inventory)
        inventory = cursor.fetchall()
        inventory_list = []
        for row in inventory:
            inventorydata = {"InventoryItem": row[0], 
                                "Category": row[1], 
                                "Quantity": float(row[2]), 
                                "Units": row[3], 
                                "StorageLocation": row[4]}
            inventory_list.append(inventorydata)
        # Return as a JSON string
        return json.dumps(inventory_list)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def restock_all():
    connection = None
    try:
        connection = psycopg2.connect(user="csce315331_team_41_master",
                                       password="goldfishwithnuts",
                                       host="csce-315-db.engr.tamu.edu",
                                       database="csce315331_team_41")
        cursor = connection.cursor()
        restock_inventory = "UPDATE Inventory_t SET Quantity = 500"
        cursor.execute(restock_inventory)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def restock_items(restock_json): 
    connection = None
    try:
        connection = psycopg2.connect(user="csce315331_team_41_master",
                                       password="goldfishwithnuts",
                                       host="csce-315-db.engr.tamu.edu",
                                       database="csce315331_team_41")
        cursor = connection.cursor()
        restock_json_dict = restock_json
        # Update the inventory with the specified item and restock amount using a parameterized query
        restock_query = "UPDATE Inventory_t SET Quantity = %s WHERE InventoryItem = %s"
        inventory_tuple = (restock_json_dict["Quantity"], restock_json_dict["InventoryItem"])
        cursor.execute(restock_query, inventory_tuple)
        connection.commit()
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
