import random
from Pyhton3_udemy.RPG_Battle.classes.game import Person, bcolors
from Pyhton3_udemy.RPG_Battle.classes.magic import Spell
from Pyhton3_udemy.RPG_Battle.classes.inventory import Item

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")
curaga = Spell("Curaga", 50, 5000, "white")

# Create Items

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)

elixer = Item("Elixer", "elixer", "Fully restores HP\MP of one party member", 9999)
megaelixer = Item("MegaExlixer", "elixer", "Fully restores party's HP\MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 points of damage", 500)

# Instantiate Players
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, quake, cura, curaga]
player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": megaelixer, "quantity": 2}, {"item": grenade, "quantity": 5},]


player1 = Person("Bard", 3000, 100, 280, 34, player_spells, player_items)
player2 = Person("GPT4", 3200, 120, 300, 34, player_spells, player_items)
player3 = Person("LaMA", 2800, 75, 250, 34, player_spells, player_items)

enemy1 = Person("Ian ", 1200, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Ding" ,10000, 700, 500, 25, enemy_spells, [])
enemy3 = Person("Nepo", 1200, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("====================================")
    print("\n\n")
    print("Name               HP                                     MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1
        if index == 0:
            dmg = player.generate_damage()
            enemy_id = player.choose_target(enemies)
            enemies[enemy_id].take_dmg(dmg)
            print("You attacked " + enemies[enemy_id].name.replace(" ", "") + " for", dmg, "points of damage")

            if enemies[enemy_id].get_hp() == 0:
                print(bcolors.FAIL + enemies[enemy_id].name.replace(" ", "") +
                      " has died." + bcolors.ENDC)
                del enemies[enemy_id]
                print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                running = False
                continue

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." +
                      bcolors.ENDC)
            elif spell.type == "black":
                enemy_id = player.choose_target(enemies)
                enemies[enemy_id].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) +
                      " points of damage to " + enemies[enemy_id].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy_id].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy_id].name.replace(" ", "") +
                          " has died." + bcolors.ENDC)
                    del enemies[enemy_id]
                    print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                    running = False
                    continue

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop),
                      "HP" + bcolors.ENDC)

            elif item.type == "elixer":
                if item.name == "MegaExlixer":
                    for p in players:
                        p.hp = p.maxhp
                        p.mp = p.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name +
                          " fully restores all party members HP/MP" + bcolors.ENDC)

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name +
                          " fully restores player's HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy_id = player.choose_target(enemies)
                enemies[enemy_id].take_dmg(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                    "points of damage to " + enemies[enemy_id].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy_id].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy_id].name.replace(" ", "") +
                          " has died." + bcolors.ENDC)
                    del enemies[enemy_id]
                    if len(enemies) == 0:
                        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
                        running = False
                        continue


    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False
    # Check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    # Enemy attack
    print("\n")
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            # Enemy chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[enemy_id].generate_damage()
            players[target].take_dmg(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " +
                  players[target].name.replace(" ", "") + " for", enemy_dmg, "points of damage")
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            while spell == None and magic_dmg == None:
                spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") +
                      " for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)
                players[target].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " +
                      spell.name + " deals " + str(magic_dmg) + " points of damage to " +
                      players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + players[target].name.replace(" ", "") +
                          " has died." + bcolors.ENDC)
                    del players[player]

