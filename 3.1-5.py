dir_vector = [(0, -1), (1, 0), (0, 1), (-1, 0)]
dir_id = ['U', 'R', 'D', 'L']

class Section:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        
        self.up = None
        self.right = None
        self.down = None
        self.left = None
        
        self.set_up = False
        self.set_right = False
        self.set_down = False
        self.set_left = False
    
    def add_relation(self, index, neighbor):
        relation = dir_id[index]
        if relation == 'U':
            self.up = neighbor
            self.set_up = True
        if relation == 'R':
            self.right = neighbor
            self.set_right = True
        if relation == 'D':
            self.down = neighbor
            self.set_down = True
        if relation == 'L':
            self.left = neighbor
            self.set_left = True
    
    def delete_relation(self, index):
        relation = dir_id[index]
        if relation == 'U':
            self.set_up = True
        if relation == 'R':
            self.set_right = True
        if relation == 'D':
            self.set_down = True
        if relation == 'L':
            self.set_left = True
    
    def full_set(self):
        return self.set_up and self.set_right and self.set_down and self.set_left
    
    def get_no_set_neighbors(self):
        neighbors = []
        if not self.set_up:
            dx, dy = dir_vector[0]
            neighbors.append((self.x + dx, self.y + dy))
        if not self.set_right:
            dx, dy = dir_vector[1]
            neighbors.append((self.x + dx, self.y + dy))
        if not self.set_down:
            dx, dy = dir_vector[2]
            neighbors.append((self.x + dx, self.y + dy))
        if not self.set_left:
            dx, dy = dir_vector[3]
            neighbors.append((self.x + dx, self.y + dy))
        return neighbors
            
    
    def get_neighbors(self):
        return [self.up, self.right, self.down, self.left]
    
    def get_next(self, direction):
        x, y = self.get_up_section(direction)
        neighbors = self.get_neighbors()
        
        for neighbor in neighbors:
            if neighbor and neighbor.x == x and neighbor.y == y:
                return neighbor
    
    def get_left_section(self, direction):
        dx, dy = dir_vector[(direction - 1) % 4]
        return self.x + dx, self.y + dy
    
    def get_up_section(self, direction):
        dx, dy = dir_vector[direction]
        return self.x + dx, self.y + dy
    
    def get_right_section(self, direction):
        dx, dy = dir_vector[(direction + 1) % 4]
        return self.x + dx, self.y + dy
    
    def section_set(self, index):
        relation = dir_id[index]
        if relation == 'U':
            return self.set_left, self.set_up, self.set_right
        if relation == 'R':
            return self.set_up, self.set_right, self.set_down
        if relation == 'D':
            return self.set_right, self.set_down, self.set_left
        if relation == 'L':
            return self.set_down, self.set_left, self.set_up

class Robot:
    def __init__(self, section, direction):
        self.section = section
        self.direction = dir_id.index(direction)
        
        self.command = {'F': self.go, 'L': self.rotate_left, 'R': self.rotate_right}
        self.visit = 1

    def rotate_left(self):
        self.direction -= 1
        self.direction %= 4
        
    def rotate_right(self):
        self.direction += 1
        self.direction %= 4
    
    def go(self):
        self.section = self.section.get_next(self.direction)
        self.visit += 1
    
    def action(self, movment):
        self.command[movment]()


class Labyrinth:
    def __init__(self, k, m):
        self.k = k
        self.m = m
        self.robots = []
        self.map = []
        self.start = None
    
    def init_map(self):
        for i in range(self.k):
            column = []
            for j in range(self.m):
                section = Section(i, j)
                if j == 0:
                    section.delete_relation(0)
                if i == self.k - 1:
                    section.delete_relation(1)
                if j == self.m - 1:
                    section.delete_relation(2)
                if i == 0:
                    section.delete_relation(3)
                column.append(section)
            self.map.append(column)
    
    def add_robot(self, x, y, d):
        if len(self.robots) == 0:
            self.start = self.map[x][y]
        self.robots.append(Robot(self.map[x][y], d))
    
    def add_sections_relations(self, first, second, direction):
        first.add_relation(direction, second)
        second.add_relation((direction + 2) % 4, first)
    
    def delete_sections_relations(self, first, second, direction):
        first.delete_relation(direction)
        second.delete_relation((direction + 2) % 4)
    
    def robot_action(self, n, movment, left, up, right):
        robot = self.robots[n]
        section = robot.section
        if movment == 'F':
            x, y = section.get_up_section(robot.direction)
            up_section = self.map[x][y]
            self.add_sections_relations(section, up_section, robot.direction)
        robot.action(movment)
        section = robot.section
        set_left, set_up,set_right = section.section_set(robot.direction)
        
        if not set_left:
            x, y = section.get_left_section(robot.direction)
            left_section = self.map[x][y]
            if left == 0:
                self.add_sections_relations(section, left_section, (robot.direction - 1) % 4)
            else:
                self.delete_sections_relations(section, left_section, (robot.direction - 1) % 4)
        
        if not set_up:
            x, y = section.get_up_section(robot.direction)
            up_section = self.map[x][y]
            if up == 0:
                self.add_sections_relations(section, up_section, robot.direction)
            else:
                self.delete_sections_relations(section, up_section, robot.direction)
        
        if not set_right:
            x, y = section.get_right_section(robot.direction)
            right_section = self.map[x][y]
            if right == 0:
                self.add_sections_relations(section, right_section, (robot.direction + 1) % 4)
            else:
                self.delete_sections_relations(section, right_section, (robot.direction + 1) % 4)
    
    def get_alive(self):
        count = 0
        queue = [self.start]
        visited = []
        not_full = []
        while len(queue) != 0:
            count += 1
            section = queue.pop(0)
            visited.append(section)
            if not section.full_set():
                not_full.append(section)
            neighbors = section.get_neighbors()
            
            for neighbor in neighbors:
                if neighbor and not neighbor in visited and not neighbor in queue:
                    queue.append(neighbor)
        
        for section in not_full:
            no_set = section.get_no_set_neighbors()
            for x, y in no_set:
                if not self.map[x][y] in visited:
                    return self.robots[0].visit
            
        return count
            

if __name__ == '__main__':
    N, K, M, I = map(int, input().split())
    labyrinth = Labyrinth(K, M)
    labyrinth.init_map()
    
    for i in range(N):
        x, y, d = input().split()
        labyrinth.add_robot(int(x), int(y), d)
    
    for n in range(N):
        for i in range(I):
            movment, left, up, right = input().split()
            labyrinth.robot_action(n, movment, int(left), int(up), int(right))
    print(labyrinth.get_alive())