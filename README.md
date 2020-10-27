# RLGoalViewer

TODO:
Laravel site
Faster
Continue from last game checked
Download and analyze 1 replay with goals (check) in advance in seperate thread

Error:


Traceback (most recent call last):
  File "c:\Users\stream\.vscode\extensions\ms-python.python-2020.2.64397\pythonFiles\ptvsd_launcher.py", line 48, in <module>
    main(ptvsdArgs)
  File "c:\Users\stream\.vscode\extensions\ms-python.python-2020.2.64397\pythonFiles\lib\python\old_ptvsd\ptvsd\__main__.py", line 432, in main
    run()
  File "c:\Users\stream\.vscode\extensions\ms-python.python-2020.2.64397\pythonFiles\lib\python\old_ptvsd\ptvsd\__main__.py", line 316, in run_file
    runpy.run_path(target, run_name='__main__')
  File "C:\Python37\lib\runpy.py", line 263, in run_path
    pkg_name=pkg_name, script_name=fname)
  File "C:\Python37\lib\runpy.py", line 96, in _run_module_code
    mod_name, mod_spec, pkg_name, script_name)
  File "C:\Python37\lib\runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "d:\RLGoalViewer\download.py", line 110, in <module>
    get_replays(player_id, playlist)
  File "d:\RLGoalViewer\download.py", line 64, in get_replays
    download_and_rename(video, game, replay["id"], steam_id)
  File "d:\RLGoalViewer\download.py", line 86, in download_and_rename
    analyze_replay(replay_location, player_id)
  File "d:\RLGoalViewer\download.py", line 33, in analyze_replay
    analysis_manager = carball.analyze_replay_file(replay_file)
  File "C:\Python37\lib\site-packages\carball\decompile_replays.py", line 48, in analyze_replay_file
    _json = decompile_replay(replay_path)
  File "C:\Python37\lib\site-packages\carball\decompile_replays.py", line 23, in decompile_replay
    return parse_replay(buf)
Exception: Not enough data to decode Trailer
