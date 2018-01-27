import json
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import heapq

## first part

# This function read the input file and save it as a data variable
def loader(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

# Function for creating the dictionary with authors as a key and related publications.
def Author(file):
    dictAuthor = {}
    for i in range(len(file)):
        for author in file[i]["authors"]:
            try:
                dictAuthor[author["author_id"]] += [(file[i]["id_publication_int"])]
            except:
                dictAuthor[author["author_id"]] = [(file[i]["id_publication_int"])]

    return dictAuthor

# function for creating the dictionary with publications as a keys and authors as a values
def Publ(file):
    dictPubl = {}
    for i in range(len(file)):
        for author in file[i]["authors"]:
            try:
                dictPubl[file[i]["id_publication_int"]] += [(author["author_id"])]
            except:
                dictPubl[file[i]["id_publication_int"]] = [(author["author_id"])]
    return dictPubl
    
# function for creating the dictionary for conference as a key and authors as a values
def Conf(file):
    dictConf = {}
    for i in range(len(file)):
        for author in file[i]["authors"]:
            try:
                dictConf[file[i]["id_conference_int"]] += [(author["author_id"])]
            except:
                dictConf[file[i]["id_conference_int"]] = [(author["author_id"])]

    return dictConf

# function to create a graph - as a nodes are taken authors from the previously created dictionary dictAuthor
def createGraph(dictAuthor):
    Gall = nx.Graph()
    for k, v in dictAuthor.items():
        Gall.add_node(k, id=v[0])
    return Gall

# for computing the weights of edges with Jaccard similarity
def JaccardDistance(a,b):
    num = (len(list(set(a)&set(b))))
    den = len(list(set(a)|set(b)))
    j = 1 - num/den
    return j

# function for adding edges to the graph
def addEdges(dictPubl):
    for k, v in dictPubl.items():
        # edges are taken from created dictionary, because we want connect authors with their coworkers.
        for i in itertools.combinations(v, 2):  # all combinations between 2 values of v (author_id)
            Gall.add_edge(i[0], i[1], weight=JaccardDistance(dictAuthor[i[0]], dictAuthor[i[1]]))
    return Gall

# for plotting, but not used at the end
def draw_graph(graph):
    nx.draw_networkx(graph)
    plt.show()
    
    
## Second part
# for more information - see report.pdf
# plot the degree distribution
def degree(graph):
    degree_sequence = sorted(nx.degree_centrality(graph),reverse=True)
    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("Degree")
    plt.xlabel("Rank")
    plt.show()
    
# plot and compute closeness, which is represented in the histogram
def closeness(graph):
    close_centrality = nx.closeness_centrality(graph)
    values_centrality = [i for i in close_centrality.values()]
    plt.hist(values_centrality,ec ='black',bins = 10, color="orange")
    plt.title("Closeness rank plot")
    plt.ylabel("Closeness")
    plt.xlabel("Rank")
    plt.show()

# plot and compute betweenness
def betweeness(graph):
    bet = nx.betweenness_centrality(graph, weight= 'weight')
    bet2 = sorted(list(bet.values()), reverse=True)
    #values_betweeness = [i for i in bet.values()]
    plt.hist(bet2,ec ='black',bins = 10, color="red")
    plt.title("Betweeness rank plot")
    plt.ylabel("Betweeness")
    plt.xlabel("Rank")
    plt.show()
    
    
# for computing hop distance, we used function from the package networkx, which does exactly what we want
# at the end, we plot the subgraph
def hop_distance(graph):
    id_author = int(input('Please, give me an ID of the Author: '))
    neighbor = int(input('Please, tell me, what distance of neighbors do you want?: '))
    sub = nx.ego_graph(graph, id_author, radius = neighbor)
    nx.draw_networkx(sub)
    plt.show()
    
    
## third part
def dijkstra(graph, source, target):
    visited = set()
    heap_distance = []
    INF = ((1<<63) - 1)//2   #((1 * 2**63)-1)//2
    #initialization
    try:
        # in this loop, we initialize the "potential" of the nodes, 0 for the source and INF for all others, and we put them in heap_distance
        for node in graph.nodes():
            if node != source:
                heapq.heappush(heap_distance, (INF, node))
            else:
                heapq.heappush(heap_distance, (0, node))
        # check if the values are connected
        if nx.has_path(graph, source, target):
            while heap_distance:
                wanted_distance, w = heapq.heappop(heap_distance)   # wanted_distance became the new potential and w the node
                if w == target:
                    break #found him!
                #add node w onto visited list
                visited.add(w)
                # initialize neighbors list
                nblist = []
                for x in graph.neighbors(w):
                    # if neighbor of w is not just visited, we add it in nblist
                    if x not in visited:
                        nblist.append(x)
                for nd in nblist:
                    # new_distance is the sum between wanted_distance and the attribute weight associated with edge (w,nd)
                    new_distance = wanted_distance + graph.get_edge_data(w, nd)['weight']
                    # update the new "potential" of nd in heap_distance as new_distance
                    heapq.heappush(heap_distance, (new_distance, nd))
            return (wanted_distance)
        else:
            print ('You shall not path!!!')
    except:
        print('Choose node from graph, please!')

# function for group numbers, as an input takes graph and list of nodes we want to check
def three_b(Gall, nodes_list):
    lst=[]
    output={}
    # with the help of the networx package, first we check if the nodes are connected or not
    connected = sorted(nx.connected_components(Gall), key=len, reverse=True)
    for i in range(len(connected)):
        for node in Gall.node:
            for node_l in nodes_list:
                print("I' m examining these nodes: " + str((node,node_l)))
                if ((node and node_l) in connected[i]):
                    try:
                        print("The nodes: " + str((node,node_l)) + " are connected with distance " + str(dijkstra(Gall,node_l)[node]))
                        lst.append(dijkstra_b(Gall,node_l)[node])
                    except:
                        print("No connected")
                else:
                    print("The nodes are not connected")
    for i in range(len(lst)):
        output[node_l]=min(lst[i])
    return output
# congregated function for whole parts
def function2a(Gall, dictConf):
    a = int(input('Give me an ID of conference, please: '))
    subgraph = Gall.subgraph(dictConf[a])
    nx.draw_networkx(subgraph)
    plt.show()
    degree(subgraph)
    closeness(subgraph)
    betweeness(subgraph)

def function2b(Gall):
    hop_distance(Gall)

def function3a(Gall):
    Aris = 256176
    another_guy = int(input('Who do you want to connect?(ID please): '))
    print(dijkstra_a(Gall, Aris, another_guy))

def function3b(Gall):
    nodes_list = list(map(int,input('Give me numbers (Example - 114691,7289): ').split(",")))
    three_b(Gall, nodes_list)


# To run the first part automatically
data = loader('/Users/Dario/Desktop/Aris_Homeworks/AMD_Homework_4/full_dblp.json')
dictAuthor = Author(data)
dictPubl = Publ(data)
dictConf = Conf(data)
Gall = createGraph(dictAuthor)
Gall = addEdges(dictPubl)
#draw_graph(Gall)

# then ask user, what he wants...
n = 0
while n != 'save me':
    n = input("Enter the number of part you want (2a, 2b, 3a, 3b) or type 'save me', if you want to quit: ")
    if n == '2a':
        function2a(Gall, dictConf)
    elif n =='2b':
        function2b(Gall)
    elif n =='3a':
        function3a(Gall)
    elif n =='3b':
        function3b(Gall)
    elif n == 'save me':
        print ('It was pleasure to meat you')
    else:
        print ('Choose another part, please')

