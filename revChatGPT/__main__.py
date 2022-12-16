import json
import textwrap
from os.path import exists
from os import getenv
from sys import argv, exit
import re

from revChatGPT.revChatGPT import Chatbot


class CaptchaSolver:
    """
    Captcha solver
    """
    @staticmethod
    def solve_captcha(raw_svg):
        """
        Solves the captcha

        :param raw_svg: The raw SVG
        :type raw_svg: :obj:`str`

        :return: The solution
        :rtype: :obj:`str`
        """
        # Get the SVG
        svg = raw_svg
        # Save the SVG
        print("Saved captcha.svg")
        with open("captcha.svg", "w", encoding='utf-8') as f:
            f.write(svg)
        # Get input
        solution = input("Please solve the captcha: ")
        # Return the solution
        return solution


def get_input(prompt):
    # prompt for input
    lines = []
    print(prompt, end="")
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    # Join the lines, separated by newlines, and print the result
    user_input = "\n".join(lines)
    # print(user_input)
    return user_input


def configure(sf):
    try:
        config_files = ["config.json"]
        xdg_config_home = getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_files.append(f"{xdg_config_home}/revChatGPT/config.json")
        user_home = getenv("HOME")
        if user_home:
            config_files.append(f"{user_home}/.config/revChatGPT/config.json")

        config_file = next((f for f in config_files if exists(f)), None)
        if config_file:
            with open(config_file, encoding="utf-8") as f:
                config = json.load(f)
        else:
            print("No config file found.")
            config = {}
        if "--debug" in argv:
            print("Debugging enabled.")
            debug = True
        else:
            debug = False
        verify_config(config)
        s=chatGPT_main(config, debug,sf)
        return s
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit()
    except Exception as exc:
        print("Something went wrong! Please run with --debug to see the error.")
        print(exc)
        exit()


def verify_config(config):
    """
    Verifies the config

    :param config: The config
    :type config: :obj:`dict`
    """
    # Check if the config is empty
    if 'email' in config or 'password' in config:
        print("Email and passwords are no longer supported")


def chatGPT_main(config, debug,p):
    print("Logging in...")
    chatbot = Chatbot(config, debug=debug,
                      captcha_solver=CaptchaSolver())
    if True:
        prompt = p#get_input("\nYou:\n")

        if "--text" not in argv:
            lines_printed = 0

            try:
                print("Chatbot: ")
                formatted_parts = []
                for message in chatbot.get_chat_response(prompt, output="stream"):
                    # Split the message by newlines
                    message_parts = message["message"].split("\n")

                    # Wrap each part separately
                    formatted_parts = []
                    for part in message_parts:
                        formatted_parts.extend(
                            textwrap.wrap(part, width=80))
                        for _ in formatted_parts:
                            if len(formatted_parts) > lines_printed + 1:
                                print(formatted_parts[lines_printed])
                                lines_printed += 1
                print(formatted_parts[lines_printed])
                return formatted_parts
            except Exception as exc:
                print("Response not in correct format!")
                print(exc)

        else:
            try:
                print("Chatbot: ")
                message = chatbot.get_chat_response(prompt)
                print(message["message"])
            except Exception as exc:
                print("Something went wrong!")
                print(exc)
                return 'wrong'





if __name__ == "__main__":
    configure('你好/我是一只猫娘')
