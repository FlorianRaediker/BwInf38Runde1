import aufgabe3

while True:
    while True:
        try:
            dist = eval(input("Bitte eine Biberverteilung eingeben: "))
        except Exception:
            dist = None
        if type(dist) == tuple and len(dist) == 3 and all(type(x) == int for x in dist):
            break
        print("Das ist keine Biberverteilung. ")
    print(f"LLL ({dist[0]},{dist[1]},{dist[2]}) = {aufgabe3.get_LLL(dist)}")
    print(f"Telepaartien für ({dist[0]},{dist[1]},{dist[2]}): {aufgabe3.get_telepaartien(dist)}")
