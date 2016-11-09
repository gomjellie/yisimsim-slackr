
class singletone(type):
    def get_instance(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance=super(singletone,cls).__call__(*args,**kwargs)
            return cls.__instance
