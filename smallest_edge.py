def smallest_edge(graph):
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]["weight"])

    path = []
    dist = 0
    visited = set()

    node_connection_count = {node: 0 for node in graph.nodes}
    parent = {node: node for node in graph.nodes}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(start, end):
        root1 = find(start)
        root2 = find(end)
        if root1 != root2:
            parent[root2] = root1

    start_node = list(graph.nodes)[0]
    path.append(start_node)
    curr_node = start_node
    visited.add(curr_node)

    while len(visited) < len(graph.nodes):
        for edge in edges:
            start, end, distance = edge
            if (start == curr_node and end not in visited) or (
                end == curr_node and start not in visited
            ):
                if (
                    node_connection_count[start] < 2
                    and node_connection_count[end] < 2
                    and find(start) != find(end)
                ):
                    next_node = end if start == curr_node else start
                    path.append(next_node)
                    dist += distance["weight"]
                    visited.add(next_node)
                    node_connection_count[start] += 1
                    node_connection_count[end] += 1
                    union(start, end)
                    curr_node = next_node
                    break

    path.append(start_node)
    dist += graph[curr_node][start_node]["weight"]

    print(path)
    print(dist)
    return path
