import os
import sys
import requests

def download_and_rename(video_id, game_id, replay_id):
    site = "https://ballchasing.com/"
    url = site + "api/replays/" + replay_id + "/file"
    token = "q0S3nwpBdV9Nl7AzhUgs36oq3htgcoCT9dCNOUCw"
    headers = {"Authorization": token}
    extension = ".replay"
    filename = "active" + extension
    folder = "C:/Users/stream/Documents/My Games/Rocket League/TAGame/Demos"
    replay_location = folder + "/" + filename
    res = requests.get(url, headers=headers)

    print(res.status_code)

    with open(replay_location, 'wb') as replay_file:
        for chunk in res.iter_content(chunk_size=128):
            replay_file.write(chunk)

    print("Downloaded to: " + replay_location)

    new_filename_input = input('Enter the goal numbers that interested you\n')
    prefix = "Game_" + game_id + "_"
    if len(new_filename_input) > 1:
        new_filename_array = new_filename_input.split()
        new_filename = ""
        for goal_number in new_filename_array:
            new_filename += "G" + goal_number
    else:
        new_filename = "G" + new_filename_input

    new_folder = folder + "/" + video_id + "/"
    new_replay_location = new_folder + prefix + new_filename + extension

    if os.path.exists(new_folder) == False:
        os.mkdir(new_folder)

    os.rename(replay_location, new_replay_location)


video = 1
game = 1

for argument in sys.argv:
    if argument == os.path.basename(__file__):
        continue
    print(argument)
    download_and_rename(str(video), str(game), argument)
    game += 1


#test id: "python download.py 7cd28bf2-0f3b-4d98-88b4-bcb79abb4ba1 c4dc9ee8-b67d-4591-9f40-d132807d9c0d"