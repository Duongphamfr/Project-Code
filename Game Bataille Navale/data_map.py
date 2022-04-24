import index
import json

with open("players_data.json", "r") as f:
    data = f.read()
    data = json.loads(data)


if data['size'] == 'medium':
    # MEDIUM SIZE

    # create the Ship

    # big Ship
    ship1 = index.Ship((35, 195), (1000, 300))
    # medium ship
    ship2 = index.Ship((35, 120), (1100, 300))
    ship3 = index.Ship((35, 120), (1200, 300))
    # small ship
    ship4 = index.Ship((35, 35), (1300, 300))
    ship5 = index.Ship((35, 35), (1300, 350))
    ship6 = index.Ship((35, 35), (1300, 400))
    ship7 = index.Ship((35, 35), (1300, 450))
    ship8 = index.Ship((35, 35), (1300, 500))

    listShip = [ship1, ship2, ship3, ship4, ship5, ship6, ship7, ship8]

    def reset_listShip():
        global ship1, ship2, ship3, ship4, ship5, ship6, ship7, ship8, listShip
        ship1.__init__((35, 195), (1000, 300))
        ship2.__init__((35, 120), (1100, 300))
        ship3.__init__((35, 120), (1200, 300))
        ship4.__init__((35, 35), (1300, 300))
        ship5.__init__((35, 35), (1300, 350))
        ship6.__init__((35, 35), (1300, 400))
        ship7.__init__((35, 35), (1300, 450))
        ship8.__init__((35, 35), (1300, 500))
        listShip = [ship1, ship2, ship3, ship4, ship5, ship6, ship7, ship8]

elif data['size'] == 'multi':
    # SMALL SIZE

    # create the Ship

    # medium Ship
    ship1 = index.Ship((35, 120), (1000, 300))
    # small ship
    ship2 = index.Ship((35, 35), (1100, 300))
    ship3 = index.Ship((35, 35), (1200, 350))
    ship4 = index.Ship((35, 35), (1300, 400))
    ship5 = index.Ship((35, 35), (1300, 450))
    ship6 = index.Ship((35, 35), (1300, 500))

    listShip = [ship1, ship2, ship3, ship4, ship5, ship6]

    def reset_listShip():
        global ship1, ship2, ship3, ship4, ship5, ship6, listShip
        ship1.__init__((35, 120), (1000, 300))
        ship2.__init__((35, 35), (1100, 300))
        ship3.__init__((35, 35), (1200, 350))
        ship4.__init__((35, 35), (1300, 400))
        ship5.__init__((35, 35), (1300, 450))
        ship6.__init__((35, 35), (1300, 500))
        listShip = [ship1, ship2, ship3, ship4, ship5, ship6]