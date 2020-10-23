import os
import sys
import requests
import json
import carball
from shutil import move

video = 1
game = 1

site = "https://ballchasing.com/"
token = "q0S3nwpBdV9Nl7AzhUgs36oq3htgcoCT9dCNOUCw"
headers = {"Authorization": token}
replay_extension = ".replay"
playlist = {"unranked-duels", "unranked-doubles", "unranked-standard", "ranked-duels", "ranked-doubles", "ranked-solo-standard", "ranked-standard", "private"}

def write_game_data_to_file(lines):
    folder = "C:/Users/stream/Documents/My Games/Rocket League/TAGame/Demos/" + str(game) + "/"
    filename = "Game" + str(game) + ".txt"
    file_contents = ""
    absolute_path = folder + filename
    if not os.path.exists(os.path.dirname(absolute_path)):
        os.makedirs(os.path.dirname(absolute_path))
    for line in lines:
        file_contents += line   
    with open(folder + filename, 'w+') as file:
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
    write_game_data_to_file(goal_frames)

def get_replays(steam_id, playlist):
    query = {
        "player-id": "steam:" + steam_id,
        "count": 200
    }
    url = site + "api/replays"
    res = requests.get(url, headers=headers, params=query)
    print(res.status_code)
    replay_list = json.loads(res.text)["list"]
    print_json(replay_list)
    game = 1
    for replay in replay_list:
        res2 = requests.get(url, headers=headers, params={"id": replay["id"]})
        print_json(json.loads(res2.text))
        download_and_rename(video, game, replay["id"], steam_id)
        game += 1




def download_and_rename(video_id, game_id, replay_id, player_id):
    url = site + "api/replays/" + replay_id + "/file"
    filename = "active" + replay_extension
    folder = "C:/Users/stream/Documents/My Games/Rocket League/TAGame/Demos"
    replay_location = folder + "/" + filename
    res = requests.get(url, headers=headers)

    print(res.status_code)

    with open(replay_location, 'wb') as replay_file:
        for chunk in res.iter_content(chunk_size=128):
            replay_file.write(chunk)

    print("Downloaded to: " + replay_location)

    if player_id != "":    
        analyze_replay(replay_location, player_id)

    new_filename_input = input('Enter the goal numbers that interested you\n')
    prefix = "Game_" + str(game_id) + "_"
    if len(new_filename_input) > 1:
        new_filename_array = new_filename_input.split()
        new_filename = ""
        for goal_number in new_filename_array:
            new_filename += "G" + goal_number
    else:
        new_filename = "G" + new_filename_input

    new_folder = folder + "/" + str(video_id) + "/"
    new_replay_location = new_folder + prefix + new_filename + replay_extension

    if os.path.exists(new_folder) == False:
        os.mkdir(new_folder)

    move(replay_location, new_replay_location)




player_id = input("Please enter the Steam ID of the player whose replays you wish to download\n")#str(76561199023677910) #input("Please enter the Steam ID of the player whose replays you wish to download")
get_replays(player_id, playlist)

for argument in sys.argv:
    if argument == os.path.basename(__file__):
        continue
    print(argument)
    download_and_rename(str(video), str(game), argument, player_id)
    game += 1


#test id: "python download.py 7cd28bf2-0f3b-4d98-88b4-bcb79abb4ba1 c4dc9ee8-b67d-4591-9f40-d132807d9c0d"
#AppJack steamID 76561199023677910