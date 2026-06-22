def parse_graph(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    num_vertices, _ = map(int, lines[0].split("\t"))
    adj = [set() for _ in range(num_vertices)]
    for line in lines[1:]:
        u, v = map(int, line.split("\t"))
        adj[u].add(v)
        adj[v].add(u)
    return num_vertices, adj


def dsatur(num_vertices, adj):
    color = [-1] * num_vertices
    saturation = [0] * num_vertices
    degree = [len(adj[v]) for v in range(num_vertices)]
    neighbor_colors = [set() for _ in range(num_vertices)]

    for _ in range(num_vertices):
        best = max(
            (v for v in range(num_vertices) if color[v] == -1),
            key=lambda v: (saturation[v], degree[v]),
        )
        used = neighbor_colors[best]
        c = 1
        while c in used:
            c += 1
        color[best] = c
        for nb in adj[best]:
            if color[nb] == -1 and c not in neighbor_colors[nb]:
                neighbor_colors[nb].add(c)
                saturation[nb] += 1

    return color


JUSTIFICATIVA = (
    "O DSatur e uma heuristica gulosa que prioriza, a cada iteracao, o vertice nao colorido de "
    "maior saturacao — quantidade de cores distintas na vizinhanca —, reduzindo conflitos de forma "
    "sistematica e produzindo coloracoes de qualidade proxima ao numero cromatico em tempo O(V^2)."
)


def write_output(filename, algorithm, justification, coloring):
    num_colors = max(coloring)
    coloracao = " ".join(f"{v}={coloring[v]}" for v in range(len(coloring)))
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"ALGORITMO: {algorithm}\n")
        f.write(f"JUSTIFICATIVA: {justification}\n")
        f.write(f"NUM_CORES: {num_colors}\n")
        f.write(f"COLORACAO: {coloracao}\n")


def solve_part2(input_file, output_file):
    num_vertices, adj = parse_graph(input_file)
    coloring = dsatur(num_vertices, adj)
    write_output(output_file, "DSatur", JUSTIFICATIVA, coloring)
    print(f"[Parte 2] {input_file} → {output_file}  (NUM_CORES={max(coloring)})")


solve_part2("grafo_wifi_p.txt", "saida_parte2_p.txt")
solve_part2("grafo_wifi_m.txt", "saida_parte2_m.txt")