class ActivatedID():
     activated_id = {}
     def is_activated(usr_id):
         if ActivatedID.activated_id.get(usr_id) == True:
             return True
         else:
             return False
     def activate(usr_id):
         ActivatedID.activated_id[usr_id] = True
     def deactivate(usr_id):
         del ActivatedID.activated_id[usr_id]
