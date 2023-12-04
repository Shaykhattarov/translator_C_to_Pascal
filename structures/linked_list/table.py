from structures.linked_list import TableNode


class Table:
    def __init__(self) -> None:
        self.head: TableNode = None

    def contains(self, value: dict):
        lastnode = self.head
        while (lastnode):
          if value.keys == lastnode.value.keys:
            return True
          else:
            lastnode = lastnode.nextnode
        return False
    
    def put(self, value: dict):
        newnode = TableNode(value)
        if self.head is None:
            self.head = newnode
            return
        lastnode = self.head
        while lastnode.nextnode:
           lastnode = lastnode.nextnode
        lastnode.nextnode = newnode

    def remove(self, rmnode: dict):
        headnode = self.head
        if headnode is not None:
            if headnode.value.keys == rmnode.keys:
                self.head = headnode.nextnode
                headnode = None
                return 
        while headnode is not None:
            if headnode.value.keys == rmnode.keys:
                break
            
            lastnode = headnode
            headnode = headnode.nextnode
        if headnode == None:
            return 
        lastnode.nextnode = headnode.nextnode
        headnode = None
