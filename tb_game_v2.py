import random


class Room:
    class Spawn:
        movement = ["NORTH"]
        dialogues = [
            "You open your eyes to be greeted by a familiar TESCOs blue",
            "You wake up in an abandoned TESCOs warehouse"
        ]

    class Crossroad:
        movement = ["NORTH", "SOUTH", "EAST", "WEST"]
        dialogues = [
            "You find yourself in a 4-way junction There are old groceries all over the floor."
        ]

    class Room_e_south:  # e = exit, imagine like a room with just one door leading south
        movement = ["SOUTH"]
        dialogues = [
            "You find yourself in a room. The only way out is the way you came in."
        ]


# Movement Values
coordinates = [0, 0, 0]
current_room = Room.Spawn  # Where the player currently is

# Map
# (Room, Loot claimed, Enemy Killed)
game_map = {
    (0, 0, 0): (Room.Spawn(), True, True),
    (0, 1, 0): (Room.Crossroad(), False, False),
    (0, 2, 0): (Room.Room_e_south, False, False),
    (1, 1, 0): (Room.Crossroad, False, False),
    (2, 1, 0): (Room.Crossroad, False, False),
    (2, 2, 0): (Room.Room_e_south, False, False)

}

# Character Values
hit_points = 100
action_points = 100


# Functions

# Unpacker = Tuple -> List convertor. This function will get the tuple from game_map by getting the players coordinates.
# Returns the game_map tuple as a list for easy access.
# example: unpacker([0, 0, 0,]) -> [Room.Spawn(), True, True]
# Unpacker is also a kick ass name for a function
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


# ACL = Action Choice List, Works pretty much the same as MCL
# ACL will ONLY display fight button if current room has an enemy
def acl():
    output_message = ""
    actions = []

    room_unpacked = unpacker(coordinates)
    if len(room_unpacked) > 0:
        actions.append("MOVE")
    if not room_unpacked[2]:
        actions.append("FIGHT")
    actions.append("ITEMS")

    for i in actions:
        output_message += str(actions.index(i) + 1) + ": " + str(i.capitalize()) + "\n"
    return output_message, actions


# This is the standard movement function, All it does is change the coordinates depending on the players input.
# This function does not loop, so you can write any code after it.
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


# Gets ACL function and makes it work
# Since ACL returns 2 values (The list of available actions and the list itself) this function prints the list and then
# compares the user input to what is in the list.
# You can get a better understanding of this function by just printing it.
def choose_action():
    unpacked_room = unpacker(coordinates)
    print(random.choice(unpacked_room[0].dialogues))
    acl_tuple = acl()
    user_choice = input(acl_tuple[0])
    if user_choice.upper() in acl_tuple[1]:
        return user_choice.upper()


while True:
    unpacked = unpacker(coordinates)  # Turns tuple into a list so that its easier to work with.
    current_room = unpacked[0]  # Gets coordinates -> turns it in to a room -> changes current_room
    if choose_action() == "MOVE":
        print(random.choice(current_room.dialogues))  # Prints a random dialogue from the room class.
        print(mcl())  # Prints movement choice list
        move()  # Moves player through inputs
        print(coordinates)  # Prints new coordinates for debugging or whatever
