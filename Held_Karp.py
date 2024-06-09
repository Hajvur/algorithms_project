from itertools import combinations


def held_karp(distance_matrix):
    n = len(distance_matrix)
    
    G = {}
    
    for k in range(1,n):
        G[(1 << k,k)] = (distance_matrix[0][k],0)
    
    for s in range(2,n):
        for S in combinations(range(1,n),s):
            #ustawiamy bity z danej kombinacji jako sciezka, ktora przeszlismy np 1001 oznacza ze bylismy w punkcie 1 i w 4 (liczac od 1)
            bity = 0
            for bit in S:
                #print(f"bit = {bin(bit)[2:]}")
                bity |= 1 << bit
                #print(f" bity = {bin(bity)[2:]}")
            for k in S:
                poprzednia_permutacja = bity & ~ (1<<k)
                
                result = []
                for m in S:
                    if m == 0 or m ==k:#jeżeli m bedzie "dworcem głownym" albo po przekatna macierzy to skipuje bo byloby 0
                        continue
                    result.append((G[(poprzednia_permutacja,m)][0] + distance_matrix[m][k],m))
                G[(bity,k)] = min(result)

                
    bity = (2**n -1) -1
    
    result = []
    for k in range(1, n):
        result.append((G[(bity, k)][0] + distance_matrix[k][0], k))
        #print(f"curr res = {result}")
    min_dist, parent = min(result)
    
    path = []
    
    for j in range(n-1):
        path.append(parent)
        new_bits = bity & ~(1 << parent)
        holder, parent = G[(bity, parent)]
        bity = new_bits
    
    path.append(0)
    
    print(f"path = {list(reversed(path))}")
    print(f"min dist  = {min_dist}")
                

                
            
            