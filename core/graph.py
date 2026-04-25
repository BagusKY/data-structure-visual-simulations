class Graph:
    def __init__(self, directed=False):
        self._adj = {}           # adjacency list: {node: [neighbors]}
        self._directed = directed

    def add_node(self, node):
        if node not in self._adj:
            self._adj[node] = []

    def add_edge(self, u, v):
        """
        Tambah edge u -> v
        Jika undirected: otomatis v -> u
        """
        self.add_node(u)
        self.add_node(v)

        self._adj[u].append(v)

        if not self._directed:
            self._adj[v].append(u)

    def remove_edge(self, u, v):
        if u in self._adj and v in self._adj[u]:
            self._adj[u].remove(v)

        if not self._directed:
            if v in self._adj and u in self._adj[v]:
                self._adj[v].remove(u)

    def get_neighbors(self, node):
        return list(self._adj.get(node, []))

    def get_nodes(self):
        return list(self._adj.keys())

    def has_node(self, node):
        return node in self._adj

    def clear(self):
        self._adj.clear()

    def get_all(self):
        """
        Return adjacency list (copy)
        """
        return {node: list(neigh) for node, neigh in self._adj.items()}

    # =========================
    # BFS (Breadth-First Search)
    # =========================
    def bfs(self, start):
        """
        Return urutan traversal BFS
        """
        if start not in self._adj:
            return []

        visited = set()
        queue = [start]
        order = []

        visited.add(start)

        while queue:
            current = queue.pop(0)
            order.append(current)

            for neighbor in self._adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def bfs_steps(self, start):
        """
        Return langkah-langkah BFS untuk animasi
        Format:
        [
            {"current": node, "queue": [...], "visited": [...]},
            ...
        ]
        """
        if start not in self._adj:
            return []

        visited = set([start])
        queue = [start]
        steps = []

        while queue:
            current = queue.pop(0)

            steps.append({
                "current": current,
                "queue": list(queue),
                "visited": list(visited)
            })

            for neighbor in self._adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return steps