import sys
import matplotlib.pyplot as plt
from graph import Graph, generate_hamiltonian_graph, generate_non_hamiltonian_graph

def main():
    if len(sys.argv) < 2:
        print("Określ tryb: --hamilton lub --non-hamilton")
        sys.exit(0)
    
    mode = sys.argv[1]
    nodes = int(input("nodes> "))
    if nodes <= 10:
        print("Liczba węzłów musi być większa niż 10")
        sys.exit(1)

    g = Graph(nodes)

    if mode == "--hamilton":
        saturation = int(input("saturation> "))
        nx_graph = generate_hamiltonian_graph(nodes, saturation)
    elif mode == "--non-hamilton":
        saturation = 50  # Stałe nasycenie dla grafu nie-Hamiltona
        nx_graph = generate_non_hamiltonian_graph(nodes, saturation)
    else:
        print("Nieznany tryb")
        sys.exit(1)

    # Konwersja NetworkX graph na nasz Graph obiekt
    for u, v in nx_graph.edges():
        g.add_edge(u + 1, v + 1)  # Przesunięcie indeksów o 1, aby zaczynały się od 1

    # Rysuj wygenerowany graf z etykietami
    nx.draw(nx_graph, with_labels=True)
    plt.show()

    while True:
        print("\nWybierz operację:")
        print("1. Wydrukuj graf")
        print("2. Znajdź cykl Hamiltona")
        print("3. Znajdź cykl Eulera")
        print("4. Zakończ")
        print("5. Wygeneruj graficzną reprezentację grafu")

        choice = input("Wybór: ")
        if choice == "1":
            representation = input("Podaj reprezentację grafu (matrix/list/table): ")
            g.print_graph(representation)
        elif choice == "2":
            representation = input("Podaj reprezentację grafu (matrix/list/table): ")
            print(g.hamiltonian_cycle(representation))
        elif choice == "3":
            representation = input("Podaj reprezentację grafu (matrix/list/table): ")
            print(g.find_eulerian_cycle(representation))
        elif choice == "4":
            break
        elif choice == "5":
            # Rysuj graf z etykietami
            nx.draw(nx_graph, with_labels=True)
            plt.show()
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
