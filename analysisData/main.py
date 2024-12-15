def determine_cell_type(queries):
    results = []

    for ni, ki in queries:
        current_generation = "X"

        # Simulate the process for ni steps
        for _ in range(ni):
            next_generation = ""
            for cell in current_generation:
                if cell == "X":
                    next_generation += "XY"
                else:
                    next_generation += "YX"
            current_generation = next_generation

        # Get the cell type at position ki (1-indexed)
        results.append(current_generation[ki - 1])

    return results
if __name__ == '__main__':
    t =  int(input())
    queries = []
    for _ in range(t):
        a,b = map(int,(input().split()))
        queries.append((a,b))

    results = determine_cell_type(queries)
    for result in results:
        print(result)