class Bullet:
    def __init__(self, x, y, facing, owner_id):
        self.x = x
        self.y = y
        self.facing = facing
        self.velocity = 10 * facing
        self.owner_id = owner_id
