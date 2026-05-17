class SceneManager:
    def __init__(self):
        self._scenes = {}
        self.current = None

    def register(self, key, scene):
        self._scenes[key] = scene

    def switch(self, key):
        self.current = self._scenes[key]
        self.current.on_enter()

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)
