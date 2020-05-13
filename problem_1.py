class Node:
    '''
    Node class is used to encapsulate a key and a value.
    '''

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class Doubly_linked_list:
    '''
    This double linked list tracks the usage order of the cache.

    Attributes:
    head: Start of the list. The head is the most recent key accessed.
    tail: End of the list. THe tail is the least recently key accessed.
    '''

    def __init__(self):
        self.head = None
        self.tail = None

    def get_tail_key(self):
        return self.tail.key

    def get_head_key(self):
        return self.head.key

    def insert_new_node(self, new_node):
        '''
        This function take a new_node and places the node in front of the list.
        '''
        # linked list is empty
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        # insert at head
        self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

    def move_node_to_front(self, node):
        '''
        Takes a recently accessed node and places it at the front of the list.
        '''
        # Node is already at front
        if node.key == self.head.key:
            return
        # node is at tail
        if node.next is None:
            # set node prev to None to make then make it the new tail
            node.prev.next = None
            self.tail = node.prev
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

            # set node next to head
            node.next = self.head
            # set head to prev to node
            self.head.prev = node
            node.prev = None
            self.head = node

    def remove_least_recent_node(self):
        node_to_delete = self.tail
        self.tail = node_to_delete.prev
        self.tail.next = None
        node_to_delete.next = None
        node_to_delete.prev = None


class LRU_Cache(object):
    '''
    Attributes:
    capacity: max size of the cache
    usage_order: doubly_linked_list to keep track of access order.
    storage: dictionary to retrieve the values associated to a key
    '''

    def __init__(self, capacity):
        # Initialize class variables
        if capacity <= 0:
            raise ValueError("Cache size should be greater than 0")
        self.capacity = capacity
        self.usage_order = Doubly_linked_list()
        self.storage = dict()

    def get(self, key):
        # Retrieve item from provided key. Return -1 if nonexistent.
        node = self.storage.get(key)

        if node is None:
            return -1

        self.usage_order.move_node_to_front(node)
        return node.value

    def set(self, key, value):
        # Set the value if the key is not present in the cache. If the cache is at capacity remove the oldest item.
        node = self.storage.get(key)

        if node:
            node.value = value
            # update recently_used list
            self.usage_order.move_node_to_front(node)
            return

            # Node not in list
            # Remove least recently used if full
        if len(self.storage) == self.capacity:
            tail_key = self.usage_order.get_tail_key()
            self.usage_order.remove_least_recent_node()
            del self.storage[tail_key]

            # add new node
        new_node = Node(key, value)
        self.storage[key] = new_node
        self.usage_order.insert_new_node(new_node)


# Test case 1
our_cache = LRU_Cache(5)

our_cache.set(1, 1)
our_cache.set(2, 2)
our_cache.set(3, 3)
our_cache.set(4, 4)


print(our_cache.get(1))
# return 1      
print(our_cache.get(2))       
# returns 2
print(our_cache.get(9))       
# returns -1 because 9 is not present in the cache

our_cache.set(5, 5)
our_cache.set(6, 6)

print(our_cache.get(3))      
# returns -1 because the cache reached it's capacity and 3 was the least recently used entry
print(our_cache.storage.keys())

print("----------------Test Case 2-----------")

# Test case 2
# Case where same key is being set in the cache.
# Occurs after the cache is full. Key of 3 is set again.
# Four should removed
our_cache = LRU_Cache(5)

our_cache.set(1, 1)
our_cache.set(2, 2)
our_cache.set(3, 3)
our_cache.set(4, 4)

our_cache.get(1)      
our_cache.get(2)       #
our_cache.get(9)       

our_cache.set(5, 5)           # Cache is full 
our_cache.set(3, 3)           # Three is set again
our_cache.set(6, 6)           
# Here four should be removed
print(our_cache.get(4))
# -1 should be printed  
print(our_cache.storage.keys()) 

print("----------------Test Case 3-----------")
# Test case 3
# Case where cache size is 0
our_cache = LRU_Cache(0)
# Should raise a ValueError