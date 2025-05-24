import pygame
from threading import Thread
import os
import time
import requests
import json

x_vel_cmd, y_vel_cmd, yaw_vel_cmd = 0.0, 0.0, 0.0
joystick_opened = False

def joystick_client():
    joystick_use = True
    pygame.init()
    try:
        # get joystick
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joystick_opened = True
    except Exception as e:
        print(f"无法打开手柄：{e}")

    def handle_joystick_input():
        global exit_flag, x_vel_cmd, y_vel_cmd, yaw_vel_cmd, head_vel_cmd

        while True:
            # get joystick input
            pygame.event.get()
            # update robot command
            x_vel_cmd = -joystick.get_axis(1) * 1
            y_vel_cmd = -joystick.get_axis(0) * 1
            yaw_vel_cmd = -joystick.get_axis(3) * 1

            print(x_vel_cmd, y_vel_cmd, yaw_vel_cmd)

            #发送到WSL机器人服务端
            headers = {
                "Content-Type": "application/json; charset=UTF-8"
            }
            url = "http://172.17.15.170:8001/joystick"
            data = {
                "axis_0": y_vel_cmd,
                "axis_1": x_vel_cmd,
                "axis_3": yaw_vel_cmd
            }
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1).text
                print(response)
            except:
                pass

            pygame.time.delay(100)

    if joystick_opened and joystick_use:
        joystick_thread = Thread(target=handle_joystick_input)
        joystick_thread.start()
        joystick_thread.join()

if __name__ == '__main__':
    joystick_client()