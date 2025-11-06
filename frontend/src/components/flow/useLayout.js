import dagre from '@dagrejs/dagre'
import { Position } from '@vue-flow/core'
import { ref } from 'vue'

/**
 * Composable to run the layout algorithm on the graph.
 * It uses the `dagre` library to calculate the layout of the nodes and edges.
 */
export function useLayout() {
  const graph = ref(new dagre.graphlib.Graph())
  const previousDirection = ref('LR')

  function layout(nodes, edges, direction = 'LR') {
    // Create a new graph instance
    const dagreGraph = new dagre.graphlib.Graph()
    graph.value = dagreGraph

    dagreGraph.setDefaultEdgeLabel(() => ({}))

    const isHorizontal = direction === 'LR'
    dagreGraph.setGraph({ 
      rankdir: direction,
      nodesep: isHorizontal ? 100 : 150,  // ✅ Spacing between nodes in same rank
      ranksep: isHorizontal ? 300 : 200,  // ✅ Spacing between ranks
      edgesep: 50,                         // ✅ Spacing between edges
      marginx: 50,
      marginy: 50,
    })

    previousDirection.value = direction

    // Add nodes to graph
    for (const node of nodes) {
      dagreGraph.setNode(node.id, { 
        width: node.width || 280, 
        height: node.height || 70 
      })
    }

    // Add edges to graph
    for (const edge of edges) {
      dagreGraph.setEdge(edge.source, edge.target)
    }

    // Calculate layout
    dagre.layout(dagreGraph)

    // Set nodes with updated positions
    return nodes.map((node) => {
      const nodeWithPosition = dagreGraph.node(node.id)

      return {
        ...node,
        targetPosition: isHorizontal ? Position.Left : Position.Top,
        sourcePosition: isHorizontal ? Position.Right : Position.Bottom,
        position: { x: nodeWithPosition.x, y: nodeWithPosition.y },
      }
    })
  }

  return { graph, layout, previousDirection }
}
