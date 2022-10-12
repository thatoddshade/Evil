from animation import AnimateSprite
import pygame
import settings


class Entity(AnimateSprite):

    def __init__(self, name, x, y, width=32, height=32, portrait=False):
        super().__init__(name)
        # graphic setup
        self.image = self.get_image(32, 00)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        # movement & hitboxes
        self.position = [x, y]
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.direction = pygame.math.Vector2()

        # stats
        self.stats = {
            'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 2
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        # dialog
        self.portrait = portrait

    def save_location(self): self.old_position = self.position.copy()

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.position[0] += self.direction.x * self.speed * settings.delta_time
        self.position[1] += self.direction.y * self.speed * settings.delta_time

        if self.direction.x > 0:
            self.change_animation('right')
        elif self.direction.x < 0:
            self.change_animation('left')
        elif self.direction.y < 0:
            self.change_animation('up')
        elif self.direction.y > 0:
            self.change_animation('down')
        # else:
        #     self.change_animation(self.current_animation)

    def update(self):
        self.rect.topleft = self.position
        self.hitbox.midbottom = self.rect.midbottom
        # pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect(self.rect.x, self.rect.y, self.hitbox.width, self.hitbox.height), 1, 8)

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.hitbox.midbottom = self.rect.midbottom

    def draw_outline(self, wideness=1, color=(255, 255, 255)):
        display = self.image
        loc = (0, 0)
        mask = pygame.mask.from_surface(self.image)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
            n += 1
        pygame.draw.polygon(display, color, mask_outline, wideness)

    def get_distance_direction(self, target):
        entity_vec = pygame.math.Vector2(self.rect.center)
        target_vec = pygame.math.Vector2(target.rect.center)
        distance = (target_vec - entity_vec).magnitude()

        if distance > 0:
            direction = (target_vec - entity_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)


class Player(Entity):

    def __init__(self):
        super().__init__(
            'player', 0, 0, width=32, height=32, portrait=False
        )
        self.inventory = [
            {"type": "coin", "number": 1},
            {"type": "oak_log", "number": 64},
            {"type": "oak_log", "number": 64}
        ]


class Item(Entity):
    def __init__(self, x, y, status):
        super().__init__("items", x, y)
        # graphic setup
        self.width, self.height = 16, 16
        self.change_status(status)
        self.image = self.get_image(00, 00)
        self.image.set_colorkey([0, 0, 0])

    def change_animation(self, name): pass

    def move_back(self): pass

    def give(self, player):
        pygame.mixer.Sound.play(pygame.mixer.Sound("../sounds/coin.ogg"))

        for i in range(0, len(player.inventory)):
            if player.inventory[i]["type"] == self.status:
                if player.inventory[i]["number"] < settings.default_max_stack:
                    player.inventory[i]["number"] += 1
                    break
                # else:
                #     continue
            if i >= len(player.inventory) - 1:
                player.inventory.append({"type": self.status, "number": 1})

        self.kill()


class NPC(Entity):
    def __init__(self, name, nb_points, width=32, height=32, dialog=[''],
                 speed=2, portrait=False
                 ):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.current_point = 0

        # stats
        self.stats = {
            'health': 100, 'energy': 60, 'attack': 10, 'magic': 4,
            'speed': speed
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        # dialog
        self.portrait = portrait

    def move_to_next_point(self):
        self.direction.x, self.direction.y = 0, 0
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(
            current_rect.x - target_rect.x
        ) < 3:
            self.direction.y = 1
            self.move()

        elif current_rect.y > target_rect.y and abs(
            current_rect.x - target_rect.x
        ) < 3:
            self.direction.y = -1
            self.move()

        if current_rect.x > target_rect.x and abs(
            current_rect.y - target_rect.y
        ) < 3:
            self.direction.x = -1
            self.move()

        elif current_rect.x < target_rect.x and abs(
            current_rect.y - target_rect.y
        ) < 3:
            self.direction.x = 1
            self.move()
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
