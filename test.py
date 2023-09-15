class Parent:
    __a=None

    @classmethod
    def get_a(cls) -> None:
        return cls.__a
    @classmethod
    def set_a(cls,value) -> None:
        cls.__a=value
        print("set")

if __name__ == "__main__":
    Parent.set_a(5)
    print(Parent.get_a())
