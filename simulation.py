import pygame
import sys
import random
import math
import time

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
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
        self._disconnect_prob = random.uniform(0, 1)
        self._relationship_prob = random.uniform(0, 1)
        self._death_prob = random.uniform(0, 1)
        self._birth_prob = random.uniform(0, 1)
        self._neighbors = []
        self._friends = []
        self._gender = bool(random.getrandbits(1)) #1 is male, 0 is female
        self._partner = None
        self._color = WHITE

    def connect(self, other: "Node", nodes: list["Node"]) -> None:
        connect_color = RED if self.partner == other else WHITE

        if other in self._neighbors:
            pygame.draw.line(surface, connect_color, self._pos, other.pos, 1)
        else:
            avoid = self.find_obstructions(other, nodes)
            if len(avoid) == 0:
                pygame.draw.line(surface, connect_color, self._pos, other.pos, 1)
                return
                
            r = 15
            cartx_self = self._pos[0] - SCREEN_WIDTH/2
            carty_self = SCREEN_HEIGHT/2 - self._pos[1]
            cartx_other = other.pos[0] - SCREEN_WIDTH/2
            carty_other = SCREEN_HEIGHT/2 - other.pos[1]
            vertical = True if self._pos[0] == other.pos[0] else False
            x_intersects = []
            y_intersects = []
            if not vertical:
                for n in avoid:
                    cartx_avoid = n.pos[0] - SCREEN_WIDTH/2
                    carty_avoid = SCREEN_HEIGHT/2 - n.pos[1]

                    x_intersects += find_intersections([cartx_self, carty_self], [cartx_other, carty_other], [cartx_avoid, carty_avoid], r)
                if self._pos[0] < other.pos[0]:
                    #left to right
                    x_intersects.sort()
                else:
                    x_intersects.sort(reverse=True)

                m = (self._pos[1] - other.pos[1]) / (self._pos[0] - other.pos[0])     
                b = self._pos[1] - m*self._pos[0]
                y_intersects = [m*x+b for x in x_intersects]

            else:
                x_intersects = [avoid[0].pos[0] for _ in range(len(avoid)*2)]
                
                y_intersects += [n.pos[1]+r for n in avoid]
                y_intersects += [n.pos[1]-r for n in avoid]

                if self._pos[1] < other.pos[1]:
                    #top to bottom
                    y_intersects.sort()
                else:
                    y_intersects.sort(reverse=True)

            self.draw_around(other, avoid, x_intersects, y_intersects, r, connect_color)

    def draw_around(self, other: "Node", nodes: list["Node"], x_i: list[float], y_i: list[float], radius: int, color: list[int]) -> None:
        pygame.draw.line(surface, color, self.pos, (x_i[0], y_i[0]), 1)

        prev, curr = 1, 2
        while curr < len(x_i):
            pygame.draw.line(surface, color, (x_i[prev], y_i[prev]), (x_i[curr], y_i[curr]), 1)
            prev += 2
            curr += 2

        pygame.draw.line(surface, color, (x_i[prev], y_i[prev]), other.pos, 1)

        for n in nodes:
            pygame.draw.circle(surface, color, n.pos, radius, 1)

    def find_obstructions(self, other: "Node", nodes: list["Node"]) -> list["Node"]:
        obstructors = []
        if self._pos[0] == other.pos[0]:
            for n in nodes:
                if abs(n.pos[0] - other.pos[0]) < 15 and n != self and n != other:
                    if n.pos[1] > min(other.pos[1], self._pos[1]) and n.pos[1] < max(other.pos[1], self._pos[1]):
                        obstructors.append(n)
        else:
            m = (self._pos[1] - other.pos[1]) / (self._pos[0] - other._pos[0]) 
            b = self._pos[1] - self._pos[0] * m
            for n in nodes:
                if abs(n.pos[1] - (n.pos[0] * m + b)) < 15 and n != self and n != other:
                    if n.pos[0] > min(other.pos[0], self._pos[0]) and n.pos[0] < max(other.pos[0], self._pos[0]):
                        obstructors.append(n)

        return obstructors
    
    def find_adjacent(self, nodes: list["Node"]) -> list["Node"]:
        adj = []
        for n in nodes:
            if calculate_distance(self, n) < 150 and n != self:
                adj.append(n)
        return adj

    def possible_friends(self, nodes: list["Node"]) -> list["Node"]:
        poss_friends = []
        for n in self._neighbors:
            if n not in self._friends:
                poss_friends.append(n)
        for f in self._friends:
            for _f in f.friends:
                for __f in _f.friends:
                    if __f != _f and __f != f and __f not in self._friends:
                        poss_friends.append(__f)

        return poss_friends
    
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
    def disconnect_prob(self) -> float:
        return self._disconnect_prob

    @property
    def relationship_prob(self) -> float:
        return self._relationship_prob

    @property
    def gender(self) -> bool:
        return self._gender
    
    @property
    def color(self) -> list[int]:
        return self._color

    @color.setter
    def color(self, newcolor: list[int]) -> None:
        self._color = newcolor

    @property
    def death_prob(self) -> float:
        return self._death_prob
    
    @property
    def birth_prob(self) -> float:
        return self._birth_prob

def find_intersections(cart_self: list[float], cart_other: list[float], cart_avoid: list[float], r: int) -> list[float]: 
    m = (cart_self[1] - cart_other[1]) / (cart_self[0] - cart_other[0]) 
    b = cart_self[1] - cart_self[0] * m
    a = m**2+1
    B = 2*(m*b-m*cart_avoid[1]-cart_avoid[0])
    c = cart_avoid[1]**2 - r**2 + cart_avoid[0]**2 - 2*b*cart_avoid[1] + b**2
    x1 = (-B+math.sqrt(B**2-4*a*c))/(2*a)
    x2 = (-B-math.sqrt(B**2-4*a*c))/(2*a)
    x1 += SCREEN_WIDTH/2
    x2 += SCREEN_WIDTH/2

    return [x1, x2]

def calculate_distance(n1: Node, n2: Node) -> float:
    return sum([(n1.pos[i]-n2.pos[i])**2 for i in range(len(n1.pos))])**0.5

def update(node: Node, nodes: list[Node], spaces: [list[list[float]]]) -> (list[Node], list[list[float]]):
    rand_id = random.uniform(0, 1)
    if node.death_prob < rand_id*0.2:
        spaces.append(node.pos)
        for n in nodes:
            if node in n.friends:
                n.friends.remove(node)
            if node in n.neighbors:
                n.neighbors.remove(node)
            if node == n.partner:
                n.partner = None
            
        nodes.remove(node)

    if node.partner is not None and (node.birth_prob + node.partner.birth_prob)/2 < rand_id*0.4 and len(spaces) > 0:
        nodes.append(Node(s:=random.choice(spaces)))
        spaces.remove(s)
        for n in nodes:
            n.neighbors = n.find_adjacent(nodes)

    poss_friends = node.possible_friends(nodes)
    if node.connect_prob < rand_id and len(poss_friends) > 0:
        node.friends.append(random.choice(poss_friends))

    for f in node.friends:
        node.connect(f, nodes)
        if node.disconnect_prob < rand_id*0.8:
            node.friends.remove(f)
            node.partner = None
            f.partner = None
        elif (node.gender != f.gender) and (node.partner is None and f.partner is None) and (node.relationship_prob < rand_id):
            node.partner = f
            f.partner = node

    return nodes, spaces

def generate_nodes() -> list[Node]:
    nodes = []
    n = round(NUM_NODES**0.5)
    space = math.floor((SCREEN_WIDTH-OFFSET)/n)
    for i in range(n):
        for j in range(n):
            x, y = space * i + math.floor(OFFSET), space * j + math.floor(OFFSET)
            if i % 2 != 0:
                y += math.floor(OFFSET)
            
            nodes.append(Node([x, y]))
    for n in nodes:
        n.neighbors = n.find_adjacent(nodes)

    return nodes

def main() -> None:
    run = True
    clock = pygame.time.Clock()
    nodes = generate_nodes()
    spaces = []
    while run:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_q]:
            run = False

        surface.fill(BLACK)
        
        for node in nodes:
            nodes, spaces = update(node, nodes, spaces)
            node.draw_node()

        display.flip()
        time.sleep(1)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
