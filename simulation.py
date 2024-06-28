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
        # This is fricked - need to stop drawing lines between self and other every iteration of for loop
        self._friends.append(other)
        if other in self._neighbors:
            pygame.draw.line(surface, WHITE, self._pos, other.pos, 1)
        else:
            avoid = self.find_obstructions(other, nodes)
            #assert len(avoid) > 0, "no obstructions"
            if len(avoid) == 0:
                pygame.draw.line(surface, WHITE, self._pos, other.pos, 1)
            r = 15
            cartx_self = self._pos[0] - SCREEN_WIDTH/2
            carty_self = SCREEN_HEIGHT/2 - self._pos[1]
            
            cartx_other = other.pos[0] - SCREEN_WIDTH/2
            carty_other = SCREEN_HEIGHT/2 - other.pos[1]

            m = (carty_self - carty_other) / (cartx_self - cartx_other) 
            b = carty_self - cartx_self * m
            
            prev = self
            for n in avoid:
                cartx_avoid = n.pos[0] - SCREEN_WIDTH/2
                carty_avoid = SCREEN_HEIGHT/2 - n.pos[1]

                a = m**2+1
                B = 2*(m*b-m*carty_avoid-cartx_avoid)
                c = carty_avoid**2 - r**2 + cartx_avoid**2 - 2*b*carty_avoid + b**2
                
                x1 = (-B+math.sqrt(B**2-4*a*c))/(2*a)
                x2 = (-B-math.sqrt(B**2-4*a*c))/(2*a)

                x1 += SCREEN_WIDTH/2
                x2 += SCREEN_WIDTH/2
                    
                
                m = (self._pos[1] - other.pos[1]) / (self._pos[0] - other.pos[0]) 
                b = self._pos[1] - m*self._pos[0]

                if self._pos[0] < other.pos[0]:
                    self.draw_around(other, min(x1, x2), max(x1, x2), min(x1, x2)*m+b, max(x1, x2)*m+b, n, r)
                elif self._pos[0] > other.pos[0]:
                    self.draw_around(other, max(x1, x2), min(x1, x2), max(x1, x2)*m+b, min(x1, x2)*m+b, n, r)
                else:
                    if self._pos[1] > other.pos[1]:
                        self.draw_around(other, (max(y1, y2)-b)/m, (min(y1, y2)-b)/m, max(y1, y2), min(y1, y2), n, r)
                    elif self._pos[1] < other.pos[1]:
                        self.draw_around(other, (min(y1, y2)-b)/m, (max(y1, y2)-b)/m, min(y1, y2), max(y1, y2), n, r)

    def draw_around(self, other: "Node", x1: float, x2: float, y1: float, y2: float, n: "Node", radius: int) -> None:
        pygame.draw.line(surface, WHITE, self._pos, (x1, y1), 1)
        pygame.draw.circle(surface, WHITE, n.pos, radius, 1)
        pygame.draw.line(surface, WHITE, (x2, y2), other.pos, 1)
                    
    
    def find_obstructions(self, other: "Node", nodes: list["Node"]) -> list["Node"]:
        obstructors = []
        m = (self._pos[1] - other.pos[1]) / (self._pos[0] - other._pos[0]) 
        b = self._pos[1] - self._pos[0] * m
        #pygame.draw.line(surface, WHITE, (self._pos[0],m*self._pos[0]+b), (other.pos[0],m*other.pos[0]+b),1)
        for n in nodes:
            if abs(n.pos[1] - (n.pos[0] * m + b)) < 15 and n != self and n != other:
                if n.pos[0] > min(other.pos[0], self._pos[0]) and n.pos[0] < max(other.pos[0], self._pos[0]):
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
                nodes[15]._color = (0, 255, 0)
                node.connect(nodes[15], nodes)
            
            i += 1

        display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
