import sys
from collections import defaultdict


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for i in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append({"u": u, "v": v, "w": w, "id": i + 1, "in_tree": i < n - 1})

    order = list(range(m))
    order.sort(key=lambda a: (edges[a]["w"], not edges[a]["in_tree"]))

    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def unite(a, b):
        a, b = find(a), find(b)
        if a == b:
            return False
        if rank[a] < rank[b]:
            a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1
        return True

    in_mst = [False] * m
    for idx in order:
        e = edges[idx]
        if unite(e["u"], e["v"]):
            in_mst[idx] = True

    to_remove = []
    to_add = []
    for i, e in enumerate(edges):
        if e["in_tree"] and not in_mst[i]:
            to_remove.append(i)
        if not e["in_tree"] and in_mst[i]:
            to_add.append(i)

    to_add.sort(key=lambda i: edges[i]["w"])

    adj = defaultdict(list)
    for i in range(n - 1):
        e = edges[i]
        adj[e["u"]].append((e["v"], e["id"], e["w"]))
        adj[e["v"]].append((e["u"], e["id"], e["w"]))

    id_to_idx = {edges[i]["id"]: i for i in range(m)}
    marked_remove = [False] * m
    for idx in to_remove:
        marked_remove[idx] = True

    swaps = []

    def rebuild_parents():
        par = [0] * (n + 1)
        par_edge = [0] * (n + 1)
        depth = [0] * (n + 1)
        stack = [1]
        par[1] = 0
        while stack:
            u = stack.pop()
            for v, eid, _ in adj[u]:
                if v == par[u]:
                    continue
                par[v] = u
                par_edge[v] = eid
                depth[v] = depth[u] + 1
                stack.append(v)
        return par, par_edge, depth

    def find_heaviest_marked(u, v, par, par_edge, depth, active_remove):
        best_w = -1
        best_id = -1

        def consider(edge_id):
            nonlocal best_w, best_id
            eidx = id_to_idx[edge_id]
            if active_remove[eidx] and edges[eidx]["w"] > best_w:
                best_w = edges[eidx]["w"]
                best_id = edge_id

        def lift(x):
            while depth[x] > depth[v]:
                consider(par_edge[x])
                x = par[x]
            return x

        u = lift(u)
        v = lift(v)
        while u != v:
            if depth[u] < depth[v]:
                u, v = v, u
            consider(par_edge[u])
            u = par[u]
        return best_id

    for add_idx in to_add:
        par, par_edge, depth = rebuild_parents()
        e = edges[add_idx]
        rem_id = find_heaviest_marked(
            e["u"], e["v"], par, par_edge, depth, marked_remove
        )
        swaps.append((rem_id, e["id"]))

        rem_idx = id_to_idx[rem_id]
        marked_remove[rem_idx] = False

        a, b = edges[rem_idx]["u"], edges[rem_idx]["v"]
        adj[a] = [(x, i, w) for x, i, w in adj[a] if not (x == b and i == rem_id)]
        adj[b] = [(x, i, w) for x, i, w in adj[b] if not (x == a and i == rem_id)]

        u, v, nid, nw = e["u"], e["v"], e["id"], e["w"]
        adj[u].append((v, nid, nw))
        adj[v].append((u, nid, nw))

    out = [str(len(swaps))]
    out.extend(f"{rem} {add}" for rem, add in swaps)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
