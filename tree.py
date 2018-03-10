class node(object):
    def __init__(self,key,val=0,left=None,right=None,parent=None):
        self.key=key
        self.val=val
        self.left=left
        self.right=right
        self.parent=parent
    def hasleft(self):
        return self.left
    def hasright(self):
        return self.right
    def setval(self,val):
        self.val=val
    def setleft(self,left):
        self.left=left
    def setright(self,right):
        self.right=right
    def show(self):
        if not self.left==None :
            self.left.show()
        print('key=',self.key,'value=',self.val)
        if not self.right==None :
            self.right.show()
class tree(object):
    def __init__(self):
        self.root=None
        self.size=0
    def length(self):
        return self.size
    def put(self,key,val=0):
        if self.root :
            self._put(self.root,key,val)
        else:
            self.root=node(key,val)
    def _put(self,cur,key,val):
        if key<cur.key :
            if cur.hasleft() :
                self._put(cur.left,key,val)
            else :
                cur.setleft(node(key,val))
                self.size+=1
        elif key==cur.key :
            cur.setval(val)
        else :
            if cur.hasright() :
                self._put(cur.right,key,val)
            else :
                cur.setright(node(key,val))
                self.size+=1
    def __setitem__(self, key, val):
        self.put(key,val)
    def show(self):
        print('size of tree =',self.size)
        self.findmin()
        self.findmax()
        self.root.show()
    def get(self,key):
        if self.root==None :
            print('empty tree')
            return
        self._get(self.root,key)
    def _get(self,cur,key):
        if key<cur.key :
            if cur.hasleft() :
                self._get(cur.left,key)
            else :
                print('Not exist')
                return
        elif key==cur.key :
            print('key=',cur.key,'value=',cur.val)
            return
        else :
            if cur.hasright() :
                self._get(cur.right,key)
            else :
                print('Not exist')
                return
    def findmin(self):
        if self.root==None :
            print('empty tree')
            return
        self._findmin(self.root)
    def _findmin(self,cur):
        if cur.hasleft() :
            self._findmin(cur.left)
        else :
            print('min:key=',cur.key,'value=',cur.val)
    def findmax(self):
        if self.root==None :
            print('empty tree')
            return
        self._findmax(self.root)
    def _findmax(self,cur):
        if cur.hasright() :
            self._findmax(cur.right)
        else :
            print('max:key=',cur.key,'value=',cur.val)