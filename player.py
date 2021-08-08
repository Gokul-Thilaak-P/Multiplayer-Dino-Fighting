class Player:
    def __init__(self, id, x, y, width, height, name, is_connected):
        self.id = id
        self.x = x
        self.y = y
        self.name = name
        self.width = width
        self.height = height
        self.is_connected = is_connected
        self.is_game_over = False
        self.ready_to_play = False
        self.velocity = 6
        self.isjumping = False
        self.jump_pos = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.health = 5
        self.bullets = []
        self.score = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
