from dataclasses import dataclass
import pygame, pytmx, pyscroll
from pygame import mixer
from entity import NPC, Item
import particles
from settings import *


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
    items: list[Item]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"


        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon"),
            Portal(from_world="world", origin_point="switch_beach", target_world="beach", teleport_point="spawn_beach"),
            Portal(from_world="world", origin_point="switch_snowy_forest", target_world="snowy_forest", teleport_point="spawn_snowy_forest"),
            Portal(from_world="world", origin_point="switch_autumn_forest", target_world="autumn_forest", teleport_point="spawn_autumn_forest")
        ], npcs=[
            NPC("liam", nb_points=4, dialog=['Hi, how are you ?', "I feel good.", 'Good luck !']),
            NPC("gunvald", nb_points=8, dialog=['...'])
        ])
        self.register_map("anoying_room", portals=[
            Portal(from_world="anoying_room", origin_point="exit_anoying_room", target_world="world", teleport_point="player")
        ], npcs=[
            NPC("wassa", nb_points=4, dialog=["(o_o)", "Is this dog eating un skeleton ?"], speed=16, has_a_portrait=True)
        ])
        self.register_map("beach", portals=[
            Portal(from_world="beach", origin_point="switch_world", target_world="world", teleport_point="spawn_from_beach"),
            Portal(from_world="beach", origin_point="enter_house5", target_world="house5", teleport_point="spawn_house")
        ], npcs=[
            NPC("faster", nb_points=6, dialog=["Want to run faster ?", "Hold Shift while moving to go fast!"], speed=4),
            NPC("umbra", nb_points=4, dialog=["I'm not cheating !"], speed=16, has_a_portrait=True)
        ])
        self.register_map("house5", portals=[
            Portal(from_world="house5", origin_point="exit_house", target_world="beach", teleport_point="enter_house_exit5"),
        ])
        self.register_map("snowy_forest", portals=[
            Portal(from_world="snowy_forest", origin_point="switch_world", target_world="world", teleport_point="spawn_from_snowy_forest"),
            Portal(from_world="snowy_forest", origin_point="enter_house3", target_world="house3", teleport_point="spawn_house")
        ], npcs=[
            NPC("allein", nb_points=6, dialog=["What's up ?", "Here, I don't see many people.", 'I\'m Allein. Welcome !'], speed=0.75)
        ])
        self.register_map("autumn_forest", portals=[
            Portal(from_world="autumn_forest", origin_point="switch_world", target_world="world", teleport_point="spawn_from_autumn_forest")
        ], npcs=[
            NPC("helma", nb_points=8, dialog=["Hello !", "My name is Wilhelmina. But you can call me Helma !", 'Bye !']),
            NPC("dustan", nb_points=4, dialog=["...", "What are you looking at ?"])
        ])
        self.register_map("house3", portals=[
            Portal(from_world="house3", origin_point="exit_house", target_world="snowy_forest", teleport_point="enter_house_exit3"),
        ])


        self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit"),
            Portal(from_world="house", origin_point="cave_enter", target_world="cave", teleport_point="spawn_cave")
        ])
        self.register_map("cave", portals=[
            Portal(from_world="cave", origin_point="exit_cave", target_world="house", teleport_point="cave_exit"),
            Portal(from_world="cave", origin_point="enter_underground", target_world="underground", teleport_point="spawn_underground")
        ], npcs=[
            NPC("aiko", nb_points=5, dialog=["Hello ! My name is Aiko.", "It's a weird place, isn't it ? But I stay here.", "Don't forget this sentence: Bread is pain."])
        ])
        self.register_map("underground", portals=[
            Portal(from_world="underground", origin_point="exit_underground", target_world="cave", teleport_point="spawn_from_underground")
        ], npcs=[
            NPC("john_doe", nb_points=4, dialog=["Why so many sinks?"])
        ])
        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit2"),
            Portal(from_world="house2", origin_point="second_floor", target_world="stage2", teleport_point="spawn_floor")
        ], npcs=[
            NPC("cooper", nb_points=2, dialog=["Hi,I'mYourNewGardener,MyNameIsCooper!", 'Oh, sorry, I\'m stessed...', "Hello ,  I  am  your  new  gardener ,  my  name  is  Cooper ."])
        ])
        self.register_map("stage2", portals=[
            Portal(from_world="stage2", origin_point="first_floor", target_world="house2", teleport_point="bottom_stairs")
        ])

        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="world", teleport_point="spawn_from_dungeon")
        ], npcs=[
            NPC("boss", nb_points=6, dialog=["I am alone,", 'like a boss.', "I'm dangerous,", 'like a boss.', 'I am scary,', 'like a boss.'])
        ])

        self.teleport_player("player")
        self.teleport_npcs()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite, sprite.dialog)

    def check_collisions(self):
        # portals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = sprite.stats["speed"]

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

        # items
        for sprite in self.get_group().sprites():
            if type(sprite) is Item:
                # get the distance and the direction
                distance = sprite.get_player_distance_direction(self.player)[0]
                direction = sprite.get_player_distance_direction(self.player)[1]

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
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = ZOOM

        # set lists to store rectangles
        walls = []
        items = []

        for obj in tmx_data.objects: # obj = object
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "item":
                items.append(Item("item", obj.x, obj.y, obj.name))

        # draw the layer group and add elements to group
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)
        for npc in npcs: group.add(npc)
        for item in items: group.add(item)

        # create a new object Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, items)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

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
            npc.move()
