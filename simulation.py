import pygame
import sys
import random
import math

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
MIN_SEPERATION = 20
NUM_NODES = 54
OFFSET = 50

pygame.init()
display = pygame.display
surface = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption("Social Network Sim")

class Node:
    def __init__(self, pos: list[int]) -> None:
        self._pos = pos
        self._connect_prob = random.uniform(0, 1)
        self._meetup_prob = random.uniform(0, 1)
        self._neighbors = []
        self._friends = []
        self._gender = bool(random.getrandbits(1)) #1 is male, 0 is female
        self._partner = None
        self._color = WHITE

    def draw_node(self) -> None:
        pygame.draw.circle(surface, self._color, self._pos, 5)
    
    @property
    def pos(self) -> list[int]:
        return self._pos

    @pos.setter
    def pos(self, newpos: list[int]) -> None:
        self._pos = newpos

    @property
    def neighbors(self) -> list["Node"]:
        return self._neighbors

    @neighbors.setter
    def neighbors(self, newneighbors: list["Node"]) -> None:
        self._neighbors = newneighbors

    @property
    def friends(self) -> list["Node"]:
        return self._friends

    @friends.setter
    def friends(self, newfriends: list["Node"]) -> None:
        self._friends = newfriends

    @property
    def partner(self) -> "Node":
        return self._partner

    @partner.setter
    def partner(self, newpartner: "Node") -> None:
        self._partner = newpartner

    @property
    def connect_prob(self) -> float:
        return self._connect_prob

    @property
    def meetup_prob(self) -> float:
        return self._meetup_prob

    @property
    def gender(self) -> bool:
        return self._gender
    
    @property
    def color(self) -> list[int]:
        return self._color

    @color.setter
    def color(self, newcolor: list[int]) -> None:
        self._color = newcolor

def calculate_distance(n1: list[int], n2: list[int]) -> float:
    return sum([(n1[i]-n2[i])**2 for i in range(len(n1))])**0.5

def update() -> None:
    pass


def generate_nodes() -> list[Node]:
    nodes = []
    n = round(NUM_NODES**0.5)
    space = math.floor((SCREEN_WIDTH-OFFSET)/n) # spacing for nodes
    for i in range(n):
        for j in range(n):
            x, y = space * i + math.floor(OFFSET), space * j + math.floor(OFFSET)
            if i % 2 != 0:
                y += math.floor(OFFSET)
            
            nodes.append(Node([x, y]))
            
    return nodes


def main() -> None:
    run = True
    clock = pygame.time.Clock()
    nodes = generate_nodes()

    while run:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_q]:
            run = False

        surface.fill(BLACK)
        
        # update()
        for node in nodes:
            node.draw_node()

        display.flip()


    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()
