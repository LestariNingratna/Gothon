from sys import exit
from random import randint
import time
import math

class Scene:
    def enter(self, hero):
        print("This scene is not yet configured. Subclass it and implement enter().")
        exit(1)

class Engine:
    def __init__(self, scene_map, hero):
        self.scene_map = scene_map
        self.hero = hero

    def play(self):
        current_scene = self.scene_map.opening_scene()
        while True:
            print("\n--------")
            next_scene_name = current_scene.enter(self.hero)
            current_scene = self.scene_map.next_scene(next_scene_name)

class Death(Scene):
    quips = [
        "You died. You kinda suck at this.",
        "Your mom would be proud...if she were smarter.",
        "Such a loser.",
        "I have a small puppy that's better at this."
    ]
    def enter(self, hero):
        print(Death.quips[randint(0, len(self.quips) - 1)])
        exit(1)

class CentralCorridor(Scene):
    def enter(self, hero):
        print("The Gothons of Planet Percal #25 have invaded your ship and destroyed your entire crew.")
        print("You are the last surviving member and must get the neutron destruct bomb from the Weapons Armory.")
        print("A Gothon jumps out, blocking your way!")
        
        action = input("> ")
        if action == "shoot!":
            print("Your shot misses! The Gothon kills you.")
            return 'death'
        elif action == "dodge!":
            print("You slip, hit your head, and get eaten.")
            return 'death'
        elif action == "tell a joke":
            print("The Gothon laughs! You take your chance and escape.")
            return 'laser_weapon_armory'
        else:
            print("DOES NOT COMPUTE!")
            return 'central_corridor'

class LaserWeaponArmory(Scene):
    def enter(self, hero):
        print("You find the neutron bomb, but it's locked by a keypad. Guess the 3-digit code!")
        code = f"{randint(1,9)}{randint(1,9)}{randint(1,9)}"
        guesses = 0
        while guesses < 10:
            guess = input("[keypad]> ")
            if guess == code:
                print("The lock opens! You grab the bomb and run to the bridge.")
                return 'the_bridge'
            else:
                print("BZZZZEDDD!")
                guesses += 1
        print("You failed! The Gothons kill you.")
        return 'death'

class TheBridge(Scene):
    def enter(self, hero):
        print("You enter the bridge with the bomb. The Gothons stare at you.")
        action = input("> ")
        if action == "throw the bomb":
            print("You panic and throw the bomb! The Gothons kill you.")
            return 'death'
        elif action == "slowly place the bomb":
            print("You carefully place the bomb and escape!")
            return 'escape_pod'
        else:
            print("DOES NOT COMPUTE!")
            return "the_bridge"

class EscapePod(Scene):
    def enter(self, hero):
        print("You reach the escape pods. Pick one (1-5).")
        good_pod = randint(1, 5)
        guess = input("[pod #]> ")
        if guess.isdigit() and int(guess) == good_pod:
            print("You escape successfully! The ship explodes behind you. You won!")
            return 'win'
        else:
            print("Wrong pod! It malfunctions and kills you.")
            return 'death'

class Win(Scene):
    def enter(self, hero):
        print("You Win! Good Job!")
        exit(0)

class Final(Scene):
    def enter(self, hero):
        monster = Monster("Gothon Boss")
        print(f"{hero.name}, you face the final boss {monster.name}! Prepare to fight!")
        combat = Combat()
        return combat.combat(hero, monster)

class Combat:
    def combat(self, hero, monster):
        round_num = 1
        while True:
            print(f"Round {round_num}")
            print(f"Your HP: {hero.hp}, {monster.name}'s HP: {monster.hp}")
            print("1) Attack, 2) Defend")
            action = input("> ")
            if action == "1":
                hero.attack(monster)
            elif action == "2":
               hero.defend()
            else:
                print("Invalid action!")
                continue
            if monster.hp > 0:
                monster.attack(hero)
            if hero.hp <= 0:
                return 'death'
            if monster.hp <= 0:
                return 'win'
            hero.rest()
            monster.rest()
            round_num += 1

class Map:
    scenes = {
        'central_corridor': CentralCorridor(),
        'laser_weapon_armory': LaserWeaponArmory(),
        'the_bridge': TheBridge(),
        'escape_pod': EscapePod(),
        'death': Death(),
        'final_fight': Final(),
        'win': Win()
    }
    def __init__(self, start_scene):
        self.start_scene = start_scene
    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)
    def opening_scene(self):
        return self.next_scene(self.start_scene)

class Human:
    def __init__(self, name, hp, power, rate):
        self.name = name
        self.hp = hp
        self.power = power
        self.rate = rate
    def attack(self, target):
        damage = int(self.power / 5 + randint(0, 10))
        target.hp -= damage
        print(f"{self.name} attacks {target.name}! {target.name}'s HP decreases by {damage}.")
    def defend(self):
        self.hp += 10
        print(f"{self.name} defends and gains 10 HP!")
    def rest(self):
        self.hp += self.rate

class Hero(Human):
    def __init__(self, name):
        super().__init__(name, hp=1000, power=200, rate=5)

class Monster(Human):
    def __init__(self, name):
        super().__init__(name, hp=5000, power=250, rate=5)

a_map = Map('central_corridor')
a_hero = Hero('Lestari')
a_game = Engine(a_map, a_hero)
a_game.play()
 
