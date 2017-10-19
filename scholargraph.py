import scholarly as sch
import networkx as nx


def populate_graph(paper, graph):
    '''
    :param paper: scholarly.Publication
    :param graph: networkx.classes.digraph.DiGraph
    :return: None
    '''

    # make node for initial paper in the graph
    graph.add_node(paper.bib['ID'], paper=paper)
    print paper.bib['ID']
    # get citations
    for citation in paper.get_citedby():
        # retrieve full paper information
        citation = citation.fill()
        # check to see if the paper is already on the graph
        if citation.bib['ID'] in graph.nodes():
            # if it already is just add the new edge
            graph.add_edge(paper.bib['ID'], citation.bib['ID'])
        else:
            # if not add the node, and the edge, and populate its children
            graph.add_node(citation.bib['ID'], paper=citation)
            graph.add_edge(paper.bib['ID'], citation.bib['ID'])
            populate_graph(citation, graph)


def test_pop():
    import matplotlib.pyplot as plt
    G = nx.DiGraph()
    search_query = sch.search_pubs_query('10.1109/THS.2013.6698999')
    P = search_query.next()
    P = P.fill()
    populate_graph(P, G)
    nx.draw_spectral(G)
    plt.show()


