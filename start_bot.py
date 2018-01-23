#!python3
# Usage: python run_external.py [--host]

import argparse

import sys
import asyncio

import sc2
from sc2 import Race
from sc2.player import Bot

from bot import MyBot

def main(is_master, map_name, races, portconfig):
    portconfig = sc2.portconfig.Portconfig.from_json(portconfig)

    player_config = [Bot(Race[r], None) for r in races]
    player_config[0 if is_master else 1].ai = MyBot()

    if is_master:
        g = sc2.main._host_game(
            sc2.maps.get(map_name),
            player_config,
            realtime=False,
            portconfig=portconfig
        )
    else:
        g = sc2.main._join_game(
            player_config,
            realtime=False,
            portconfig=portconfig
        )

    result = asyncio.get_event_loop().run_until_complete(g)
    print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--master', action='store_true', help='this is the master (creates the game)')
    parser.add_argument('map_name', type=str, help='name of the game map')
    parser.add_argument('races', type=str, help='player races as comma-separated list')
    parser.add_argument('portconfig', type=str, help='port configuration as json')
    args = parser.parse_args()

    races = args.races.split(",")

    assert all(r in ["Random", "Zerg", "Protoss", "Terran"] for r in races)

    main(args.master, args.map_name, races, args.portconfig)
