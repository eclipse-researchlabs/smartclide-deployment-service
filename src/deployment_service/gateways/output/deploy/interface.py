
class BuildInterface(type):
    """A Build metaclass that will be used for CI build engine class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'deploy') and 
                callable(subclass.build) and 
                hasattr(subclass, 'get_deployment') and 
                callable(subclass.get_build) and
                hasattr(subclass, 'delete_deployment') and 
                callable(subclass.list_builds))