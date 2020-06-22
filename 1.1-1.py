import math
angle = math.radians(270)
x = 0
y = 0
phi = 0
coords = [(0, 0)]

def сross_product(a_x, a_y, b_x, b_y):
    return a_x * b_y - a_y * b_x

def make_vector(a_x, a_y, b_x, b_y):
    return b_x - a_x, b_y - a_y

def calculate_intersection_point(a_x, a_y, b_x, b_y, z1, z2):
    p_x = a_x + (b_x - a_x) * math.fabs(z1) / math.fabs(z2-z1)
    p_y = a_y + (b_y - a_y) * math.fabs(z1) / math.fabs(z2-z1)
    
    return p_x, p_y

def intersection(a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y):
    ab_x, ab_y = make_vector(a_x, a_y, b_x, b_y)
    ac_x, ac_y = make_vector(a_x, a_y, c_x, c_y)
    ad_x, ad_y = make_vector(a_x, a_y, d_x, d_y)
    z1 = сross_product(ab_x, ab_y, ac_x, ac_y)
    z2 = сross_product(ab_x, ab_y, ad_x, ad_y)
    
    cd_x, cd_y = make_vector(c_x, c_y, d_x, d_y)
    ca_x, ca_y = make_vector(c_x, c_y, a_x, a_y)
    cb_x, cb_y = make_vector(c_x, c_y, b_x, b_y)
    z3 = сross_product(cd_x, cd_y, ca_x, ca_y)
    z4 = сross_product(cd_x, cd_y, cb_x, cb_y)
    
    if z1 * z2 <= 0 and z3 * z4 <= 0:
        if z1 == 0 and z2 == 0:
            return None, None
        return calculate_intersection_point(c_x, c_y, d_x, d_y, z1, z2)
    return None, None

if __name__ == '__main__':
    N, t = input().split(' ')
    N = int(N)
    t = float(t.replace(',', '.'))
    p_x = p_y = None
    
    for i in range(N):
        v, w = input().split(' ')
        v = float(v.replace(',', '.'))
        w = float(w.replace(',', '.'))
        l_x = x
        l_y = y
        if w != 0:            
            phi += w * t
            if v == 0:
                continue
            r = v / w
            l = v * t
            a = l / r
            d = 2 * r * math.sin(a / 2)
        else:
            d = v * t
            
        x += d * math.cos(phi)
        y += d * math.sin(phi)
        
        lc_x, lc_y = coords[0]
        p_x = p_y = None
        for j in range(1, len(coords) - 1):
            c_x, c_y = coords[j]         
            p_x, p_y = intersection(l_x, l_y, x, y, lc_x, lc_y, c_x, c_y)
            if p_x and p_y:
                break
            lc_x = c_x
            lc_y = c_y

        coords.append((x, y))
        if p_x and p_y:
            break
            
    print(round(math.sqrt(p_x * p_x + p_y * p_y)))