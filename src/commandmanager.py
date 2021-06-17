from collections import deque 

class CommandManager():
    def __init__(self, max=100) -> None:
        self.undo_list = deque([])
        self.redo_list = deque([])
        self.max_undo = max
        self.max_redo = max

    def do(self, obj, do_method, do_param, undo_method=False, undo_param=None, 
            desc='command without description', execute=True, do_kwargs={}, undo_kwargs={}):
        cmd = Command()
        cmd.obj = obj
        cmd.desc = desc
        cmd.redo_method = do_method
        cmd.redo_param = do_param
        if undo_method:
            cmd.undo_method = undo_method
        else:
            cmd.undo_method = do_method + '_undo'
        if undo_kwargs:
            cmd.undo_kwargs = undo_kwargs
        else:
            cmd.undo_kwargs = do_kwargs
        cmd.redo_kwargs = do_kwargs            
        if undo_param: cmd.undo_param = undo_param
        else: cmd.undo_param = []
        self.undo_list.append(cmd)
        self.redo_list = deque([])
        if len(self.undo_list) > self.max_undo:
            self.undo_list.pop_left()
        if execute:
            getattr(obj, do_method)(*do_param, **do_kwargs)

    def undo(self):
        if len(self.undo_list) > 0:
            cmd = self.undo_list.pop()
            self.redo_list.append(cmd)
            if len(self.redo_list) > self.max_redo:
                self.redo_list.popleft()
            getattr(cmd.obj, cmd.undo_method)(*cmd.undo_param, **cmd.undo_kwargs)
            return 'Undo ' + cmd.desc + ' done'
        else: return 'Nothing to undo'

    def redo(self):
        if len(self.redo_list) > 0:
            cmd = self.redo_list.pop()
            self.undo_list.append(cmd)
            if len(self.undo_list) > self.max_undo:
                self.undo_list.popleft()
            getattr(cmd.obj, cmd.redo_method, 'not found')(*cmd.redo_param, **cmd.redo_kwargs)
            return 'Redo ' + cmd.desc + ' done'
        else: return 'Nothing to redo'
        
class Command():
    def __init__(self) -> None:
        pass