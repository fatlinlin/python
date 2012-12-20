import os
import pystache

SERVER_DIR = ""
TEMPLATES_DIR = os.path.join(SERVER_DIR, "templates")
TEMPLATE_EXT = ".mustache"

def renderFile(path, json):
    with open(path) as th:
        template_string = th.read()
    return pystache.render(template_string, json)

def load_template(name):
    with open(get_template(name)) as th:
        return pystache.parse(unicode(th.read()))

def get_template(game):
    return os.path.join(TEMPLATES_DIR, game + TEMPLATE_EXT)

def render(game, gameJson, mainJson):
    game_body = renderFile(get_game_template(game), gameJson)
    mainJson["game_body"] = game_body
    return renderFile(get_template("game"), mainJson)

class GamePresenter:

    def __init__(self, name, key, scripts):
        self.name = name
        self.key = key
        self.renderer = pystache.Renderer()
        self.scripts = [{"path" : "/js/{}.js".format(script)} for script in scripts]
        self.game_template = load_template(key)
        self.main_template = load_template("game")

    def render(self, gameJson):
        game_body = self.renderer.render(self.game_template, gameJson)
        main_json = {
            "title" : self.name,
            "scripts" : self.scripts,
            "game_body" : game_body
            }
        return self.renderer.render(self.main_template, main_json)
