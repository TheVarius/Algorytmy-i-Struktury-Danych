import sys
import matplotlib.pyplot as plt
import networkx as nx
from projekt4 import Graph

def generate_hamiltonian_graph(nodes, saturation):
    g = Graph(nodes)
    g.create_graph_with_saturation(saturation / 100)
    return g

def generate_non_hamiltonian_graph(nodes, saturation):
    g = Graph(nodes)
    g.create_non_hamiltonian_graph(saturation / 100)
    return g

def main():
    if len(sys.argv) < 2:
        print("Specify mode: --hamilton or --non-hamilton")
        sys.exit(0)
    
    mode = sys.argv[1]
    nodes = int(input("nodes> "))
    if nodes <= 10:
        print("Number of nodes must be greater than 10")
        sys.exit(1)

    if mode == "--hamilton":
        saturation = int(input("saturation> "))
        g = generate_hamiltonian_graph(nodes, saturation)
    elif mode == "--non-hamilton":
        saturation = 50  # Fixed saturation for non-Hamiltonian graph
        g = generate_non_hamiltonian_graph(nodes, saturation)
    else:
        print("Unknown mode")
        sys.exit(1)
    while True:
        print("\nSelect an operation:")
        print("1. Print the graph")
        print("2. Find Hamiltonian cycle")
        print("3. Find Euler cycle")
        print("4. Export graph as image")
        print("5. Exit")

        choice = input("Choice: ")
        if choice == "1":
            print("Select graph representation:")
            print("1. matrix")
            print("2. list")
            print("3. table")
            rep_choice = input("Representation: ")
            if rep_choice == "1":
                representation = "matrix"
            elif rep_choice == "2":
                representation = "list"
            elif rep_choice == "3":
                representation = "table"
            else:
                print("Invalid representation choice.")
                sys.exit(1)
            g.print_graph(representation)
        elif choice == "2":
            g.find_hamiltonian_cycle()
        elif choice == "3":
            g.euler()
        elif choice == "4":
            filename = input("Enter filename (with .png extension): ")
            g.export_graph(filename)
            print(f"Graph exported as {filename}")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
