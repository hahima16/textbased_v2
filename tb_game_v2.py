import random


class Items:
    class Weapons:
        class Piwo:
            name = "Sharpened Can of Piwo"
            damage = 50


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

    class hallway_ew:
        movement = ["East", "West"]
        dialogues = [
            "You are in a hallway."
        ]

    class hallway_ns:
        movement = ["North", "South"]
        dialogues = [
            "You are in a hallway."
        ]


class EnemyContainer:

    class Overworked:
        health = 95
        damage = 15
        attack_chance = 80
        nickname = "Overworked Employee"
        drops = [
            "Employee ID"
        ]


# Values
coordinates = [0, 0, 0]
current_room = Room.Spawn  # Where the player currently is
health_points = 100
inventory = [
    Items.Weapons.Piwo
]

# Map
# (Room, Loot claimed, Enemy Killed, Enemy)
# Enemy killed = True if your room does not have an enemy.
game_map = {
    (0, 0, 0): (Room.Spawn(), True, True),
    (0, 1, 0): (Room.Crossroad(), False, False, EnemyContainer.Overworked),
    (0, 2, 0): (Room.Room_e_south, False, True),
    (1, 1, 0): (Room.Crossroad, False, False),
    (2, 1, 0): (Room.Crossroad, False, False),
    (2, 2, 0): (Room.Room_e_south, False, False)

}


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


def repacker(room, loot, enemytf, enemytype):  # Room, Loot, Enemytruefalse, Enemytype
    return tuple(room, loot, enemytf, enemytype) # does oppposite of unpacker


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


while health_points > 0:
    unpacked = unpacker(coordinates)  # Turns tuple into a list so that it's easier to work with.
    current_room = unpacked[0]  # Gets coordinates -> turns it in to a room -> changes current_room

    if not unpacked[2]:
        print("The room has an enemy with " + str(unpacked[3].health) + " HP.")
        chance = random.randint(0, 100)
        if unpacked[3].attack_chance > chance:
            health_points -= unpacked[3].damage
            print(unpacked[3].nickname + " Attacks you")
            print("You take " + str(unpacked[3].damage) + " Damage.")
            print("New health: " + str(health_points))
        else:
            print("The " + unpacked[3].nickname + " attacks you but misses!")

    stored = choose_action()

    attacks = 0
    hp_stored = None

    if stored == "MOVE":
        # print(random.choice(current_room.dialogues))  # Prints a random dialogue from the room class.
        print(mcl())  # Prints movement choice list
        move()  # Moves player through inputs
        print(coordinates)  # Prints new coordinates for debugging or whatever
    elif stored == "FIGHT":
        enemy = unpacked[3]
        weapon = max(inventory, key=lambda item: item.damage, default=None)  # i copy paste from chatgpt idk wtf this is
        attacks += 1
        hp_stored = unpacked[3].health - (weapon.damage * attacks)
        print(hp_stored)
        if hp_stored <= 0:
            game_map[tuple(coordinates)] = repacker(unpacked[0], unpacked[1], True, unpacked[3])
