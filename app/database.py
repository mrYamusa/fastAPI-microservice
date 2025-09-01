import sqlite3
# import json
# from typing import Any

# shipments: dict[Any, Any] = {}

# with open("./shipments.json", "r") as json_file:
#     content = json.load(json_file)
#     print(content)

#     for shipment in content:
#         shipments[shipment["id"]] = dict(**shipment)
#         # shipments[shipment["id"]] = {
#         #     "weight": shipment["weight"],
#         #     "content": shipment["content"],
#         #     "status": shipment["status"],
#         # }

# print(shipments)


# def save():
#     with open("./shipments.json", "w") as json_file:
#         json.dump(list(shipments.values()), json_file)

connection = sqlite3.connect("sqlite.db")

cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Shipments (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status REAL)
    """
)

# cursor.execute(
#     """
#     INSERT INTO Shipments VALUES (154, 'Air Pods Max', 2.9, 'Placed!')
#     """
# )

cursor.execute(
    """
    SELECT content FROM Shipments WHERE weight = 4.1
    """
)
result = cursor.fetchall()
print(result)
connection.commit()

# cursor.execute(
#     """
#     DELETE FROM Shipments
#     WHERE id = 154
#     """
# )
# connection.commit()

# cursor.execute(
#     """
#     DROP TABLE Shipments
#     """
# )
# connection.commit()

status = "Delivered"
content = "Skateboard"

cursor.execute(
    """
    UPDATE Shipments SET status = :status
    WHERE content  = :content
    """,
    (status, content),
)
connection.commit()

connection.close()
