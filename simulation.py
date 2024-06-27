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

    def connect(self, other: "Node", nodes: list["Node"]) -> None:
        self._friends.append(other)
        if other in self._neighbors:
            pygame.draw.line(surface, WHITE, self._pos, other.pos, 1)
        else:
            avoid = self.find_obstructions(other, nodes)
            if self._pos[1] < other.pos[1]:
                # lower
                print(len(avoid))
                for n in avoid:
                    pygame.draw.line(surface, WHITE, (self._pos), (n.pos[0]-10, n.pos[1]+10), 1)
                    

            elif self._pos[1] > other.pos[1]:
                # higher
                pass


    
    def find_obstructions(self, other: "Node", nodes: list["Node"]) -> list["Node"]:
        obstructors = []
        m = (self._pos[1] - other.pos[1]) / (self._pos[0] - other._pos[0]) 
        b = self._pos[1] - self._pos[0] * m
        pygame.draw.line(surface, WHITE, (self._pos[0],m*self._pos[0]+b), (other.pos[0],m*other.pos[0]+b),1)
        for n in nodes:
            if abs(n.pos[1] - (n.pos[0] * m + b)) < 20 and calculate_distance(self, n) < calculate_distance(self, other) and n != self and n != other:
                obstructors.append(n)

        return obstructors


    """
    pygame.draw.arc(surface, WHITE, (200, 200, 100, 20), 0, math.pi, 1)
    pygame.draw.circle(surface, WHITE, (200, 215), 2)
    pygame.draw.circle(surface, WHITE, (300, 215), 2)
    """
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
    return sum([(n1.pos[i]-n2.pos[i])**2 for i in range(len(n1.pos))])**0.5

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
        i = 0
        for node in nodes:
            node.draw_node()
            if i == 2:
                node._color = (255, 0, 0)
                nodes[17]._color = (0, 255, 0)
                node.connect(nodes[17], nodes)
            
            i += 1

        display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
