#!/usr/bin/env python

import random
DEBUG = True
LEN = 1000

# TODO - not generic, just works for numbers
class TreapNode:
    def __init__(self, data, parent):
        # assign a random priority
        self.priority = random.random()
        self.data = data
        self.parent = parent
        self.left = None
        self.right = None

    def height(self):
        if self.left == None and self.right == None:
            return 1
        elif self.left == None and self.right:
            return self.right.height() + 1
        elif self.left and self.right == None:
            return self.left.height() + 1
        else:
            return max(self.left.height(), self.right.height()) + 1

    def checker(self):
        if DEBUG:
            # ensures the in order properties of the entire tree
            # and max-heap properties
            if (self.left):
                assert(self.left.data < self.data)
                assert(self.left.priority < self.priority)
                # check grandchildren
                left = self.left
                if (left.left):
                    assert(left.left.data < self.data)
                    assert(left.left.priority < self.priority)
                if (left.right):
                    assert(left.right.data < self.data)
                    assert(left.right.priority < self.priority)

                self.left.checker()
            if (self.right):
                assert(self.right.data > self.data)
                assert(self.right.priority < self.priority)
                # check grandchildren
                right = self.right
                if (right.left):
                    assert(right.left.data > self.data)
                    assert(right.left.priority < self.priority)
                if (right.right):
                    assert(right.right.data > self.data)
                    assert(right.right.priority < self.priority)
                self.right.checker()

    def __replace_child(self, child, new_child):
        if (new_child):
            new_child.parent = self
        if (self.left == child):
            self.left = new_child
        elif (self.right == child):
            self.right = new_child
        else:
            import pdb; pdb.set_trace()
            assert(False)
            
    ## based on https://en.wikipedia.org/wiki/Tree_rotation
    
    # rotation about P
    # rotate left
    def __rotate_left(self):
        assert(self.right != None)
        curr_parent = self.parent

        # replace child of curr_parent with Q
        if (curr_parent):
            curr_parent.__replace_child(self, self.right)
        else:
            self.right.parent = None

        # store Q's left, B
        b = self.right.left 

        # Q's left should point to P
        self.right.left = self
        self.parent = self.right

        # P(self)'s right should point to B
        self.right = b
        if b:
            b.parent = self

    # rotation about Q
    # rotate right
    def __rotate_right(self):
        assert(self.left != None)
        curr_parent = self.parent

        # replace child with P
        if (curr_parent):
            curr_parent.__replace_child(self, self.left)
        else:
            self.left.parent = None

        # store P's right child
        b = self.left.right

        # replaqce P's right child with self
        self.left.right = self
        self.parent = self.left

        # replace self.left to b
        self.left = b
        if b:
            b.parent = self
    
    # rotates the parent for add
    def rotate_parent(self):
        parent = self.parent
        if (self.parent.left == self):
            parent.__rotate_right()
        else:
            parent.__rotate_left()
        
    # add
    # assumes all data are unique
    def add_h(self, data, root):
        if self.data > data:
            if self.left:
                # recursively find the inorder position
                return self.left.add_h(data, root)
            else:
                # create a new node at that posiiton
                n = TreapNode(data, self)
                self.left = n
                
                 # we rotate until we are root or we are less than parent's priority
                while n.parent != None and (n.parent.priority < n.priority):
                    n.rotate_parent()
                
                if n.parent == None:
                    return n
                else:
                    return root
        elif self.data < data:
            if self.right:
                return self.right.add_h(data, root)
            else:
                # create a new node at that posiiton
                n = TreapNode(data, self)
                self.right = n

                # we rotate until we are root or we are less than parent's priority
                while n.parent != None and (n.parent.priority < n.priority):
                    n.rotate_parent()
                
                if n.parent == None:
                    return n
                else:
                    return root
        else:
            assert(False)


    def add(self, data):
        return self.add_h(data, self)
        
    

    # delete, needs to return the new root
    def delete(self, data):
        croot = self
        def delete_h(curr, data, root):
            # find the thing
            if data == curr.data:
                is_root = curr == root
                has_rooted = False
                # actually delete the thing
                while not (curr.left == None and curr.right == None):
                    if (curr.right and curr.left):
                        # pick the one with the highest priority
                        if (curr.right.priority > curr.left.priority):
                            curr.__rotate_left()
                        else:
                            curr.__rotate_right()
                    elif curr.right:
                        curr.__rotate_left()
                    else:
                        curr.__rotate_right()
                    if is_root and not has_rooted:
                        root = curr.parent
                        has_rooted = True
                    curr.checker()
                # i am a leaf, just kill me
                parent = curr.parent
                curr.parent.__replace_child(curr, None)
                parent.checker()
                return root
            else:
                if curr.data > data and curr.left:
                    return delete_h(curr.left, data, root)
                elif curr.data < data and curr.right:
                    return delete_h(curr.right, data, root)
                else:
                    assert(False)
        return delete_h(self, data, croot)

    # lookup (membership)
    def lookup(self, data):
        if data == self.data:
            return True
        else:
            if self.data > data and self.left:
                return self.left.lookup(data)
            elif self.data < data and self.right:
                return self.right.lookup(data)
            else:
                return False

    
if __name__=="__main__":
    test = range(LEN)
    #random.shuffle(test)
    
    root = TreapNode(test[0], None)
    root.checker()

    for i in test[1:]:
        #print("[+] Adding %d" % i)
        root = root.add(i)
        root.checker()
    for i in test:
        assert(root.lookup(i))
        root.checker()

    print(root.height())

    random.shuffle(test)

    for i in test[:LEN - 1]:
        root = root.delete(i)
        root.checker()

    print("[+] All tests passed")
        