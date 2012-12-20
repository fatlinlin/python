import os
import pystache

SERVER_DIR = ""
TEMPLATES_DIR = os.path.join(SERVER_DIR, "templates")

def renderFile(path, json):
    with open(path) as th:
        template_string = th.read()
    return pystache.render(template_string, json)

def get_game_template(game):
    return os.path.join(TEMPLATES_DIR, game + ".html")

def render(game, gameJson, mainJson):
    game_body = renderFile(get_game_template(game), gameJson)
    mainJson["game_body"] = game_body
    return renderFile(get_game_template("game"), mainJson)
