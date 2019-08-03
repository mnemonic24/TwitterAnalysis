import networkx as nx
import matplotlib.pyplot as plot

class NetworkAnalysis:
    def __init__(self):
        self.graph = None

    def from_dict(self, dataset):
        if isinstance(dataset, dict):
            self.graph = nx.from_dict_of_lists(dataset)
        else:
            print('Type Error')

    def load_file(self, path):
        self.graph = nx.read_gml(path)

    def save_graph(self, filename):
        nx.write_gml(self.graph, filename)

    def display(self, figsize=(6, 6)):
        pos = nx.spring_layout(self.graph)
        plot.figure(figsize=figsize)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_nodes(self.graph, pos)
        plot.axis('off')
        plot.show()

if __name__ == "__main__":
    na = NetworkAnalysis()
    na.load_file('graph/twitter.gml')
    na.display()

    