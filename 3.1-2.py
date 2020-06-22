class Section:
    def __init__(self, s_id):
        self.s_id = s_id
        self.up = None
        self.right = None
        self.down = None
        self.left = None
    
    def __repr__(self):
        return "id - {0}, relation: {1} {2} {3} {4}".format(self.s_id, self.up, self.right, self.down, self.left)
    
    def add_relation(self, relation, neighbor):
        if relation == 0:
            self.up = neighbor
        if relation == 1:
            self.right = neighbor
        if relation == 2:
            self.down = neighbor
        if relation == 3:
            self.left = neighbor
    
    def get_neighbor(self, direction):
        if direction == 0:
            return self.left, self.up, self.right
        if direction == 1:
            return self.up, self.right, self.down
        if direction == 2:
            return self.right, self.down, self.left,
        if direction == 3:
            return self.down, self.left, self.up


class Robot:
    def __init__(self):
        self.section_id = None
        self.direction = None
        self.sections = {}
        self.alive = set()
        self.move = False
    
    def add_sections(self, M):
        for i in range(1, M + 1):
            self.sections[i] = Section(i)
    
    def add_sections_relations(self, first, second, direction):
        self.sections[first].add_relation(direction, second)
        self.sections[second].add_relation((direction + 2) % 4, first)
    
    def add_start_section(self, section, direction):
        self.section_id = section
        self.direction = direction
        self.alive.add(section)
    
    def get_destroyed_sections(self):
        sections = set(self.sections.keys())
        destroyed = list(sections.difference(self.alive))
        destroyed.sort()
        return " ".join(str(s) for s in destroyed)
    
    def check_alive_neighbor(self, c_left, c_up, c_right):
        section = self.sections[self.section_id]
        left, up, right = section.get_neighbor(self.direction)
        if self.move:
            self.section_id = up
            section = self.sections[self.section_id]
            left, up, right = section.get_neighbor(self.direction)
        
        if left and c_left == 1:
            self.alive.add(left)
        if up and c_up == 1:
            self.alive.add(up)
        if right and c_right == 1:
            self.alive.add(right)
        
        self.move = True
    
    def rotate_left(self):
        if self.direction == 0:
            self.direction = 3
        else:
            self.direction -= 1
        
    def rotate_right(self):
        self.direction += 1
        self.direction %= 4
    
    def action(self, left, up, right):
        if left == 2:
            self.rotate_left()
            self.move = False
        elif left == 3:
            self.rotate_right()
            self.move = False
        else:
            self.check_alive_neighbor(left, up, right)
            

if __name__ == '__main__':
    M, N, K = map(int, input().split())
    robot = Robot()
    robot.add_sections(M)
    
    for i in range(N):
        robot.add_sections_relations(*map(int, input().split()))
        
    robot.add_start_section(*map(int, input().split()))
    
    for i in range(K):
        robot.action(*map(int, input().split()))
    
    print(robot.get_destroyed_sections())