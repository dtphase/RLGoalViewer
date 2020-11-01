from env import SITE, HEADERS, REPLAYS_FOLDER, REPLAY_EXTENSION, PLAYLIST
import os
import sys
import requests
import json
import carball
import threading
import logging
import time
from shutil import move

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
video = 1
game = 1
replay_queue = []
max_queue_size = 3
queue_size = 0


class Replay:
    def __init__(self, replay_id, goals, path, player_id, is_next):
        self.replay_id = replay_id
        self.goals = goals
        self.path = path
        self.player_id = player_id
        d = threading.Thread(target=self.download_and_analyze, args=(player_id, is_next), daemon=True)
        d.start()
        if(is_next == False):
            d.join()

    def download_and_analyze(self, player_id, is_next):
        url = SITE + "api/replays/" + self.replay_id + "/file"
        replay_location = self.path
        res = requests.get(url, headers=HEADERS)
        with open(replay_location, 'wb') as replay_file:
            for chunk in res.iter_content(chunk_size=128):
                replay_file.write(chunk)
        if player_id != "":
            time.sleep(10)
            goal_frames = analyze_replay(replay_location, player_id)
            write_game_data_to_file(self.replay_id, goal_frames)
        if is_next == True:
            global replay_queue
            replay_queue.append(self)
            logging.debug(replay_queue)


def update_active_txt():
    global game
    global video
    folder =  REPLAYS_FOLDER + "/"
    filename = "active.txt"
    file_contents = str(video) + "\n" + str(game)
    absolute_path = folder + filename
    if not os.path.exists(os.path.dirname(absolute_path)):
        os.makedirs(os.path.dirname(absolute_path))
    with open(folder + filename, 'w') as file:
        file.write(str(file_contents))


def write_game_data_to_file(replay_id, goal_frames):
    global game
    global video
    folder =  REPLAYS_FOLDER + "/" + str(video) + "/"
    filename = "Game" + str(game) + ".txt"
    file_contents = "Game " + str(game) + ": Replay: " + replay_id + " Goals:\n"
    absolute_path = folder + filename
    if not os.path.exists(os.path.dirname(absolute_path)):
        os.makedirs(os.path.dirname(absolute_path))
    for goal in goal_frames:
        file_contents += str(goal)
    with open(folder + filename, 'w') as file:
        file.write(str(file_contents))

def print_json(j):
    print(json.dumps(j, sort_keys=True, indent=4))

def analyze_replay(replay_file, player_id):
    analysis_manager = carball.analyze_replay_file(replay_file)
    proto_game = analysis_manager.get_json_data()
    for player in proto_game["players"]:
        if player["id"]["id"] == player_id:
           """  if proto_game["players"][0]["goals"] < 1:
                print("Player scored 0 goals")
                return False """
        
        #print_json(proto_game)
    goals = proto_game["gameMetadata"]["goals"]
    goal_frames = []
    for goal in goals:
        if goal["playerId"]["id"] == player_id:
            print(goal["frameNumber"])
            goal_frames.append(str(goal["frameNumber"]) + "\n")
    return goal_frames
    

def get_replays(steam_id, playlist):
    query = {
        "player-id": "steam:" + steam_id,
        "count": 200
    }
    url = SITE + "api/replays"
    res = requests.get(url, headers=HEADERS, params=query)
    print(res.status_code)
    replay_list = json.loads(res.text)["list"]
    print_json(replay_list)
    for replay in replay_list:
        res2 = requests.get(url, headers=HEADERS, params={"id": replay["id"]})
        print_json(json.loads(res2.text))
        download_and_rename(video, game, replay["id"], steam_id)




def download_and_rename(video_id, game_id, replay_id, player_id):
    #x = threading.Thread(target=download_and_analyze, args=(video_id, game_id, replay_id, player_id), daemon=True)
    #x.start()
    global replay_queue
    global max_queue_size
    global queue_size
    filename = "active" + str(queue_size) + REPLAY_EXTENSION
    path = REPLAYS_FOLDER + "/" + filename
    if(len(replay_queue) == 0):
        r1 = Replay(replay_id, "", path, player_id, False)
        print(r1.path)
    while (queue_size < max_queue_size):
        Replay(replay_id, "", path, player_id, True)
        queue_size += 1
    global game
    url = SITE + "api/replays/" + replay_id + "/file"
    filename = "active" + REPLAY_EXTENSION
    replay_location = REPLAYS_FOLDER + "/" + filename
    res = requests.get(url, headers=HEADERS)

    print(res.status_code)

    """ with open(replay_location, 'wb') as replay_file:
        for chunk in res.iter_content(chunk_size=128):
            replay_file.write(chunk) """

    print("Downloaded to: " + replay_location)
    update_active_txt()
    """ if player_id != "":    
        goal_frames = analyze_replay(replay_location, player_id)
        write_game_data_to_file(replay_id, goal_frames) """
    new_filename_input = input('Enter the goal numbers that interested you\n')
    print(replay_queue)
    prefix = "Game_" + str(game_id) + "_"
    if len(new_filename_input) > 1:
        new_filename_array = new_filename_input.split()
        new_filename = ""
        for goal_number in new_filename_array:
            new_filename += "G" + goal_number
    else:
        new_filename = "G" + new_filename_input

    new_folder = REPLAYS_FOLDER + "/" + str(video_id) + "/"
    new_replay_location = new_folder + prefix + new_filename + REPLAY_EXTENSION

    if os.path.exists(new_folder) == False:
        os.mkdir(new_folder)

    move(replay_queue.pop(0).path, new_replay_location)
    queue_size -= 1
    
    game += 1

def get_next_replay():
    
    return


player_id = input("Please enter the Steam ID of the player whose replays you wish to download\n")#str(76561199023677910) #input("Please enter the Steam ID of the player whose replays you wish to download")
get_replays(player_id, PLAYLIST)

for argument in sys.argv:
    if argument == os.path.basename(__file__):
        continue
    print(argument)
    download_and_rename(str(video), str(game), argument, player_id)
    game += 1


#test id: "python download.py 7cd28bf2-0f3b-4d98-88b4-bcb79abb4ba1 c4dc9ee8-b67d-4591-9f40-d132807d9c0d"
#AppJack steamID 76561199023677910
#ahmad 76561198174027955