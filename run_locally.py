import json

from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

from bot import MyBot

def main():
    with open("botinfo.json") as f:
        info = json.load(f)

    race = Race[info["race"]]

    run_game(maps.get("Abyssal Reef LE"), [
        Bot(race, MyBot()),
        Computer(Race.Random, Difficulty.Medium)
    ], realtime=False, step_time_limit=2.0, game_time_limit=20.0)

if __name__ == '__main__':
    main()
