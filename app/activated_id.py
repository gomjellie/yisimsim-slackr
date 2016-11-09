from app.singletone import singletone

class ActivatedID(metaclass=singletone):
     def __init__(self):
        self.activated_id = {}
     def is_activated(self,usr_id):
         if self.activated_id.get(usr_id) == True:
             return True
         else:
             return False
     def activate(self,usr_id):
         self.activated_id[usr_id] = True
     def deactivate(self,usr_id):
         del self.activated_id[usr_id]
