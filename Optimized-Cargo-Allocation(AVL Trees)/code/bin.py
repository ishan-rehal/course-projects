from avl import AVLTree
from avl import compare_by_ObjID
from avl import compare_by_bin_ID
from object import Object
class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.objects = AVLTree(compare_by_ObjID)
        
    def add_object(self, object):
        # Implement logic to add an object to this bin
        self.objects.insert(object)
        self.capacity -= object.size
        object.parent = self
        pass

    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        temp_object = Object(object_id,0,0)
        search_object = self.objects.search(temp_object)
        self.objects.delete(search_object)
        self.capacity += search_object.size
        pass
    
    def value(self):
        return self.bin_id
    
class Bin_ID_Group:
    def __init__(self,capacity):
        self.group_of_bins = AVLTree(compare_by_bin_ID)
        self.capacity = capacity
        
    def add_bin(self,bin):
        self.group_of_bins.insert(bin)
        pass
    
    def remove_bin(self,bin_id):
        temp_bin = Bin(bin_id,0)
        search_bin = self.group_of_bins.search(temp_bin)
        self.group_of_bins.delete(search_bin)
        
    def value(self):
        return self.capacity