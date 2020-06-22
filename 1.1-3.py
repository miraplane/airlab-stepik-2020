import math

def calculate_cell_size(M, phi, h):
    return 2 * math.tan(phi/2) * h / M

def read_photo(K, M):
    photos = []
    for k in range(K):
        lines = []
        for m in range(M):
            lines.append(input())
        photos.append(lines)
    return photos

if __name__ == '__main__':
    M, N , phi, h = input().split(' ')
    M = int(M)
    N = int(N)
    phi = math.radians(float(phi.replace(',', '.')))
    h = float(h.replace(',', '.'))
    
    cell_size = calculate_cell_size(M, phi, h)
    
    K = int(input())
    photos = read_photo(K, M)
    
    control_lines = photos[0]
    l = M - 1
    count = math.inf
    for i in range(1, K):
        lines = photos[i]     
        for j in range(M):
            l = M - 1
            equels = True
            for m in reversed(range(j + 1)):
                if lines[m] != control_lines[l]:
                    equels = False
                    break
                l -= 1
            if equels:
                break
        if equels and l + 1 > 0:
            count = min(count, l + 1)
        control_lines = lines
        l = M - 1

    print(round(cell_size * K * count, 2))