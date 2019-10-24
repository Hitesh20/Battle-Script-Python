from classes.game import Person,bcolors
from classes.magic import Spell
from classes.inventary import Item
import random

#create black magic
fire=Spell("Fire",20,600,"black")
thunder=Spell("thunder",15,550,"black")
bizzard=Spell("bizzard",30,650,"black")
meteor=Spell("meteor",10,500,"black")
quake=Spell("quake",40,700,"black")


#create white magic
cure=Spell("Cure",10,500,"white")
cura=Spell("Better Cure",11,700,"white")

player_spells=[fire,thunder,bizzard,meteor,quake,cure,cura]
enemy_spells=[fire,meteor,cure]

#create some item
potion=Item("Potion","potion","Heals 50 HP",50)
hipotion=Item("Hi-potion","potion","heals 100 HP",100)
super_potion=Item("Super Potion","potion","heals 500 HP",500)
elixer=Item("elixer","elixer","Fully restores HP/MP of one party member",9999)
hielixer=Item("MegaElixer","elixer","Fully restores HP/MP of party",9999)
grenade=Item("Grenade","attack","Deals 500 damage",500)

player_items=[{"item":potion,"quantity":15},{"item":hipotion,"quantity":5},{"item":super_potion,"quantity":5},
              {"item":elixer,"quantity":5},{"item":hielixer,"quantity":5},{"item":grenade,"quantity":5}]


#Instantiate People
player1 = Person("Hitesh  :",4000,200,300,100,player_spells,player_items)
player2 = Person("Kohli   :",6000,150,200,100,player_spells,player_items)
player3 = Person("Gandotra:",5000,100,250,100,player_spells,player_items)

enemy1 = Person("Ankit   :",20000,700,500,300,enemy_spells,[])
enemy2 = Person("Tripathi:",2000,300,150,100,enemy_spells,[])
enemy3 = Person("Anubhav :",1500,400,200,150,enemy_spells,[])

players=[player1,player2,player3]
enemies=[enemy1,enemy2,enemy3]


print(bcolors.FAIL+bcolors.BOLD + "AN ENEMY ATTACKS"+bcolors.ENDC)

running = True
i=0
while running:
    print("==========================")

    print("\n\n")
    print("NAME            HP                                            MP")


    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()



    for player in players:

        enemy=player.choose_action()
        choice= input(" Choose Action : ")
        index=int(choice) - 1


    #To choose Attack
        if index == 0:
            dmg=player.generate_damage()
            enemy=player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked" + enemies[enemy].name+" for ",dmg," points of damage.")


            if enemies[enemy].get_hp()==0:
                print(enemies[enemy].name.replace(" ",""),"has died.\n")
                del enemies[enemy]

     #to choose magic
        elif index==1:
            player.choose_magic()
            magic_choice=int(input("    Choose Magic : "))-1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg=spell.generate_damage()

            current_mp=player.get_mp()
            if spell.cost>current_mp:
                print(bcolors.FAIL+"\n Not enough MP\n"+bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKGREEN+"\n"+spell.name+"heals for",str(magic_dmg),"HP."+bcolors.ENDC)
            elif spell.type =='black':
                enemy=player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals for", str(magic_dmg), "HP." + bcolors.ENDC)


            print(bcolors.OKBLUE+"\n"+spell.name+" deals",str(magic_dmg),"points of damage to "+
                  enemies[enemy].name+bcolors.ENDC)

            if enemies[enemy].get_hp()==0:
                print(enemies[enemy].name.replace(" ",""),"has died.\n")
                del enemies[enemy]



      #to choose items

        elif index==2:
            player.choose_item()
            item_choice=int(input(" Choose item"))-1

            if item_choice== -1:
                continue

            item=player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"]==0:
                print(bcolors.FAIL+"\n"+"None left..."+bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -=1




            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN+"\n"+item.name+"heals for",str(item.prop),"HP"+bcolors.ENDC)
            elif item.type =="elixer":
                if item.name=="MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp=player.maxhp
                    player.mp=player.maxmp
                print(bcolors.OKGREEN+"\n"+item.name+" Fully recovers hp/mp."+bcolors.ENDC)
            elif item.type=="attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals",str(item.prop),"points of damage to "+enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ",""), "has died.\n")
                    del enemies[enemy]

    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + bcolors.BOLD + "YOC WIN" + bcolors.ENDC)
        running = False

    if defeated_players == 2:
        print(bcolors.FAIL + bcolors.BOLD + "YOC LOST" + bcolors.ENDC)
        running = False

    print("\n")

    #Enemy Choice
    for enemy in enemies:
        enemy_choice=random.randrange(0,2)
        if enemy_choice==0:
            target=random.randrange(0,3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ",""),"attacked"+ players[target].name.replace(" ","") +" for", enemy_dmg)
        elif enemy_choice==1:
            spell, magic_dmg=enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKGREEN+spell.name+"heals"+enemy.name+" for",str(magic_dmg),"HP."+bcolors.ENDC)
            elif spell.type =='black':
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" +enemy.name.replace(" ","")+"'s "+ spell.name + " deals for", str(magic_dmg), "points of damage " + players[target].name.replace(" ","")+ bcolors.ENDC)
            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", ""), "has died.\n")
                del players[player]

            print("Enemy chose", spell," damage is",magic_dmg)




