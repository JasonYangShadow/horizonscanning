from enum import Enum

class Type(Enum):
    ValueException = 0
    NoneException = 1
    MissMatchException= 2
    UnknownException = 3
    WrongTypeException = 4
    FullException = 5

class TeleException(Exception):
    def __init__(self,type,msg):
        if isinstance(type, Type):
            self.__type=type
            self.__msg=msg
        else:
            raise TeleException(Type.WrongTypeException,'type should be instance of Type class') 

    def __str__(self):
        return '[Exception:'+Type(self.__type.value).name+'][Exception Msg:'+self.__msg+']'
