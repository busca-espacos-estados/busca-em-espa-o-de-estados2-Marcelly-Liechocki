from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier = 1

        while frontier:
            max_frontier = max(max_frontier, len(frontier))
            node = frontier.pop()
            nodes_expanded += 1

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier,
                    depth=node.cost,
                )

            if node.cost < self.depth_limit:
                for child in node.neighbors():
                    nodes_generated += 1
                    ancestor = node
                    in_path = False
                    while ancestor is not None:
                        if ancestor.tiles == child.tiles:
                            in_path = True
                            break
                        ancestor = ancestor.parent
                    if not in_path:
                        frontier.append(child)

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier,
        )
