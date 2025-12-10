from __future__ import annotations
import graphics as g
import os
import game_handler
import traceback
import inputs
import import_this


win: g.Window = None

games: dict[str, Game] = {}
game_previews: list[GamePreview] = []

main_menu_image: g.Image = None
game_name_text: g.Text = None
game_description_text: g.Text = None

frame_memory = 20
fps_text: g.Text = None
fps_list = [0.005 for i in range(frame_memory)]

num_game_previews = 0
scroll_offset = 0.0
selected_game = 0
preview_spacing = 360
scroll_speed = 3.0


class GamePreview:

    def __init__(self, game: Game, img: g.Image):
        self.game = game
        self.img = img

class Game:
    def __init__(self, file_name: str, img_path: str, name: str, description: str):
        self.file_name = file_name
        self.img_path = img_path
        self.name = name
        self.short_name = name
        if len(self.name) > 10:
            self.short_name = self.short_name[:6] + "..."

        self.description = description

def get_valid_games():
    games = {}
    for entry in os.scandir("games"):
        try:
            if entry.is_dir():
                path = entry.path
                valid = True
                valid &= os.path.exists(path + "/icon.png")
                valid &= os.path.exists(path + "/info.txt")
                valid &= os.path.exists(path + "/" + entry.name + ".py")
                with open(path + "/info.txt", "r") as file:
                    lines = file.readlines()
                    if valid:
                        desc = ""
                        for i in lines[1:]:
                            desc += i
                        games[entry.name] = Game(entry.name, path + "/icon.png", lines[0], desc)
        except Exception as e:
            if game_handler.debug_mode:
                print("Error while reading game with name: " + entry.name)
                traceback.print_exc()
    return games

def initialize():
    global main_menu_image, games, game_previews, num_game_previews, game_name_text, game_description_text, fps_text

    main_menu_image = g.Image(1920 // 2, 1080 // 2, win, "resources/main_menu.png")
    main_menu_image.resizeImage(1920, 1080)

    if game_handler.debug_mode:
        fps_text = g.Text(0, 0, win, fontSize=64, color=(255, 255, 255))

    game_name_text = g.Text(350, 790, win, fontSize=128, color=(20, 52, 100))
    game_description_text = g.Text(350, 880, win, fontSize=64, color=(20, 52, 100))
    #350, 880

    games = get_valid_games()

    game_previews = [GamePreview(games[game], g.Image(0, 0, win, games[game].img_path)) for game in games]
    while len(game_previews) < 7:
        game_previews.extend([GamePreview(games[game], g.Image(0, 0, win, games[game].img_path)) for game in games])
    game_previews = tuple(game_previews)
    num_game_previews = len(game_previews)

    game_name_text.setText(game_previews[selected_game].game.name)
    game_description_text.setText(game_previews[selected_game].game.description)

def load():
    main_menu_image.setVisibility(True)
    game_name_text.setVisibility(True)
    game_description_text.setVisibility(True)
    for prev in game_previews:
        prev.img.setVisibility(True)

def game_to_play() -> str:
    if inputs.hasKeybindBeenPressed("button1"):
        print(game_previews[selected_game].game.file_name)
        return game_previews[selected_game].game.file_name
    return ""

def update():
    global scroll_offset, selected_game, game_name_text, game_description_text

    if game_handler.debug_mode:
        fps_text.setText(str(int(frame_memory / sum(fps_list) * 100) / 100))
        fps_list[import_this.frame_num % frame_memory] = import_this.frame_time

    for i in range(num_game_previews):
        x = 960 + ((i + scroll_offset + selected_game + 3.0) % num_game_previews - 3.0) * preview_spacing
        game_previews[i].img.moveTo(x, 380)

        size = 320.0 + -abs(x - 960) / 1920 * 192
        game_previews[i].img.resizeImage(size, size)

    if inputs.hasJoystickChangedDirections() and (inputs.getJoystickQuadrant() == 0 or inputs.getJoystickQuadrant() == 2):
        direction = inputs.getJoystickQuadrant() - 1
        selected_game = (int(direction) + selected_game) % num_game_previews
        scroll_offset -= direction

        game_name_text.setText(game_previews[selected_game].game.name)
        game_description_text.setText(game_previews[selected_game].game.description)

    if scroll_offset > scroll_speed * import_this.frame_time:
        scroll_offset -= scroll_speed * import_this.frame_time
    elif scroll_offset < -scroll_speed * import_this.frame_time:
        scroll_offset += scroll_speed * import_this.frame_time

def unload():
    main_menu_image.setVisibility(False)
    game_name_text.setVisibility(False)
    game_description_text.setVisibility(False)
    for prev in game_previews:
        prev.img.setVisibility(False)
