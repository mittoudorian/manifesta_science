def hanoi(n, d1, d2, d3, count=0):
    if n == 1:
        count += 1
        print('(' + str(count) +')', "Disque 1 :", d1, "=>", d2)
        return count
    count = hanoi(n-1, d1, d3, d2, count)
    count += 1
    print('(' + str(count) +')', "Disque", n, ":", d1, "=>", d2)
    count = hanoi(n-1, d3, d2, d1, count)
    return count

def print_deplacement():
    n = 3
    count = hanoi(n, 'A', 'C', 'B')
    print("---------------------------------")
    print("Nombre total de déplacements :", count)
    print("---------------------------------")
