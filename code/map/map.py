from dataclasses import dataclass
from entity import NPC
from item import ItemSprite
from particle import Particle
import settings
import pygame
import pytmx
import pyscroll
import random


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    items: list[ItemSprite]


class MapManager:
    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "village"

        self.register_map("village", portals=[], npcs=[
            NPC("umbra", nb_points=4, dialog=[["player", "Hello ! "], ["player",
                "How are you feeling ? Who are you ? What is your name ?"],
                ["umbra", "Not fine at all."], ["umbra", "I am someone..."],
                ["umbra", "I am someone who hasn't any soul."],
                ["umbra", "But I can read in souls."],
                ["umbra", "My name is written on the top-left of the dialog box."],
                ["player", "whot's a dialog box ?"]], speed=2, portrait=True),

            NPC("wassa", nb_points=1, dialog=[["player", "Bonjour."],
                ["umbra", "Salue."], ["cooper", "Hola."],
                ["umbra", "Buongiorno."], ["wassa", "Gutentag."],
                ["umbra", "Hello."]], speed=2, portrait=True)
        ])

        self.teleport_player("player")
        self.teleport_npcs()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.hitbox.colliderect(
                    self.player.rect
            ) and type(sprite) is NPC:
                dialog_box.execute(sprite, sprite.dialog)

    def check_collisions(self):
        # portals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.hitbox.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.hitbox.colliderect(self.player.rect):
                    sprite.speed = 0
                    sprite.draw_outline()
                else:
                    sprite.speed = sprite.stats["speed"]

            if sprite.hitbox.collidelist(self.get_walls()) > -1 and not type(
              sprite) is Particle:
                sprite.move_back()

        # items
        for sprite in self.get_group().sprites():
            if type(sprite) is ItemSprite:
                # get the distance and the direction
                distance = sprite.get_distance_direction(
                    self.player
                )[0]

                direction = sprite.get_distance_direction(
                    self.player
                )[1]

                if distance < 64:
                    sprite.direction = direction
                    sprite.move()
                    if distance < 16:
                        sprite.give(self.player)

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # load the map
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data,
            self.screen.get_size()
        )
        map_layer.zoom = settings.ZOOM

        # set lists to store rectangles
        walls = []
        items = []

        for obj in tmx_data.objects:
            properties = obj.__dict__
            # since Tiled 1.9 type is renamed "class"
            if "class" in properties:
                if properties["class"] == "collision":
                    walls.append(
                        pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    )
                if properties["class"] == "item":
                    items.append(ItemSprite(obj.x, obj.y, obj.name))

            elif "type" in properties:
                if properties["type"] == "collision":
                    walls.append(
                        pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    )
                if properties["type"] == "item":
                    items.append(ItemSprite(obj.x, obj.y, obj.name))

        # draw the layer group and add elements to group
        group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=settings.DEFAULT_SPRITE_LAYER
        )
        group.add(self.player)
        for npc in npcs:
            group.add(npc)
        for item in items:
            group.add(item)

        # create a new object Map
        self.maps[name] = Map(
            name, walls, group, tmx_data, portals, npcs, items
        )

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
        for npc in self.get_map().npcs:
            npc.move_to_next_point()
        for sprite in self.get_group().sprites():
            if type(sprite) is not ItemSprite:
                if hasattr(sprite, "direction"):
                    if sprite.direction[0] * sprite.speed != 0 or sprite.direction[1] * sprite.speed != 0:
                        if random.choice([True, False]):
                            self.get_group().add(
                                Particle(
                                    sprite.position[0] + sprite.width / 2 -
                                        6 - sprite.direction[0] * 10,
                                    sprite.position[1] + sprite.height / 2 -
                                        sprite.direction[1] * 15,
                                    "dust"
                                )
                            )
