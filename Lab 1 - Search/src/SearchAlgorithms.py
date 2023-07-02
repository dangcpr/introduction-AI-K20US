from Space import *
from Constants import *

def DFS(g:Graph, sc:pygame.Surface):
    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()

    while open_set:
        current_node_value = open_set.pop()
        current_node = g.grid_cells[current_node_value]
        current_node.set_color(yellow)
        #g.draw(sc)

        if g.is_goal(current_node):
            # Path found
            path = []
            while current_node.value != g.start.value:
                path.append(current_node.value)
                current_node = g.grid_cells[father[current_node.value]]
            path.append(g.start.value)
            path.reverse()

            g.start.set_color(orange)
            g.goal.set_color(purple)

            # mark the path nodes as gray
            for node in path:
                if (node == g.start.value):
                    g.start.set_color(orange)
                    continue
                if (node == g.goal.value):
                    g.goal.set_color(purple)
                    continue
                g.grid_cells[node].set_color(grey)
                g.draw(sc)
                pygame.time.delay(20)

            # draw a light gray line connecting the path nodes
            for i in range(len(path)-1):
                pygame.draw.line(sc, green, (g.grid_cells[path[i]].x, g.grid_cells[path[i]].y), (g.grid_cells[path[i+1]].x, g.grid_cells[path[i+1]].y), 4)
                pygame.display.flip()
                pygame.time.delay(20)

            return path

        closed_set.append(current_node_value)

        for neighbor in g.get_neighbors(current_node):
            if neighbor.value not in closed_set:
                if neighbor.value not in open_set:
                    open_set.append(neighbor.value)
                    father[neighbor.value] = current_node.value
                neighbor.set_color(red)

        g.draw(sc)
        current_node.set_color(blue)

        # Pause for a short time to show the visualization
        pygame.time.wait(20)
    raise NotImplementedError('Not implemented')


def BFS(g:Graph, sc:pygame.Surface):
    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()

    while open_set:
        current_node_value = open_set.pop(0)
        closed_set.append(current_node_value)
        current_node = g.grid_cells[current_node_value]
        current_node.set_color(yellow)
        #g.draw(sc)

        if g.is_goal(current_node):
            # Path found
            path = []
            while current_node.value != g.start.value:
                path.append(current_node.value)
                current_node = g.grid_cells[father[current_node.value]]
            path.append(g.start.value)
            path.reverse()

            g.start.set_color(orange)
            g.goal.set_color(purple)

            # mark the path nodes as gray
            for node in path:
                if (node == g.start.value):
                    g.start.set_color(orange)
                    continue
                if (node == g.goal.value):
                    g.goal.set_color(purple)
                    continue
                g.grid_cells[node].set_color(grey)
                g.draw(sc)
                pygame.time.delay(20)

            # draw a light gray line connecting the path nodes
            for i in range(len(path)-1):
                pygame.draw.line(sc, green, (g.grid_cells[path[i]].x, g.grid_cells[path[i]].y), (g.grid_cells[path[i+1]].x, g.grid_cells[path[i+1]].y), 4)
                pygame.display.flip()
                pygame.time.delay(20)

            return path

        for neighbor in g.get_neighbors(current_node):
            if neighbor.value not in closed_set:
                if neighbor.value not in open_set:
                    open_set.append(neighbor.value)
                    father[neighbor.value] = current_node.value

        # Draw the current node and its neighbors
        
        #g.draw(sc)
        
        for neighbor in g.get_neighbors(current_node):
            if neighbor.value not in closed_set:
                neighbor.set_color(red)
        g.draw(sc)
        current_node.set_color(blue)

        # Pause for a short time to show the visualization
        pygame.time.wait(20)
    raise NotImplementedError('Not implemented')



def UCS(g:Graph, sc:pygame.Surface):
    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    cost = [float('inf')]*g.get_len()
    cost[g.start.value] = 0

    while open_set:
        current_node_value = min(open_set, key=lambda x: cost[x])
        open_set.remove(current_node_value)
        closed_set.append(current_node_value)
        current_node = g.grid_cells[current_node_value]
        current_node.set_color(yellow)

        if g.is_goal(current_node):
            # Path found
            path = []
            while current_node.value != g.start.value:
                path.append(current_node.value)
                current_node = g.grid_cells[father[current_node.value]]
            path.append(g.start.value)
            path.reverse()

            g.start.set_color(orange)
            g.goal.set_color(purple)

            # mark the path nodes as gray
            for node in path:
                if (node == g.start.value):
                    g.start.set_color(orange)
                    continue
                if (node == g.goal.value):
                    g.goal.set_color(purple)
                    continue
                g.grid_cells[node].set_color(grey)
                g.draw(sc)
                pygame.time.delay(20)

            # draw a light gray line connecting the path nodes
            for i in range(len(path)-1):
                pygame.draw.line(sc, green, (g.grid_cells[path[i]].x, g.grid_cells[path[i]].y), (g.grid_cells[path[i+1]].x, g.grid_cells[path[i+1]].y), 4)
                pygame.display.flip()
                pygame.time.delay(20)

            return path

        for neighbor in g.get_neighbors(current_node):
            if neighbor.value not in closed_set:
                new_cost = cost[current_node.value] + get_cost(current_node, neighbor)
                if new_cost < cost[neighbor.value]:
                    cost[neighbor.value] = new_cost
                    father[neighbor.value] = current_node.value
                    if neighbor.value not in open_set:
                        open_set.append(neighbor.value)
                        neighbor.set_color(red)

        # Draw the current node and its neighbors
        g.draw(sc)
        current_node.set_color(blue)
        for neighbor in g.get_neighbors(current_node):
            if neighbor.value not in closed_set:
                neighbor.set_color(red)

    raise NotImplementedError('Not implemented')


def AStar(g:Graph, sc:pygame.Surface):
    open_set = [(g.start.value, 0)]
    closed_set = []
    father = [-1] * g.get_len()
    g_score = {node.value: float('inf') for node in g.grid_cells}
    g_score[g.start.value] = 0
    f_score = {node.value: float('inf') for node in g.grid_cells}
    f_score[g.start.value] = manhattan_distance(g.start, g.goal)

    while open_set:
        current_node_value, cost = min(open_set, key=lambda x: f_score[x[0]])
        open_set.remove((current_node_value, cost))
        closed_set.append(current_node_value)
        current_node = g.grid_cells[current_node_value]
        current_node.set_color(yellow)

        if g.is_goal(current_node):
            # Path found
            path = []
            while current_node.value != g.start.value:
                path.append(current_node.value)
                current_node = g.grid_cells[father[current_node.value]]
            path.append(g.start.value)
            path.reverse()

            g.start.set_color(orange)
            g.goal.set_color(purple)

            # mark the path nodes as gray
            for node in path:
                if (node == g.start.value):
                    g.start.set_color(orange)
                    continue
                if (node == g.goal.value):
                    g.goal.set_color(purple)
                    continue
                g.grid_cells[node].set_color(grey)
                g.draw(sc)
                pygame.time.delay(20)

            # draw a light gray line connecting the path nodes
            for i in range(len(path) - 1):
                pygame.draw.line(sc, green, (g.grid_cells[path[i]].x, g.grid_cells[path[i]].y),
                                 (g.grid_cells[path[i + 1]].x, g.grid_cells[path[i + 1]].y), 4)
                pygame.display.flip()
                pygame.time.delay(20)

            return path

        for neighbor in g.get_neighbors(current_node):
            if neighbor.value in closed_set:
                continue
            tentative_g_score = g_score[current_node.value] + 1
            if neighbor.value not in [x[0] for x in open_set]:
                open_set.append((neighbor.value, tentative_g_score))
            elif tentative_g_score >= g_score[neighbor.value]:
                continue
            father[neighbor.value] = current_node.value
            g_score[neighbor.value] = tentative_g_score
            f_score[neighbor.value] = g_score[neighbor.value] + manhattan_distance(neighbor, g.goal)

            neighbor.set_color(red)
        g.draw(sc)
        current_node.set_color(blue)

        # Pause for a short time to show the visualization
        pygame.time.wait(20)
    raise NotImplementedError('Not implemented')

def manhattan_distance(node1: Node, node2: Node) -> int:
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def get_cost(node1:Node, node2:Node) -> int:
    '''
    trả về giá trị của cạnh nối 2 node `node1` và `node2`
    '''
    r1 = node1.value//(cols-2)
    c1 = node1.value%(cols-2)
    r2 = node2.value//(cols-2)
    c2 = node2.value%(cols-2)

    if r1 == r2 or c1 == c2:            
        return 10
    else:
        return 14

