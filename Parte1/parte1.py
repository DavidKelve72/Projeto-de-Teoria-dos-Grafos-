import heapq
import math


def parse_graph(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    num_vertices, _ = map(int, lines[0].split("\t"))
    S, T = map(int, lines[1].split("\t"))
    edges = []
    adj = [[] for _ in range(num_vertices)]
    for line in lines[2:]:
        u, v, cost = line.split("\t")
        u, v, cost = int(u), int(v), float(cost)
        edges.append((u, v, cost))
        adj[u].append((v, cost))
    return num_vertices, S, T, edges, adj


def dijkstra(adj, S, num_vertices):
    dist = [math.inf] * num_vertices
    prev = [-1] * num_vertices
    dist[S] = 0
    heap = [(0.0, S)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, cost in adj[u]:
            if dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev


def bellman_ford(edges, S, num_vertices):
    dist = [math.inf] * num_vertices
    prev = [-1] * num_vertices
    dist[S] = 0
    for _ in range(num_vertices - 1):
        for u, v, cost in edges:
            if dist[u] != math.inf and dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                prev[v] = u
    for u, v, cost in edges:
        if dist[u] != math.inf and dist[u] + cost < dist[v]:
            raise ValueError("Ciclo negativo detectado no grafo.")
    return dist, prev


def reconstruct_path(prev, S, T):
    path = []
    cur = T
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    if path[0] != S:
        return []
    return path


JUSTIFICATIVA_DIJKSTRA = (
    "O algoritmo de Dijkstra e selecionado pois todos os pesos do grafo sao nao-negativos, "
    "processando vertices em ordem crescente de distancia via fila de prioridade com "
    "complexidade O((V+E) log V), superior ao Bellman-Ford neste cenario."
)

JUSTIFICATIVA_BELLMAN_FORD = (
    "O algoritmo de Bellman-Ford e adotado pois o grafo contem arestas de peso negativo, "
    "relaxando todas as arestas em V-1 iteracoes com complexidade O(V*E) e verificando "
    "a ausencia de ciclos negativos por meio de uma passagem adicional."
)


def write_output(filename, algorithm, justification, path, cost):
    route = " ".join(map(str, path))
    cost_str = str(int(cost)) if cost == int(cost) else str(cost)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"ALGORITMO: {algorithm}\n")
        f.write(f"JUSTIFICATIVA: {justification}\n")
        f.write(f"ROTA: {route}\n")
        f.write(f"CUSTO: {cost_str}\n")


def solve_part1(input_file, output_file):
    num_vertices, S, T, edges, adj = parse_graph(input_file)
    has_negative = any(cost < 0 for _, _, cost in edges)

    if has_negative:
        dist, prev = bellman_ford(edges, S, num_vertices)
        algorithm, justification = "Bellman-Ford", JUSTIFICATIVA_BELLMAN_FORD
    else:
        dist, prev = dijkstra(adj, S, num_vertices)
        algorithm, justification = "Dijkstra", JUSTIFICATIVA_DIJKSTRA

    path = reconstruct_path(prev, S, T)
    cost = dist[T]
    write_output(output_file, algorithm, justification, path, cost)
    print(f"[Parte 1] {input_file} → {output_file}  ({algorithm}, custo={cost})")


solve_part1("grafo_rede_p.txt", "saida_parte1_p.txt")
solve_part1("grafo_rede_m.txt", "saida_parte1_m.txt")
