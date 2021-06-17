from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy.clock import Clock
from appkit.src.cursor import HoverCursor

class ColSplitter(Splitter, HoverCursor):
    def __init__(self, col_index=None, size_limit={'min':0, 'max':10000000}, app_cursor=None, **kwargs) -> None:
        super().__init__(cursor_type='size_we', app_cursor=app_cursor, edge_right=self.strip_size, **kwargs)
        self.size_hint = (None, 1)
        self.col_index = col_index
        self.previous_size = self.size[0]
        self.min_size = size_limit['min']
        self.max_size = size_limit['max']
    
    def on_size(self, instance, value):
        if self.parent.build_complete and not self.parent.adjusting:
            self.parent.adjusting = True 
            self.size[0] = clamp(self.size[0], self.size_limit['min'], self.size_limit['max'])
            self.parent.balance_col_size(self)
            self.parent.check_col_limits3()
            self.previous_size = self.size[0]
            self.parent.set_size_props()
            self.parent.adjusting = False

class RowSplitter(Splitter, HoverCursor):
    def __init__(self, grid=None, col_index=None, row_index=None,
                size_limit={'min':0, 'max':10000000}, app_cursor=None, **kwargs) -> None:
        super().__init__(cursor_type='size_ns', app_cursor=app_cursor, edge_bottom=self.strip_size, **kwargs)
        self.size_hint = (1, None)
        self.row_index = row_index
        self.col_index = col_index
        self.previous_size = self.size[1]
        self.grid = grid
        self.min_size = size_limit['min'][1] + self.strip_size
        self.max_size = size_limit['max'][1] + self.strip_size

    def on_size(self, instance, value):
        if self.grid.build_complete:
            if not self.grid.adjusting:
                self.size[1] = clamp(self.size[1], self.min_size, self.max_size)
                self.grid.balance_row_size(self)
                self.grid.check_row_limits(self)
                self.previous_size = self.size[1]
                self.grid.set_size_props()
                self.grid.adjusting = False

class GridContent():
    def __init__(self, size_limit = {'min':[20,20], 'max':[10000000, 10000000]}, **kwargs) -> None:
        self.size_limit = size_limit
        super().__init__(**kwargs)

class EmptyPane(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_limit = {'min':[10, 10], 'max': [3000,3000]} # [10,10]

class ResizeableGrid(BoxLayout):
    # Grid of resizeable columns, each split into resizeable rows
    # pane_contents is indexed as [col][row]
    # kwarg contents is list of columns
    # Columns must be list of contents
    # Content of each pane may be GridContent or None
    # pane content widget must have an attribute size_limit, of format size_limit = {'min':[50, 50], 'max': [20000,10000]

    def __init__(self, contents=[[]], strip_size=10, hide_empty_panes=True, app_cursor=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1,1)
        self.hide_empty_panes = hide_empty_panes
        self.contents = contents
        max_num_rows = max([len(col) for col in contents])
        self.panes = [[None for i in range(max_num_rows)] for j in range(len(contents))]
        self.columns = [None] * len(contents)
        self.strip_size = strip_size
        self.min_empty_pane_size = [10,10]
        self.adjusting = False
        self.build_complete = False
        Clock.schedule_once(lambda dt: self.build_grid())
        self.app_cursor = app_cursor

    def on_size(self, widget, value):
        if self.build_complete:
            self.adjusting = True
            self.new_check_sizes()
            self.set_size_props()
            Clock.schedule_once(lambda dt: setattr(self, 'adjusting', False))

    def new_check_sizes(self):
        if self.build_complete:
            for i, col in enumerate(self.columns):
                if i < self.display_cols - 1:
                    self.adjusting = True
                    col.split.size[0] = clamp(self.size[0]*col.width_prop, col.min_size, col.max_size)
                    self.check_col_limits3()
                for j, pane in enumerate(self.panes[i]):
                    if i < self.display_cols:
                        if j < col.display_rows -1:
                            self.panes[i][j].split.size[1] = clamp(self.size[1] * pane.height_prop, pane.split.min_size, pane.split.max_size)
                            self.check_row_limits(self.panes[i][j].split)
    
    def set_size_props(self):
        for col_index, col in enumerate(self.columns):
            if col_index < self.display_cols - 1:
                col.width_prop = col.split.size[0] / self.size[0]
            for row_index, pane in enumerate(self.panes[col_index]):
                if col_index < self.display_cols:
                    if row_index < col.display_rows -1:
                        pane.height_prop = pane.split.size[1] / self.size[1]
        self.build_complete = True

    def build_grid(self):
        self.build_complete = False
        self.display_cols = 0
        if self.hide_empty_panes:
            for col in self.contents:
                if col != []:
                    self.display_cols += 1
        else: self.display_cols = len(self.contents)
        col_index = 0
        for cont_col_index, col in enumerate(self.contents):
            self.columns[col_index] = BoxLayout(orientation='vertical')
            self.columns[col_index].display_rows = 0
            if col != [] or not self.hide_empty_panes:
                if cont_col_index < len(self.contents) - 1:
                    # Not last column
                    self.columns[col_index].split = ColSplitter(sizable_from='right', 
                        strip_size=self.strip_size, col_index=col_index, app_cursor=self.app_cursor)
                    self.columns[col_index].split.add_widget(self.columns[col_index])
                    self.add_widget(self.columns[col_index].split)
                    self.columns[col_index].grab = self.columns[col_index].split
                else:
                    # Last column
                    self.add_widget(self.columns[col_index])
                    self.columns[col_index].grab = self.columns[col_index]
                row_index = 0
                for row in col:
                    if row != None or self.hide_empty_panes == False:
                        # Put something in the pane
                        self.panes[col_index][row_index] = BoxLayout()
                        if row == None:
                            pane_content = EmptyPane()
                        else:
                            pane_content = row
                            row.grid = self
                            size_limit = row.size_limit
                        if row != col[-1]:
                            # Not last row, so put it in a splitter
                            size_limit = {'min': pane_content.size_limit['min'], 'max':pane_content.size_limit['max']}
                            self.panes[col_index][row_index].split = RowSplitter(grid=self, sizable_from='bottom', strip_size=self.strip_size,
                                                    col_index=col_index, row_index=row_index, size_limit=size_limit, app_cursor=self.app_cursor)
                            self.panes[col_index][row_index].split.add_widget(self.panes[col_index][row_index])
                            self.columns[col_index].add_widget(self.panes[col_index][row_index].split)
                        else:
                            # Last row - no splitter needed
                            self.columns[col_index].add_widget(self.panes[col_index][row_index])
                        self.panes[col_index][row_index].add_widget(pane_content)
                        self.columns[col_index].display_rows += 1
                        row_index += 1
                col_index += 1
        for col_index in range(self.display_cols):
            min_size = self.strip_size + self.min_empty_pane_size[0]
            max_size = 10000000
            for row_index in range(self.columns[col_index].display_rows):
                pane = self.panes[col_index][row_index]
                if not isinstance(pane, EmptyPane):
                    min_size = max(min_size, pane.children[0].size_limit['min'][0] + self.strip_size)
                    max_size = min(max_size, pane.children[0].size_limit['max'][0] + self.strip_size)
            self.columns[col_index].min_size = min_size
            self.columns[col_index].max_size = max_size
            if col_index < self.display_cols - 1:
                self.columns[col_index].split.size_limit = {'min':min_size, 'max':max_size}
        Clock.schedule_once(lambda dt: self.final_build_tasks())
                    
    def final_build_tasks(self):
        self.check_col_limits3()
        for col_index, col in enumerate(self.columns):
            if col_index < self.display_cols:
                if col.display_rows > 1:
                    self.check_row_limits(self.panes[col_index][0].split)
        self.set_size_props()
    
    def balance_col_size(self, changed_splitter):
        if self.display_cols > changed_splitter.col_index + 2:
            # Not the rightmost splitter
            i = changed_splitter.col_index
            self.columns[i+1].split.size[0] -= changed_splitter.size[0] - changed_splitter.previous_size
            self.columns[i+1].split.size[0] = clamp(self.columns[i+1].split.size[0], self.columns[i+1].min_size, self.columns[i+1].max_size)
            self.columns[i+1].split.previous_size = self.columns[i+1].split.size[0]
        else:
            right = self.size[0] - self.col_split_total()
            if right < self.columns[self.display_cols - 1].min_size or right > self.columns[self.display_cols - 1].max_size:
                changed_splitter.size[0] = changed_splitter.previous_size

    def balance_row_size(self,changed_splitter):
        self.adjusting = True
        i = changed_splitter.col_index 
        j = changed_splitter.row_index
        if changed_splitter.row_index < self.columns[changed_splitter.col_index].display_rows-2:
            # Not the bottom splitter
            self.panes[i][j+1].split.size[1] -= changed_splitter.size[1] - changed_splitter.previous_size 
            self.panes[i][j+1].split.size[1] = clamp(self.panes[i][j+1].split.size[1], self.panes[i][j+1].split.min_size, self.panes[i][j+1].split.max_size)
            self.panes[i][j+1].split.previous_size  = self.panes[i][j+1].split.size[1]
        else:
            bottom = self.size[1] - self.row_split_total(i)
            if bottom < self.panes[i][j].split.min_size or bottom > self.panes[i][j].split.max_size:
                changed_splitter.size[1] = changed_splitter.previous_size

    def check_col_limits3(self):
        # Makes max_count attempts to comply with size limit rules. Rules will remain broken if needed by the size of the overall GridSplitter.
        problem = ''
        count = 0
        max_count = 5
        while problem != 'none' and count < max_count:
            problem = 'none'
            count += 1
            for col_index, col in enumerate( self.columns):
                if col_index < self.display_cols -1:
                    if col.split.size[0] > col.max_size or col.split.size[0] < col.min_size:
                        problem = 'col outside limits'
                        col.split.size[0] = clamp(col.split.size[0], col.min_size, col.max_size)
                        col.split.previous_size = col.split.size[0]
            last = self.size[0] - self.col_split_total()
            if last < self.columns[self.display_cols - 1].min_size:
                problem = 'last col too small'
                self.adjust_col_splits(self.columns[self.display_cols - 1].min_size)
            if last > (self.columns[self.display_cols - 1].max_size +1):
                problem = 'last col too big'
                self.adjust_col_splits(self.columns[self.display_cols - 1].max_size)

    def check_row_limits(self, row_split):
        #row_split can be any RowSplitter in the column to be checked
        problem = ''
        col_index= row_split.col_index
        count = 0
        max_count = 100
        while problem != 'none' and count < max_count:
            problem = 'none'
            count += 1
            for row_index, pane in enumerate(self.panes[col_index]):
                if row_index < self.columns[col_index].display_rows - 1:
                    if pane.split.size[1] > pane.split.max_size or pane.split.size[1] < pane.split.min_size:
                        problem = 'pane outside vertical limits'
                        pane.split.size[1] = clamp(pane.split.size[1], pane.split.min_size, pane.split.max_size)
                        pane.split.previous_size = pane.split.size[1]
            last = self.size[1] - self.row_split_total(col_index)
            if last < self.panes[col_index][self.columns[col_index].display_rows -1].children[0].size_limit['min'][1]:
                problem = 'last row too small'
                self.adjust_row_splits(col_index, self.panes[col_index][self.columns[col_index].display_rows -1].children[0].size_limit['min'][1])
            if last > self.panes[col_index][self.columns[col_index].display_rows -1].children[0].size_limit['max'][1]:
                problem = 'last row too big'
                self.adjust_row_splits(col_index, self.panes[col_index][self.columns[col_index].display_rows -1].children[0].size_limit['max'][1])

    def adjust_col_splits(self, last_col_size):
        ratio = (self.size[0] - last_col_size) / self.col_split_total()
        for col_index, col in enumerate( self.columns):
            if col_index < self.display_cols -1:
                col.split.size[0] = (col.split.size[0] * ratio)
                col.split.previous_size = col.split.size[0]

    def adjust_row_splits(self, col_index, last_row_size):
        if self.row_split_total(col_index) == 0:
            ratio = 1
        else:
            ratio = (self.size[1] - last_row_size) / self.row_split_total(col_index)
        for row_index, row in enumerate( self.panes[col_index]):
            if row_index < self.columns[col_index].display_rows -1:
                row.split.size[1] = (row.split.size[1] * ratio)
                row.split.previous_size = row.split.size[1]

    def col_split_total(self):
        total = 0
        for i, col in enumerate(self.columns):
            if i < self.display_cols - 1:
                total += col.split.size[0]
        return total

    def row_split_total(self, col_index):
        total = 0
        for i, pane in enumerate(self.panes[col_index]):
            if i < self.columns[col_index].display_rows - 1:
                total += pane.split.size[1]
        return total
    
def clamp(value, lim1, lim2):
    if lim1 < lim2:
        return min(max(value, lim1), lim2)
    else: return min(max(value, lim2), lim1)