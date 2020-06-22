import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.a = self.start.y - self.end.y
        self.b = self.end.x - self.start.x
        self.c = self.start.x * self.end.y - self.end.x * self.start.y
    
    def get_x(self, y):
        if self.a == 0:
            return self.start.y
        return round((-self.c - self.b * y) / self.a)
    
    def get_y(self, x):
        if self.b == 0:
            return self.start.x
        return round((-self.c - self.a * x) / self.b)
    
    def get_cells(self):
        cell = []
        dx = math.fabs(self.end.x - self.start.x)
        dy = math.fabs(self.end.y - self.start.y)
        
        if dx > dy:
            min_x = min(self.end.x, self.start.x)
            max_x = max(self.end.x, self.start.x)
            for x in range(min_x, max_x + 1):
                cell.append(Point(x, self.get_y(x)))
        else:
            min_y = min(self.end.y, self.start.y)
            max_y = max(self.end.y, self.start.y)
            for y in range(min_y, max_y + 1):
                cell.append(Point(self.get_x(y), y))
        return cell


class Circle:
    def __init__(self, id, x, y, r):
        self.id = id
        self.center = Point(x, y)
        self.r = r
    
    def get_cells(self):
        cells = []
        for d1 in range(-self.r, self.r + 1):
            for d2 in range(-self.r + 1, self.r):
                cells.append(Point(self.center.x + d1, self.center.y + d2))
                cells.append(Point(self.center.x + d2, self.center.y + d1))
        return cells
    
    def get_fill(self):
        return self.id + 1;
        

class Obstacle:
    def __init__(self, vertex_count):
        self.count = vertex_count
        self.vertex = []
    
    def add_vertex(self, x, y):
        self.vertex.append(Point(x, y))
    
    def get_cells(self):
        cells = []
        start = self.vertex[self.count - 1]
        for i in range(self.count):
            end = self.vertex[i]
            vector = Vector(start, end)
            cells += vector.get_cells()
            start = end
        return cells
    
    def get_fill(self):
        return -1;


class Map:
    def __init__(self, k, l):
        self.k = k
        self.l = l
        self.map = []
        self.circles = []
        self.obstacles = []
        self.init_map(k, l)    
    
    def in_map(self, point):
        return 0 <= point.x <= self.k - 1 and 0 <= point.y <= self.l - 1
    
    def init_map(self, k, l):
        for i in range(k):
            line = []
            for j in range(l):
                line.append(0)
            self.map.append(line)
    
    def add_circle(self, circle):
        self.circles.append(circle)
        self.update_map(circle)
    
    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
        self.update_map(obstacle)
    
    def update_map(self, map_object):
        cells = map_object.get_cells()
        fill = map_object.get_fill()
        for cell in cells:
            if self.in_map(cell):
                self.map[cell.x][cell.y] = fill
        
    def check_point(self, point, visited):
        no_border = (1 <= point.x <= self.k - 2) and (1 <= point.y <= self.l - 2)
        if not no_border: 
            return False
        
        no_visited = True
        for last in visited:
            if last.x == point.x and last.y == point.y:
                no_visited = False
        if not no_visited: 
            return False
        
        no_obstacle = True        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                part = Point(point.x + dx, point.y + dy)
                if self.map[part.x][part.y] == -1:
                    no_obstacle = False
        return no_obstacle
    
    def cross_circle(self, end, parent):
        circle = []
        while end != -1:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    point = Point(end.x + dx, end.y + dy)
                    if not self.in_map(point):
                        continue
                    fill = self.map[point.x][point.y]
                    if not fill - 1 in circle and fill != 0:
                        circle.append(fill - 1)
            end = parent[(end.x, end.y)]
        circle.reverse()

        return circle
    
    def find_way(self, start, end):
        visited = []
        parent = {(start.x, start.y): -1}
        queue = [start]
        while(len(queue) != 0):
            current = queue.pop(0)
            visited.append(current)
            if (current.x == end.x and current.y == end.y):
                break

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    point = Point(current.x + dx, current.y + dy)
                    if self.check_point(point, visited):
                        if not (point.x, point.y) in parent.keys():
                            queue.append(point)
                            parent[(point.x, point.y)] = current
        
        if not (end.x, end.y) in parent.keys():
            return -1
        return " ".join(str(c) for c in self.cross_circle(end, parent))
    

if __name__ == '__main__':
    K, L = map(int, input().split(' '))
    my_map = Map(K, L)
    
    start = Point(*map(int, input().split(' ')))
    finish = Point(*map(int, input().split(' ')))
    
    N, M = map(int, input().split(' '))
    for i in range(N):
        my_map.add_circle(Circle(*map(int, input().split(' '))))

    for i in range(M):
        O, P = map(int, input().split(' '))
        obstacle = Obstacle(P)
        for j in range(P):
            obstacle.add_vertex(*map(int, input().strip().split(' ')))
        my_map.add_obstacle(obstacle)
    
    print(my_map.find_way(start, finish))