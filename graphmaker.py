from GraphPlus import GraphPlus

def make_prereq() -> GraphPlus:
    """Make the prerequisites graph for the CSC major from HW1."""
    g = GraphPlus()
    g.add_edge('MTH108', 'MTH117')
    g.add_edge('MTH110', 'MTH117')
    g.add_edge('MTH110', 'MTH205')
    g.add_edge('MTH108', 'CSC201')
    g.add_edge('MTH110', 'CSC201')
    g.add_edge('CSC201', 'CSC202')
    g.add_edge('CSC202', 'CSC203')
    g.add_edge('CSC201', 'MTH205')
    g.add_edge('CSC201', 'CSC235')
    g.add_edge('CSC202', 'CSC321')
    g.add_edge('CSC321', 'CSC322')
    g.add_edge('CSC235', 'CSC335')
    g.add_edge('CSC202', 'CSC350')
    g.add_edge('CSC202', 'CSC355')
    g.add_edge('CSC202', 'CSC392')
    g.add_edge('CSC392', 'CSC492')
    return g

def makeSCInterstates():
    """Make the graph of the SC interstate highways."""
    g = GraphPlus()
    g.add2WayEdge('SPB', 'AVL', 70)
    g.add2WayEdge('SPB', 'GVL', 30)
    g.add2WayEdge('SPB', 'CLN', 36)
    g.add2WayEdge('SPB', 'CLT', 75)
    g.add2WayEdge('GVL', 'CLN', 46)
    g.add2WayEdge('GVL', 'ATL', 145)
    g.add2WayEdge('CLN', 'CLB', 63)
    g.add2WayEdge('CLB', 'CLT', 93)
    g.add2WayEdge('CLB', 'AUG', 76)
    g.add2WayEdge('CLB', 'FLO', 83)
    g.add2WayEdge('CLB', 'WSL', 62)
    g.add2WayEdge('CLB', 'WSL', 62)
    g.add2WayEdge('WSL', 'FLO', 86)
    g.add2WayEdge('WSL', 'SAV', 99)
    g.add2WayEdge('WSL', 'CHS', 58)
    g.add2WayEdge('FLO', 'FAY', 88)    
    return g

def make_graph_7_18():
    "Make the graph from section 7.18 of Miller & Ranum."
    g = GraphPlus()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('B', 'E')
    g.add_edge('C', 'C')
    g.add_edge('C', 'F')
    g.add_edge('D', 'B')
    g.add_edge('D', 'G')
    g.add_edge('E', 'A')
    g.add_edge('E', 'D')
    g.add_edge('F', 'H')
    g.add_edge('G', 'E')
    g.add_edge('H', 'I')
    g.add_edge('I', 'F')
    return g
