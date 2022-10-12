import pygame
from animation import AnimateSprite

class Entity(AnimateSprite):

    def __init__(self, name, x, y, has_a_portrait=False):
        super().__init__(name)
        # graphic setup
        self.image = self.get_image(32, 00)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        # movement & hitboxes
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.direction = pygame.math.Vector2()

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 2}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        # dialog
        self.has_a_portrait = has_a_portrait

    def save_location(self): self.old_position = self.position.copy()

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.position[0] += self.direction.x * self.speed
        self.position[1] += self.direction.y * self.speed
        if self.direction.x > 0: self.change_animation('right')
        elif self.direction.x < 0: self.change_animation('left')
        elif self.direction.y < 0: self.change_animation('up')
        elif self.direction.y > 0: self.change_animation('down')

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
        	direction = (player_vec - enemy_vec).normalize()
        else:
        	direction = pygame.math.Vector2()

        return (distance, direction)

class Player(Entity):

    def __init__(self):
        super().__init__('player', 0, 0, has_a_portrait=False)
        self.inventory = {
            "coin": 0
        }

class Item(Entity):
    def __init__(self, name, x, y, status):
        super().__init__(name, x, y, has_a_portrait=False)
        # graphic setup
        self.change_status(status)
        self.image = self.get_image(00, 00)
        self.image.set_colorkey([0, 0, 0])

    def change_animation(self, name):
        pass

    def move_back(self):
        pass

    def give(self, player):
        pygame.mixer.Sound.play(pygame.mixer.Sound("../sounds/coin.ogg"))
        if self.status in player.inventory:
            player.inventory[self.status] += 1
        else:
            player.inventory[self.status] = 1
        self.kill()



class NPC(Entity):

    def __init__(self, name, nb_points, dialog, speed=2, has_a_portrait=False):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.current_point = 0

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': speed}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        # dialog
        self.has_a_portrait = has_a_portrait


    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.direction.y = 1
            self.position[1] += self.speed * self.direction.y
            self.change_animation('down')
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.direction.y = -1
            self.position[1] += self.speed * self.direction.y
            self.change_animation('up')
        if current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.direction.x = -1
            self.position[0] += self.speed * self.direction.x
            self.change_animation('left')
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.direction.x = 1
            self.position[0] += self.speed * self.direction.x
            self.change_animation('right')

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    # set the npc position
    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
