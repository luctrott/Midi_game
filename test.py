class Parent:
    def __init__(self):
        pass
        self.t=self._call

    def _call(self):
        print("Parent")
    
    def call(self):
        self._call()
    
class Child(Parent):
    def __init__(self):
        super().__init__()
    
    def _call(self):
        super()._call()
        print("Child")
    

if __name__ == '__main__':
    c=Child()
    c.call()
    print("Done")