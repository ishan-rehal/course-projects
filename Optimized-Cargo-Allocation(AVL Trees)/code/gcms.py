from bin import Bin
from avl import AVLTree
from avl import compare_by_size
from avl import compare_by_bin_ID
from avl import compare_by_ObjID
from avl import compare_by_capacity
from bin import Bin_ID_Group
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.bins = AVLTree(compare_by_capacity)
        self.objects = AVLTree(compare_by_ObjID)
        self.bins_ID = AVLTree(compare_by_bin_ID)
        pass 

    def add_bin(self, bin_id, capacity):
        temp_binidgroup = Bin_ID_Group(capacity)
        search_binidgroup = self.bins.search(temp_binidgroup)
        if(search_binidgroup==None):
            temp_bin = Bin(bin_id,capacity)
            temp_binidgroup.group_of_bins.insert(temp_bin)
            self.bins_ID.insert(temp_bin)
            self.bins.insert(temp_binidgroup)
        else:
            temp_bin = Bin(bin_id,capacity)
            search_binidgroup.group_of_bins.insert(temp_bin)
            self.bins_ID.insert(temp_bin)
        pass
    

    def add_object(self, object_id, size, color):
        if(color==Color.BLUE):
            temp_key = Bin_ID_Group(size)
            temp_bin_id_group = self.bins.get_least_greater_or_equal(temp_key) #Choosing group of bin
            if(temp_bin_id_group is None):
                raise NoBinFoundException
            if(temp_bin_id_group.capacity>=size):
                temp_bin = temp_bin_id_group.group_of_bins.get_min_value()
                temp_bin_id_group.group_of_bins.delete(temp_bin)
                self.bins_ID.delete(temp_bin)
                obj = Object(object_id,size,color)
                # obj.parent_bin = temp_bin 
                temp_bin.add_object(obj)
                self.objects.insert(obj)
                
                new_bin_id_group_temp = Bin_ID_Group(temp_bin.capacity)
                new_bin_id_group =  self.bins.search(new_bin_id_group_temp)
                if(new_bin_id_group):
                    new_bin_id_group.add_bin(temp_bin)
                    self.bins_ID.insert(temp_bin)
                else:
                    insert_bin_id_group = Bin_ID_Group(temp_bin.capacity)
                    insert_bin_id_group.group_of_bins.insert(temp_bin)
                    self.bins_ID.insert(temp_bin)
                    self.bins.insert(insert_bin_id_group)
                    #Searching for added bin to add object
                
                if(temp_bin_id_group.group_of_bins.root == None):
                    self.bins.delete(temp_bin_id_group)
                        
            else:
                raise NoBinFoundException
            
        elif(color==Color.YELLOW):
            temp_key = Bin_ID_Group(size)
            temp_bin_id_group = self.bins.get_least_greater_or_equal(temp_key) #Choosing group of bin
            if(temp_bin_id_group is None):
                raise NoBinFoundException
            if(temp_bin_id_group.capacity>=size):
                temp_bin = temp_bin_id_group.group_of_bins.get_max_value()
                temp_bin_id_group.group_of_bins.delete(temp_bin)
                self.bins_ID.delete(temp_bin)
                obj = Object(object_id,size,color)
                # obj.parent_bin = temp_bin 
                temp_bin.add_object(obj)
                self.objects.insert(obj)
                
                new_bin_id_group_temp = Bin_ID_Group(temp_bin.capacity)
                new_bin_id_group =  self.bins.search(new_bin_id_group_temp)
                if(new_bin_id_group):
                    new_bin_id_group.add_bin(temp_bin)
                    self.bins_ID.insert(temp_bin)
                else:
                    insert_bin_id_group = Bin_ID_Group(temp_bin.capacity)
                    insert_bin_id_group.group_of_bins.insert(temp_bin)
                    self.bins_ID.insert(temp_bin)
                    self.bins.insert(insert_bin_id_group)
                    #Searching for added bin to add object
                
                if(temp_bin_id_group.group_of_bins.root == None):
                    self.bins.delete(temp_bin_id_group)
                        
            else:
                raise NoBinFoundException
        
        elif(color==Color.RED):
            temp_key = Bin_ID_Group(size)
            temp_bin_id_group = self.bins.get_max_value() #Choosing group of bin
            if(temp_bin_id_group is None):
                raise NoBinFoundException
            if(temp_bin_id_group.capacity>=size):  #Checking if required size is present
                temp_bin = temp_bin_id_group.group_of_bins.get_min_value() #Finiding bin acc to algo
                temp_bin_id_group.group_of_bins.delete(temp_bin)
                self.bins_ID.delete(temp_bin)
                obj = Object(object_id,size,color)
                # obj.parent_bin = temp_bin 
                temp_bin.add_object(obj)
                self.objects.insert(obj)
                
                new_bin_id_group_temp = Bin_ID_Group(temp_bin.capacity)
                new_bin_id_group =  self.bins.search(new_bin_id_group_temp)
                if(new_bin_id_group):
                    new_bin_id_group.add_bin(temp_bin)
                    self.bins_ID.insert(temp_bin)
                else:
                    insert_bin_id_group = Bin_ID_Group(temp_bin.capacity)
                    insert_bin_id_group.group_of_bins.insert(temp_bin)
                    self.bins_ID.insert(temp_bin)
                    self.bins.insert(insert_bin_id_group)
                    #Searching for added bin to add object
                
                if(temp_bin_id_group.group_of_bins.root == None):
                    self.bins.delete(temp_bin_id_group)
                        
            else:
                raise NoBinFoundException
                
        elif(color==Color.GREEN):
            temp_key = Bin_ID_Group(size)
            temp_bin_id_group = self.bins.get_max_value() #Choosing group of bin
            if(temp_bin_id_group is None):
                raise NoBinFoundException
            if(temp_bin_id_group.capacity>=size):
                temp_bin = temp_bin_id_group.group_of_bins.get_max_value()
                temp_bin_id_group.group_of_bins.delete(temp_bin)
                self.bins_ID.delete(temp_bin)
                obj = Object(object_id,size,color)
                # obj.parent_bin = temp_bin 
                temp_bin.add_object(obj)
                self.objects.insert(obj)
                
                new_bin_id_group_temp = Bin_ID_Group(temp_bin.capacity)
                new_bin_id_group =  self.bins.search(new_bin_id_group_temp)
                if(new_bin_id_group):
                    new_bin_id_group.add_bin(temp_bin)
                    self.bins_ID.insert(temp_bin)
                else:
                    insert_bin_id_group = Bin_ID_Group(temp_bin.capacity)
                    insert_bin_id_group.group_of_bins.insert(temp_bin)
                    self.bins_ID.insert(temp_bin)
                    self.bins.insert(insert_bin_id_group)
                    #Searching for added bin to add object
                
                if(temp_bin_id_group.group_of_bins.root == None):
                    self.bins.delete(temp_bin_id_group)
                        
            else:
                raise NoBinFoundException
                    
                    

    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin
        temp_obj = Object(object_id,0,0)
        search_obj = self.objects.search(temp_obj)
        if(search_obj is None):
            return None
        
        temp_bin = search_obj.parent
        #delete bin from orignial bin group as size will be changed
        search_bin_id_group_temp = Bin_ID_Group(temp_bin.capacity)
        search_bin_id_group = self.bins.search(search_bin_id_group_temp)
        search_bin_id_group.group_of_bins.delete(temp_bin)
        self.bins_ID.delete(temp_bin)
        
        temp_bin.remove_object(search_obj.object_id)
        #Size of bin is changed
        
        new_bin_id_group_temp = Bin_ID_Group(temp_bin.capacity)
        new_bin_id_group =  self.bins.search(new_bin_id_group_temp)
        if(new_bin_id_group):
            new_bin_id_group.add_bin(temp_bin)
            self.bins_ID.insert(temp_bin)
        else:
            insert_bin_id_group = Bin_ID_Group(temp_bin.capacity)
            insert_bin_id_group.group_of_bins.insert(temp_bin)
            self.bins_ID.insert(temp_bin)
            self.bins.insert(insert_bin_id_group)
            #Searching for added bin to add object
        
        if(search_bin_id_group.group_of_bins.root == None):
            self.bins.delete(search_bin_id_group)


        self.objects.delete(search_obj)
        
        
        
        pass

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        search_bin_temp = Bin(bin_id,0)
        search_bin = self.bins_ID.search(search_bin_temp)
        bin_capacity = search_bin.capacity
        inorder_objects = search_bin.objects.in_order_traversal()
        ans = []
        for object in inorder_objects:
            ans.append(object.object_id)
        return (bin_capacity,ans)
        pass

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        temp_obj = Object(object_id,0,0)
        search_obj = self.objects.search(temp_obj)
        if(search_obj is None):
            return None
        
        temp_bin = search_obj.parent
        return temp_bin.bin_id
        pass
    
if __name__ == "__main__":
    gcms = GCMS()
    # gcms.add_bin(12,50)
    # gcms.add_bin(13,50)
    # gcms.add_object(20,25,4)
    # gcms.add_object(21,25,2)
    # # gcms.delete_object(20)
    # gcms.add_object(20,25,3)
    # # gcms.delete_object(21)
    
    # temp = Bin_ID_Group(25)
    # gcms.bins.search(temp).group_of_bins.print_tree()
    
    # gcms.bins.print_bfs_triangle()  
    # objects = gcms.objects.in_order_traversal()
    # for object in objects:
    #     print(object.object_id)  
    gcms.add_bin(1234, 10)
    gcms.add_bin(4321, 20)
    gcms.add_bin(1111, 15)
    gcms.add_object(8989, 6, Color.RED )
    gcms.add_object(2892, 8, Color.RED )
    gcms.add_object(4839, 9, Color.RED )
    gcms.add_object(3283, 2, Color.RED )
    gcms.add_object(8983, 8, Color.RED )
    print(gcms.bin_info(1234))
    print(gcms.bin_info(4321))
    print(gcms.bin_info(1111))

