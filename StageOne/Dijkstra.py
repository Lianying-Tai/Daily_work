import heapq
import networkx as nx
import matplotlib.pyplot as plt

# ------------------------------
# 1. 构建示例图 (有向加权图)
# ------------------------------
# 使用邻接表表示：节点 -> (邻居, 权重)
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('D', 8), ('E', 10)],
    'D': [('E', 2), ('F', 6)],
    'E': [('F', 3)],
    'F': []
}

# 所有节点列表
nodes = list(graph.keys())

# 创建 NetworkX 有向图
G = nx.DiGraph()
for u in graph:
    for v, w in graph[u]:
        G.add_edge(u, v, weight=w)

# 固定布局，使每次绘制位置一致
pos = nx.spring_layout(G, seed=42)  # 也可用其他布局，如 nx.circular_layout

# ------------------------------
# 2. 初始化算法数据结构
# ------------------------------
source = 'A'  # 源节点
dist = {node: float('inf') for node in nodes}
prev = {node: None for node in nodes}
dist[source] = 0

# 优先队列 (距离, 节点)
pq = [(0, source)]
visited = set()  # 已确定最短路径的节点

# ------------------------------
# 3. 可视化设置
# ------------------------------
plt.ion()  # 开启交互模式
fig, ax = plt.subplots(figsize=(8, 6))


def draw_step(current_node=None, highlight_edge=None):
    """绘制当前状态的图"""
    ax.clear()

    # 节点颜色：源节点为绿色，已访问节点为浅蓝色，当前节点为红色，其余为灰色
    node_colors = []
    for node in G.nodes():
        if node == source:
            node_colors.append('lightgreen')
        elif node in visited:
            node_colors.append('skyblue')
        elif node == current_node:
            node_colors.append('red')
        else:
            node_colors.append('lightgray')

    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)

    # 绘制边（普通边为黑色，如果指定了 highlight_edge 则用红色加粗）
    edges = G.edges()
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='black', arrows=True,
                           arrowsize=20, width=1, ax=ax)
    if highlight_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[highlight_edge], edge_color='red',
                               arrows=True, arrowsize=20, width=2, ax=ax)

    # 绘制边上权重
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)

    # 在节点旁边显示当前距离
    for node in nodes:
        d = dist[node]
        label = f'{d}' if d != float('inf') else '∞'
        x, y = pos[node]
        ax.text(x + 0.05, y + 0.05, label, fontsize=12, bbox=dict(facecolor='white', alpha=0.7))

    # 图标题
    ax.set_title(f"Dijkstra Step - Current: {current_node}" if current_node else "Dijkstra Start")
    ax.axis('off')
    plt.draw()
    plt.pause(1.0)  # 暂停1秒，方便观察


# 绘制初始状态
draw_step()

# ------------------------------
# 4. Dijkstra 算法主循环 + 可视化
# ------------------------------
while pq:
    # 弹出当前距离最小的节点
    current_dist, current = heapq.heappop(pq)

    # 如果该节点已经访问过，则跳过（因为优先队列中可能保留旧记录）
    if current in visited:
        continue

    # 标记为已访问
    visited.add(current)

    # 绘制当前步骤（高亮当前节点）
    draw_step(current_node=current)

    # 遍历邻居
    for neighbor, weight in graph[current]:
        if neighbor in visited:
            continue

        new_dist = current_dist + weight
        if new_dist < dist[neighbor]:
            dist[neighbor] = new_dist
            prev[neighbor] = current
            heapq.heappush(pq, (new_dist, neighbor))

            # 绘制松弛边（高亮正在处理的边）
            draw_step(current_node=current, highlight_edge=(current, neighbor))
        else:
            # 也可短暂显示无需松弛的边（灰色），这里简单跳过
            pass

# 最终结果展示
draw_step()
plt.ioff()
plt.show()

# 打印最终最短路径结果
print("\n最终最短距离:")
for node in nodes:
    print(f"{source} -> {node} : {dist[node]}")
print("\n前驱节点:", prev)