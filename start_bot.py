#!python3

import sys
import asyncio
import logging
import argparse

import sc2
from sc2 import Race
from sc2.player import Bot

from bot import MyBot

def main(is_master, map_name, races, portconfig, replay_path, log_path, step_time_limit=None, game_time_limit=None):
    portconfig = sc2.portconfig.Portconfig.from_json(portconfig)
    i = 0 if is_master else 1

    player_config = [Bot(Race[r], None) for r in races]
    player_config[i].ai = MyBot()

    if log_path is not None:
        logger = logging.getLogger("sc2")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

    if is_master:
        g = sc2.main._host_game(
            sc2.maps.get(map_name),
            player_config,
            realtime=False,
            save_replay_as=replay_path,
            portconfig=portconfig,
            step_time_limit=step_time_limit,
            game_time_limit=game_time_limit
        )
    else:
        g = sc2.main._join_game(
            player_config,
            realtime=False,
            save_replay_as=replay_path,
            portconfig=portconfig,
            step_time_limit=step_time_limit,
            game_time_limit=game_time_limit
        )

    result = asyncio.get_event_loop().run_until_complete(g)
    print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a game against external server')
    parser.add_argument('--master', action='store_true', help='this is the master (creates the game)')
    parser.add_argument('--replay-path', nargs=1, default='replay.SC2Replay')
    parser.add_argument('--log-path', nargs=1, default='-')
    parser.add_argument('--step-time-limit', nargs=1, default=None, help="Max seconds per step (realtime seconds)")
    parser.add_argument('--game-time-limit', nargs=1, default=None, help="Max seconds per game (gametime seconds)")
    parser.add_argument('map_name', help='name of the game map')
    parser.add_argument('races', help='player races as comma-separated list')
    parser.add_argument('portconfig', help='port configuration as json')
    args = parser.parse_args()

    races = args.races.split(",")

    assert all(r in ["Random", "Zerg", "Protoss", "Terran"] for r in races)

    main(
        args.master, args.map_name, races, args.portconfig,
        args.replay_path[0],
        args.log_path[0] if args.log_path[0] != "-" else None,
        float(args.step_time_limit[0]) if args.step_time_limit else None,
        float(args.game_time_limit[0]) if args.game_time_limit else None,
    )
