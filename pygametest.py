import pygame
import pygame.locals
import configparser


def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width / width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height / height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tile_table


class TileCache:
    """Load the tilesets lazily into global cache"""
    def __init__(self, width=32, height=None):
        self.width = width
        self.height = height or width
        self.cache = {}

    def __getitem__(self, filename):
        """Return a table of tiles, load it from disk if needed."""
        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width,
                                               self.height)
            self.cache[key] = tile_table
            return tile_table

    def _load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles."""
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width / width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height / height):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))
        return tile_table


class Level(object):
    def __init__(self, filename="level.map"):
        self.key = {}
        self.map = []
        parser = configparser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_tile(self, getx, gety):
        try:
            char = self.map[gety][getx]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, getx, gety, name):
        """Tell if the specified flag is set for position on the map."""
        value = self.get_tile(getx, gety).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_wall(self, getx, gety):
        """Is there a wall?"""
        return self.get_bool(getx, gety, 'wall')

    def is_blocking(self, getx, gety):
        """Is this place blocking movement?"""
        if not 0 <= getx < self.width or not 0 <= gety < self.height:
            return True
        return self.get_bool(getx, gety, 'block')

    def render(self):
        wall = self.is_wall
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width * MAP_TILE_WIDTH, self.height * MAP_TILE_HEIGHT))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    # Draw different tiles depending on neighbourhood
                    if not wall(map_x, map_y + 1):
                        if wall(map_x + 1, map_y) and wall(map_x - 1, map_y):
                            tile = 1, 2
                        elif wall(map_x + 1, map_y):
                            tile = 0, 2
                        elif wall(map_x - 1, map_y):
                            tile = 2, 2
                        else:
                            tile = 3, 2
                    else:
                        if wall(map_x + 1, map_y + 1) and wall(map_x - 1, map_y + 1):
                            tile = 1, 1
                        elif wall(map_x + 1, map_y + 1):
                            tile = 0, 1
                        elif wall(map_x - 1, map_y + 1):
                            tile = 2, 1
                        else:
                            tile = 3, 1
                    # Add overlays if the wall may be obscuring something
                    if not wall(map_x, map_y - 1):
                        if wall(map_x + 1, map_y) and wall(map_x - 1, map_y):
                            over = 1, 0
                        elif wall(map_x + 1, map_y):
                            over = 0, 0
                        elif wall(map_x - 1, map_y):
                            over = 2, 0
                        else:
                            over = 3, 0
                        overlays[(map_x, map_y)] = tiles[over[0]][over[1]]
                else:
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 3
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x * MAP_TILE_WIDTH, map_y * MAP_TILE_HEIGHT))
        return image, overlays


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((424, 320))

    MAP_TILE_WIDTH = 24
    MAP_TILE_HEIGHT = 16
    MAP_CACHE = {
        'ground.png': load_tile_table('ground.png', MAP_TILE_WIDTH,
                                      MAP_TILE_HEIGHT),
    }

    level = Level()
    level.load_file('level.map')

    clock = pygame.time.Clock()

    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    pygame.display.flip()
    game_over = False
    while not game_over:
        # XXX draw all the objects here
        overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
