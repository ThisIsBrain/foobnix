'''
Created on Mar 11, 2010

@author: ivan
'''
import gtk
import gobject
from foobnix.model.entity import CommonBean

class DirectoryModel():
    POS_NAME = 0
    POS_PATH = 1
    POS_FONT = 2
    POS_VISIBLE = 3
    POS_TYPE = 4
    
    def __init__(self, widget):
        self.widget = widget
        column = gtk.TreeViewColumn("Title", gtk.CellRendererText(), text=0, font=2)
        column.set_resizable(True)
        widget.append_column(column)
        self.model =gtk.TreeStore(str, str, str, gobject.TYPE_BOOLEAN, str)
                
        filter = self.model.filter_new()
        filter.set_visible_column(self.POS_VISIBLE)
        widget.set_model(filter)
        
    def append(self, level, been):
        return self.model.append(level, [been.name, been.path, been.font, been.is_visible, been.type])
        
    def clear(self):
        self.model.clear() 
    def getModel(self):
        return self.model
        
    def getSelectedBean(self):
        selection = self.widget.get_selection()
        model, selected = selection.get_selected()
        return self._getBeanByIter(model, selected)   
    
    def _getBeanByIter(self, model, iter):
        if iter:
            bean = CommonBean()
            bean.name = model.get_value(iter, self.POS_NAME)
            bean.path = model.get_value(iter, self.POS_PATH)            
            bean.font = model.get_value(iter, self.POS_FONT)
            bean.visible = model.get_value(iter, self.POS_VISIBLE)
            bean.type = model.get_value(iter, self.POS_TYPE)            
            return bean
        return None

    def getChildSongBySelected(self):
        selection = self.widget.get_selection()
        model, selected = selection.get_selected()
        n = model.iter_n_children(selected)
        iterch = model.iter_children(selected)
        
        results = []
        
        for i in xrange(n):
            song = self._getBeanByIter(model, iterch)
            if song.type != CommonBean.TYPE_FOLDER:  
                results.append(self._getBeanByIter(model, iterch))
            iterch = model.iter_next(iterch)
        
        return results
        
        
    def filterByName(self, string):        
        if len(string.strip()) > 0:
            for line in self.model:
                name = line[self.POS_NAME].lower()
                string = string.strip().lower()
                
                if name.find(string) >= 0:
                    print "FIND :", name, string
                    line[self.POS_VISIBLE] = True                    
                else:                   
                    line[self.POS_VISIBLE] = False
        else:
            for line in self.model:                
                line[self.POS_VISIBLE] = True
    

