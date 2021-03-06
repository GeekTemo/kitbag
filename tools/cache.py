#-*- coding:utf-8 -*-
__author__ = 'gongxingfa'


class Node(object):
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoubleLinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def add_node(self, cls, data):
        return self.insert_node(cls, data, self.tail, None)

    def insert_node(self, cls, data, prev, next):
        node = cls(data)
        node.prev = prev
        node.next = next
        node.data = data
        if prev:
            prev.next = node
        if next:
            next.prev = next
        if not self.head or next is self.head:
            self.head = node
        if not self.tail or prev is self.tail:
            self.tail = node
        self.count += 1
        return node

    def remove_node(self, node):
        if node is self.tail:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        if node is self.head:
            self.head = node.next
        else:
            node.prev.next = node.next
        self.count -= 1

    def get_nodes_data(self):
        data = []
        node = self.head
        while node:
            data.append(node.data)
            node = node.next
        return data


class FreqNode(DoubleLinkedList, Node):
    def __init__(self, data):
        DoubleLinkedList.__init__(self)
        Node.__init__(self, data)

    def add_item_node(self, data):
        node = self.add_node(ItemNode, data)
        node.parent = self
        return node

    def insert_item_node(self, data, prev, next):
        node = self.insert_node(ItemNode, data, prev, next)
        node.parent = self
        return node

    def remove_item_node(self, node):
        self.remove_node(node)


class ItemNode(Node):
    def __init__(self, data):
        Node.__init__(self, data)
        self.parent = None


class LfuItem(object):
    def __init__(self, data, parent, node):
        self.data = data
        self.parent = parent
        self.node = node


class Cache(DoubleLinkedList):
    def __init__(self):
        DoubleLinkedList.__init__(self)
        self.items = dict()

    def insert_freq_node(self, data, prev, next):
        return self.insert_node(FreqNode, data, prev, next)

    def remove_freq_node(self, node):
        self.remove_node(node)


    def insert(self, key, value):
        if key in self.items:
            raise DuplicateException('Key exists')
        freq_node = self.head
        if not freq_node or freq_node.data != 1:
            freq_node = self.insert_freq_node(1, None, freq_node)

        item_node = freq_node.add_item_node(key)
        self.items[key] = LfuItem(value, freq_node, item_node)

    def access(self, key):
        try:
            tmp = self.items[key]
        except KeyError:
            raise NotFoundException('Key not found')
        freq_node = tmp.parent
        next_freq_node = freq_node.next

        if not next_freq_node or next_freq_node.data != freq_node.data + 1:
            next_freq_node = self.insert_freq_node(freq_node.data + 1, freq_node, next_freq_node)
        item_node = next_freq_node.add_item_node(key)
        tmp.parent = next_freq_node

        freq_node.remove_item_node(tmp.node)
        if freq_node.count == 0:
            self.remove_freq_node(freq_node)
        tmp.node = item_node
        return tmp.data

    def delete_lfu(self):
        if not self.head:
            raise NotFoundException('No frequency nodes found')
        freq_node = self.head
        item_node = freq_node.head
        del self.items[item_node.data]
        freq_node.remove_item_node(item_node)
        if freq_node.count == 0:
            self.remove_freq_node(freq_node)

    def put(self, key, value):
        if key in self.items:
            self.items[key].data = value
            self.access(key)
        else:
            self.insert(key, value)

    def get(self, key):
        if key in self.items:
            self.access(key)
            return self.items[key].data
        else:
            raise NotFoundException('Key not found')



cache = Cache()
cache.insert('key1', 'value1')
print cache.get('key1')
cache.insert('key2', 'value2')
cache.put('key1', 'value1_1')
print cache.get('key1')



