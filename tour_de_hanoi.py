def hanoi(n, from_rod, to_rod, aux_rod, count=0):
    if n == 1:
        count += 1
        print('(' + str(count) +')', "Disque 1 :", from_rod, "=>", to_rod)
        return count
    count = hanoi(n-1, from_rod, aux_rod, to_rod, count)
    count += 1
    print('(' + str(count) +')', "Disque", n, ":", from_rod, "=>", to_rod)
    count = hanoi(n-1, aux_rod, to_rod, from_rod, count)
    return count

n = 3
count = hanoi(n, 'A', 'C', 'B')
print("---------------------------------")
print("Nombre total de déplacements :", count)
print("---------------------------------")
