import random  # Unused import as of now, disregard.


class Room:
    class Spawn:
        movement = ["NORTH"]
        dialogues = [
            "Spawn",
            "Hi welcome to TESCO how may I help you?"
        ]

    class Crossroad:
        movement = ["NORTH", "SOUTH", "EAST", "WEST"]
        dialogues = [
            "crossroad"
        ]

    class Room_e_south:  # e means exit btw, imagine like a room with just one door leading south
        movement = ["SOUTH"]
        dialogues = [
            "door south"
        ]


# Movement Values
coordinates = [0, 0, 0]
current_room = Room.Spawn  # Where the player currently is

# Map
# (Room, Loot claimed, Enemy Killed)
game_map = {
    (0, 0, 0): (Room.Spawn(), True, True),
    (0, 1, 0): (Room.Crossroad(), False, False),
    (0, 2, 0): (Room.Room_e_south, False, False)

}

# Character Values
hit_points = 100
action_points = 100


# Functions

# Unpacker = Tuple -> List convertor. This function will get the tuple from game_map by getting the players coordinates.
# Returns the game_map tuple as a list for easy access.
# example: unpacker([0, 0, 0,]) -> [Room.Spawn(), True, True]
def unpacker(coord):
    return_list = list(game_map[tuple(coord)])
    return return_list


# MCL = Move Choice List. This function generates a list of available movement options in the room the player is in
# The function will get every option (i) in current_room.movement (room class). Function can be used as print(mcl())
def mcl():
    listed = ""
    for i in current_room.movement:
        listed += str(current_room.movement.index(i) + 1) + ": " + str(i.capitalize()) + "\n"
    return listed


# This is the standard movement function, All it does is change the coordinates depending on the players input.
# This function does not loop so you can write any code after it.
def move():
    mc = input("Choose Direction: ")  # mc = move choice, player inputs direction to move.
    mc = mc.upper()
    if mc in current_room.movement:
        if mc == "NORTH":
            coordinates[1] += 1
        elif mc == "SOUTH":
            coordinates[1] += -1
        elif mc == "EAST":
            coordinates[0] += 1
        elif mc == "WEST":
            coordinates[0] += -1


# the game itself
while True:
    unpacked = unpacker(coordinates)  # unpacks current rooms coordinates. Example: [Room.Spawn, false, false]
    current_room = unpacked[0]  # Gets the first element in unpacked, rn that would be Room.Spawn
    print(coordinates)  # For debugging purposes, you can delete this.
    print(mcl())   # prints the current rooms movement options
    move()  # function in charge of moving the player.
