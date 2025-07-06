from twitch import twitch_helper
from functools import partial
import os
import keyboard
import subprocess
selected = 0
list = []

def goto_input():
    global selected
    global list
    result = input('go: ')
    try:
        selected = min(len(list)-1,abs(int(result)))
    except:
        print("invalid input")
    draw_list(list,selected)
def hotkey_callback_motion(dir):
    global selected
    global list
    if dir == 'up':
        selected = max(0,selected - 1)
    elif dir == 'down':
        selected = min(len(list) -1,selected + 1)
    draw_list(list,selected)

def refresh_list(helper):
    global list
    result = helper.get_streams()
    if result != "0":
        list = result
    draw_list(list,selected)

def open_stream():
    global list
    global selected
    stream_to_open = list[selected].user_name

    args = "\"--mute yes\""
    command = "streamlink https://www.twitch.tv/{} best --twitch-disable-ads --player mpv --player-args {} ".format(stream_to_open,args)
    subprocess.Popen(command) 
    
def draw_list(list,selected):
    
        os.system('cls')
        for index,item in enumerate(list):
            marker = ">" if (index == selected) else " "
            print("{}{}. {} - {} - {}".format(marker,index+1,item.user_name,item.game_name,item.viewer_count))
def main():
    global selected
    global list
    helper = twitch_helper()
    result = helper.get_streams()
    if result != "0":
        list = result
    draw_list(list,selected)
    activate_down = partial(hotkey_callback_motion,'down')
    activate_up = partial(hotkey_callback_motion,'up')

    keyboard.add_hotkey('j',activate_down,suppress=True)
    # keyboard.add_hotkey('g',goto_input,suppress=True)

    keyboard.add_hotkey('k',activate_up,suppress=True)
    keyboard.add_hotkey('enter',open_stream,suppress=True)
    keyboard.wait('esc')
if __name__ == '__main__':
    main()
