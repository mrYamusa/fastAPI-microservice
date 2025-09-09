import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate, ShipmentStatus
from typing import Any
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


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Shipments (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status REAL)
            """,
        )
        self.connection.commit()
        # return table_name

    def create_shipment(self, shipment: ShipmentCreate):
        self.cursor.execute(
            """
            SELECT MAX(id) FROM Shipments
            """
        )
        max_id = self.cursor.fetchone()
        new_id = max_id[0] + 1
        self.connection.commit()

        self.cursor.execute(
            """
            INSERT INTO Shipments VALUES (:id, :content, :weight, :status)
            """,
            {
                "id": new_id,
                **shipment.model_dump(),
                "status": "Placed",
            },
        )
        self.connection.commit()
        return new_id

    def max_id(self):
        self.cursor.execute(
            """
            SELECT MAX(id) FROM Shipments
            """
        )
        max = self.cursor.fetchone()
        return max[0]

    def read_shipments(
        self, id: int
    ) -> dict[str, Any] | None:  # , shipment: ShipmentRead):  # -> ShipmentRead:
        self.cursor.execute(
            """
            SELECT * FROM Shipments
            WHERE id = :id
            """,
            {"id": id},
        )
        result = self.cursor.fetchone()
        print(result)
        if result:
            return {
                "id": result[0],
                "content": result[1],
                "weight": result[2],
                "status": result[3],
            }
        else:
            return None

    def update_shipment(self, id: int, shipment: ShipmentUpdate):
        self.cursor.execute(
            """
            UPDATE Shipments SET content = :content, weight = :weight, status = :status
            WHERE id = :id
            """,
            {"id": id, **shipment.model_dump()},
        )
        self.connection.commit()
        return self.read_shipments(id=id)

    def delete_shipment(self, id: int):
        self.cursor.execute(
            """
            DELETE * FROM Shipments
            WHERE id = :id
            """,
            {"id": id},
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


# Database.read_shipments(id=125)
# dbb = Database()
# su = ShipmentUpdate(status=ShipmentStatus.placed)
# print(dbb.read_shipments(id=151))
# print(dbb.update_shipment(id=151, shipment=su))


def play():
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

    status = "In Transit"
    id = 150

    # cursor.execute(
    #     """
    #     UPDATE Shipments SET status = ?
    #     WHERE id <= ?
    #     """,
    #     (status, id),
    # )

    cursor.execute(
        """
        UPDATE Shipments SET status = :status
        WHERE id <= :id
        """,
        {"status": status, "id": id},
    )
    connection.commit()

    connection.close()
