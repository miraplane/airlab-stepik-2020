import math

if __name__ == '__main__':
    d, w1, t1, w2, t2, w3, t3 = map(float, input().strip().split())
    cos30 = math.sqrt(3) / 2
    r = d / 2
    v1 = w1 * r
    v2 = w2 * r
    v3 = w3 * r
    x = v1 * t1 - t2 * v2 / 2 - t3 * v3 / 2
    y = v3 * cos30 * t3 - v2 * cos30 * t2
    print (int(x / 2), int(y / 2))