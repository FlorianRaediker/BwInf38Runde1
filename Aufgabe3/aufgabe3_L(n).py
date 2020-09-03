import aufgabe3

while True:
    while True:
        try:
            n = int(input("Bitte Wert für n eingeben: "))
            if n < 1:
                raise ValueError
        except ValueError:
            print("Das ist keine Ganzzahl größer als 0. ")
        else:
            break
    print(f"L({n}) = {len(aufgabe3.create_beaver_distributions(n)[0]) - 1}")
