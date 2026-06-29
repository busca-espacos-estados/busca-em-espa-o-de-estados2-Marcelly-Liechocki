import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for idx, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_idx = tile - 1
            curr_row, curr_col = divmod(idx, 3)
            goal_row, goal_col = divmod(goal_idx, 3)
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        counter = 0
        heap = [(self.heuristic(initial), counter, initial)]
        visited: dict = {}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier = 1

        while heap:
            max_frontier = max(max_frontier, len(heap))
            _, _, node = heapq.heappop(heap)

            if node in visited and visited[node] <= node.cost:
                continue
            visited[node] = node.cost
            nodes_expanded += 1

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier,
                    depth=node.cost,
                )

            for child in node.neighbors():
                nodes_generated += 1
                if child not in visited or visited[child] > child.cost:
                    counter += 1
                    heapq.heappush(heap, (child.cost + self.heuristic(child), counter, child))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier,
        )
