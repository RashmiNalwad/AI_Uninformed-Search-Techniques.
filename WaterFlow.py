class Node:
    ID = 0
    STATE = "",
    PARENT_NODE = {},
    PATH_LENGTH = 0,
    TYPE = ""
    OFF_PERIODS = {}
    IN_OPEN = False
    IN_CLOSE = False

    def _init_(self):
        pass
    def assign_values(self,ID,STATE,PARENT_NODE,PATH_LENGTH,TYPE,OFF_PERIODS,IN_OPEN,IN_CLOSE):
        self.ID = ID
        self.STATE = STATE
        self.PARENT_NODE = PARENT_NODE
        self.PATH_LENGTH = PATH_LENGTH
        self.TYPE = TYPE
        self.OFF_PERIODS = OFF_PERIODS #OFF Period map with src and dest as Key and all off periods as value.
        self.IN_OPEN = IN_OPEN
        self.IN_CLOSE = IN_CLOSE

class BFS_Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    
def read_write_file(file_handler): #Reading Entire file
    algo_type = ""
    write_handler = open('output.txt','w')
    for each_line in file_handler:
        if "BFS" in each_line:
            print("Running BFS")
            algo_type = each_line
            graph,source,dest_nodes = read_data(file_handler,algo_type) #Calling read data only for that type of ALGO,returns Dictionary
            run_bfs(graph,source,dest_nodes,write_handler) #Make BFS Queue Method Call
        elif "DFS" in each_line:
            print("Running DFS")
            algo_type = each_line
            graph,source,dest_nodes = read_data(file_handler,algo_type) #read_ data,returns Dictionary
            run_dfs(graph,source,dest_nodes,write_handler)
        elif "UCS" in each_line:
            print("Running UCS")
            each_line.rstrip("\n")
            algo_type = each_line
            graph,source,dest_nodes = read_data(file_handler,algo_type) #read_ data,returns Dictionary                
            run_ucs(graph, source, dest_nodes, write_handler)
    write_handler.close()        
            
def run_bfs(graph,source,destination_list,write_handler):
    print("Inside RUN BFS Method")
    oq = BFS_Queue() #open set
    eq = BFS_Queue() #explored set
    oq.enqueue(source)
    print(source.STATE)
    while True:
        if oq.isEmpty():
            print("All nodes are explored, No destination found")
            write_handler.write("None" + "\n")
            return
        else:
            node = oq.dequeue()
        print("Node for Goal test " + str(node.STATE))
        parent_time = int(node.PATH_LENGTH)
        if node in destination_list:
            print("Found destination")
            print("Node Name : " + str(node.STATE))
            print("Node Path Time : " + str(node.PATH_LENGTH))
            print(str(node.STATE) + " " + str(node.PATH_LENGTH) + "\n")
            if (node.PATH_LENGTH > 23):
                node.PATH_LENGTH = node.PATH_LENGTH % 24
            write_handler.write(str(node.STATE) + " " + str(node.PATH_LENGTH) + "\n")
            return node
        else:
            if node in graph.keys():
                child_list = graph[node]     
                child_list.sort(key=lambda x:x.STATE)              
                if len(child_list) != 0:
                    for child in child_list:
                        if child not in oq.items and child not in eq.items:  #check whether visited node is getting enqueued.
                            print("Child being enqueued " + str ( child.STATE ) )     
                            child.PATH_LENGTH = parent_time + 1 
                            oq.enqueue(child)
        
        eq.enqueue(node.STATE)    

def run_dfs(graph,source,destination_list,write_handler):
    print("Inside RUN DFS Method")
    oq = [] #open set
    eq = [] #explored set
    oq.append(source)
    print(source.STATE)
    while True:
        if len(oq) == 0:
            print("All nodes are explored and No destination found")
            write_handler.write("None" + "\n")
            return
        else:
            node = oq.pop()
        print("Node for Goal test " + str(node.STATE))
        parent_time = int(node.PATH_LENGTH)
        if node in destination_list:
            print("Found destination")
            print("Node Name : " + str(node.STATE))
            print("Node Path Time : " + str(node.PATH_LENGTH))
            print(str(node.STATE) + " " + str(node.PATH_LENGTH) + "\n")
            if (node.PATH_LENGTH > 23):
                node.PATH_LENGTH = node.PATH_LENGTH % 24
            write_handler.write(str(node.STATE) + " " + str(node.PATH_LENGTH) + "\n")
            return node
        else:
            if node in graph.keys():
                child_list = graph[node]     
                child_list.sort(key=lambda x:x.STATE,reverse=True)              
                if len(child_list) != 0:
                    for child in child_list:
                        if child not in eq:  #check whether visited node is getting enqueued.
                            print("Child being enqueued " + str ( child.STATE ) )     
                            child.PATH_LENGTH = parent_time + 1 
                            oq.append(child)
        
        eq.append(node.STATE)   
        
def run_ucs(graph,source,destination_list,write_handler):
    print("Inside RUN Uniform Cost Search")
    oq = [] #open set
    eq = [] #explored set
    found_dest = False
    oq.append(source)
    while True:
        if len(oq) == 0:
            if found_dest == False:
                print("All nodes are explored and no destination found")
                write_handler.write("None" + "\n")
            return
        else:
            node = oq.pop()
        print("Node for Goal test " + str(node.STATE))
        if node in destination_list:
            found_dest = True
            print("Found destination")
            print("Node Name : " + str(node.STATE))
            print("Node Path Time : " + str(node.PATH_LENGTH))
            print(str(node.STATE) + " " + str(node.PATH_LENGTH) + "\n")
            if (node.PATH_LENGTH > 23):
                node.PATH_LENGTH = node.PATH_LENGTH % 24    
            write_handler.write(str(node.STATE) + " " + str(node.PATH_LENGTH) + "\n")
            return node
        if node in graph.keys():
            sorted_child_list = []
            child_list = graph[node]    
            
            for kid in child_list:
                if kid.PATH_LENGTH > kid.PARENT_NODE.get(node.STATE) + node.PATH_LENGTH or kid.PATH_LENGTH == 0:
                    kid.PATH_LENGTH = kid.PARENT_NODE.get(node.STATE) + node.PATH_LENGTH 
                    
            sorted_child_list = sort_children(sorted_child_list,child_list,True)   
                       
            while len(sorted_child_list) > 0: #Need to apply all necessary condition.
                child = sorted_child_list.pop()                    
                for o in oq:
                    if child.STATE == o.STATE:
                        child.IN_OPEN = True
                    
                for e in eq:
                    if child.STATE == e.STATE:
                        child.IN_CLOSE = True    
                                
                if child.IN_OPEN == False and child.IN_CLOSE == False:
                    if node.PATH_LENGTH > 23:
                        time = node.PATH_LENGTH % 24
                    else:
                        time = node.PATH_LENGTH    
                    if time in node.OFF_PERIODS.get(child.STATE):
                        print("Pipe is Offline")
                        child.PATH_LENGTH = 0
                    else:
                        oq.append(child)
                                 
            eq.append(node)
            oq = sort_children([],oq,False)            

def sort_children(sorted_child_list,child_list,rever):
    while len(child_list) > 0:
        i = 0
        child_list.sort(key=lambda x:x.PATH_LENGTH,reverse = rever)
        if len(child_list) > 1:
            if child_list[i].PATH_LENGTH == child_list[i+1].PATH_LENGTH:
                child_list.sort(key=lambda x:x.STATE,reverse = rever)
                child1 = child_list.pop()
                child2 = child_list.pop()
                sorted_child_list.append(child1)
                sorted_child_list.append(child2)
            else:
                child = child_list.pop()
                sorted_child_list.append(child)     
        else:
            child = child_list.pop()
            sorted_child_list.append(child)       
            
    return sorted_child_list
                       
                            
def read_data(file_handler,algo_type): #This method scans input and creates source,destination nodes. Also calls construct graph method.
    source = ""
    is_source = False
    destination_nodes = ""
    destination_list = []
    is_destination = False
    intermediate_nodes = ""
    intermediate_list = []
    is_intermediate = False
    no_of_pipes = 0
    is_graph_created = False
    start_time = 0
    id = 1 
    for each_line in file_handler:
        if each_line == '\n':
            break
        else:
            if source == "" :
                source = each_line
                is_source = True
                is_destination = False
                is_intermediate = False
                source = make_node(id,source,is_source,is_destination,is_intermediate) #make node method 
            elif destination_nodes == "":
                is_source = False
                is_destination = True
                is_intermediate = False
                destination_nodes = each_line
                for dnode in destination_nodes.split(" "):
                    if "\n" in dnode:
                        dnode = dnode.rstrip("\n")
                    destination_list.append(dnode)
            elif intermediate_nodes == "":
                is_source = False
                is_destination = False
                is_intermediate = True
                intermediate_nodes = each_line
                for inode in intermediate_nodes.split(" "):
                    if "\n" in inode:
                        inode = inode.rstrip("\n")
                    intermediate_list.append(inode)
            elif no_of_pipes == 0:
                no_of_pipes = int(each_line.rstrip("\n"))
                print("No of pipes: " + str(no_of_pipes))
                if is_graph_created == False:
                    if "UCS" in algo_type:
                        graph,dest_nodes = construct_UCS_graph(file_handler,source,destination_list,intermediate_list,no_of_pipes) #UCS Construct graph
                        is_graph_created = True
                    else:
                        graph,dest_nodes = construct_graph(file_handler,source,destination_list,intermediate_list,no_of_pipes) # BFS & DFS Construct Graph
                        is_graph_created = True
            elif start_time == 0:
                each_line.rstrip("\n")
                start_time = int(each_line)           
    if source.PATH_LENGTH == 0:
        source.PATH_LENGTH = start_time
        print("Source Start Time: " + str(source.PATH_LENGTH))  
    return graph,source,dest_nodes                    

def make_node(id,node_name,is_source,is_destination,is_intermediate): 
    if is_source == True and is_destination == False and is_intermediate == False:
        node = Node()
        node.assign_values(id,node_name.rstrip('\n'),None,0,"Source",{},False,False)
        print ( "Source Node Id : " + str(node.STATE) + str(node.ID))
    elif is_source == False and is_destination == True and is_intermediate == False:
        node = Node()
        node.assign_values(id,node_name,{},0,"Destination",{},False,False)
        print ( "Destination Node Id : " + str(node.STATE) + " : " + str(node.ID))
    elif is_source == False and is_destination == False and is_intermediate == True:
        node = Node()
        node.assign_values(id,node_name,{},0,"Intermediate",{},False,False)
        print ( "Intermediate Node Id : " + str(node.STATE) + " : " + str(node.ID))  
    
    return node

def construct_graph(file_handler,source,destination_list,intermediate_list,no_of_pipes):  #constructs graph for BFS and DFS
    g = {}
    id = 1 
    dest_nodes = []
    visited = False
    Pipe_scanned = 0
    for line in file_handler:
        comp_list = [] 
        if "\n" in line:
            line.rstrip 
        for comp in line.split(" "):
            mak_node = True
            if '-' in comp:
                continue
            elif comp == source.STATE:
                if visited == False:
                    source.ID = id
                    id = id + 1
                comp_list.append(source)
                visited = True
            for node in destination_list:
                if comp == node:
                    for nkey in g.keys():
                        if node == nkey.STATE:
                            comp_list.append(nkey)
                            dest_nodes.append(nkey)
                            mak_node = False
                            break
                        else:
                            mak_node = True    
                    for vkey in g.values():
                        for key in vkey:
                            if node == key.STATE and comp_list.__contains__(key) == False:
                                comp_list.append(key)
                                dest_nodes.append(key)
                                mak_node = False
                                break 
                    if mak_node == True:
                        node = make_node(id,node,False,True,False) #make node method
                        comp_list.append(node)
                        dest_nodes.append(node)
                       
                    id = id + 1
            for node in intermediate_list:
                if comp == node:
                    for nkey in g.keys():
                        if node == nkey.STATE:
                            comp_list.append(nkey)
                            mak_node = False
                            break   
                    for vkey in g.values():
                        for key in vkey:
                            if node == key.STATE and comp_list.__contains__(key) == False:
                                comp_list.append(key)
                                mak_node = False
                                break    
                    if mak_node == True:
                        node = make_node(id,node,False,False,True) #make node method
                        comp_list.append(node)
                    id = id + 1
        
        print("Comp List Length : " + str(len(comp_list)))
        if len(comp_list) != 0:
            add_to_graph(comp_list,g)
        Pipe_scanned = Pipe_scanned + 1
        if Pipe_scanned == no_of_pipes:
            break       
    return g,dest_nodes
                    

def add_to_graph(list,graph):
    print("Add to graph method")
    print("Length of comp_list " + str(len(list)))
    if list[0] in graph.keys():
        print(list[0].STATE)
        print(list[1].STATE)
        graph[list[0]].append(list[1])
        list[1].PARENT_NODE = list[0].STATE
        print(graph.get(list[0]))
    else:
        print(list[0].STATE)
        print(list[1].STATE)
        list[1].PARENT_NODE = list[0].STATE
        graph[list[0]] = [list[1]]
        print(graph.get(list[0]))
    
def construct_UCS_graph(file_handler,source,destination_list,intermediate_list,no_of_pipes):
    g = {}
    id = 1 
    dest_nodes = []
    visited = False
    Pipe_scanned = 0
    path_time = 0
    children_list = []
    for line in file_handler:
        comp_list = [] 
        off_period = []
        dummy = line.split(" ")
        path_time = int(dummy[2])
        if "\n" in line:
            line.rstrip("\n") 
        for comp in line.split(" "):
            mak_node = True
            if '-' in comp:
                result = []
                a,b = comp.split('-')
                a,b = int(a),int(b)
                result.extend(range(a,b+1))
                for res in result:
                    off_period.append(res)
                
            if comp == source.STATE:
                if visited == False:
                    source.ID = id
                    id = id + 1
                comp_list.append(source)
                visited = True
                
            for node in destination_list:
                if comp == node:
                    for nkey in g.keys():
                        if node == nkey.STATE:
                            comp_list.append(nkey)
                            dest_nodes.append(nkey)
                            mak_node = False
                            break
                        else:
                            mak_node = True    
                    for vkey in g.values():
                        for key in vkey:
                            if node == key.STATE and comp_list.__contains__(key) == False:
                                comp_list.append(key)
                                dest_nodes.append(key)
                                mak_node = False
                                break 
                    if mak_node == True:
                        node = make_node(id,node,False,True,False) #make node method
                        comp_list.append(node)
                        dest_nodes.append(node)
                    id = id + 1
                            
            for node in intermediate_list:
                if comp == node:
                    for nkey in g.keys():
                        if node == nkey.STATE:
                            comp_list.append(nkey)
                            mak_node = False
                            break   
                    for vkey in g.values():
                        for key in vkey:
                            if node == key.STATE and comp_list.__contains__(key) == False:
                                comp_list.append(key)
                                mak_node = False
                                break    
                    if mak_node == True:
                        node = make_node(id,node,False,False,True) #make node method
                        comp_list.append(node)
                    id = id + 1             
                    
        if len(comp_list) != 0:
            add_to_ucs_graph(comp_list,g,off_period,path_time,children_list)
        Pipe_scanned = Pipe_scanned + 1
        if Pipe_scanned == no_of_pipes:
            break   
    return g,dest_nodes
                
def add_to_ucs_graph(clist,graph,off_period,path_time,children_list):
    print("Add to UCS graph method")
    if clist[0] in graph.keys():
        print(clist[0].STATE)
        print(clist[1].STATE)
        if clist[1] not in children_list:
            children_list.append(clist[1])
        graph[clist[0]].append(clist[1])
        clist[1].PATH_LENGTH = 0
        for val in children_list:
            if clist[1].STATE == val.STATE:
                clist[1].PARENT_NODE.update({clist[0].STATE:path_time})
                clist[0].OFF_PERIODS.update({clist[1].STATE:off_period})
            
    else:
        print(clist[0].STATE)
        print(clist[1].STATE)
        if clist[1] not in children_list:
            children_list.append(clist[1])
        graph[clist[0]] = [clist[1]]
        clist[1].PATH_LENGTH = 0 
        for val in children_list:
            if clist[1].STATE == val.STATE:
                clist[1].PARENT_NODE.update({clist[0].STATE:path_time})
                clist[0].OFF_PERIODS.update({clist[1].STATE:off_period})
            #else:
                #list[1].PARENT_NODE = {list[0].STATE:path_time}
                #list[1].OFF_PERIODS = {list[0]:off_period}
    
file_handler = open("sampleInput.txt")
read_write_file(file_handler)
file_handler.close()
