import index
import json

# get data stocked in a json file
with open("players_data.json", "r") as f:
    data = f.read()
    data = json.loads(data)

if data['size'] == 'medium':
    gridSize = 10
    totalTarget = 16

    # create the Ship
    ship1 = index.Ship((35, 195), (1000, 300))
    ship2 = index.Ship((35, 120), (1100, 300))
    ship3 = index.Ship((35, 120), (1200, 300))
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

elif data['size'] == 'small':
    gridSize = 7
    totalTarget = 8

    # create the Ship
    ship1 = index.Ship((35, 120), (1000, 300))
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