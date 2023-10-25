class Scene:
    def __init__(self, file_name, bg_col, fg_col, line_spacing=30): 
        self.file_name = file_name
        self.txt_col = fg_col
        self.bg_col = bg_col
        self.line_spacing = line_spacing
        self.file = open(os.path.join(SCENE_PATH, self.file_name), 'r')

    def play(self, app):
        app._display_surf.fill(self.bg_col)
        pygame.display.update()
        i = 0
        for line in self.file.readlines():
            data = re.findall(r'"(.+?)"', line)[0]
            if line[0] == ">":
                app._display_surf.blit(app.font.render(data, True, self.txt_col), (250, 330 + self.line_spacing * i))
                pygame.display.update()
                i += 1
            elif line[0] == "-":
                if ".ogg" in data:
                    play_sound(data)
                elif ".mp3" in data:
                    fn = data.split("#")[0]
                    play_music(fn, -1 if "#" not in data else int(data.split("#")[1]))
            elif line[0] == ".":
                pause(int(data), app.FPS)
