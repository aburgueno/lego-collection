# -*- coding: utf-8 -*-

global debug
debug = 1


import shelve
import csv
import pandas as pd
import os

import lego_conf as lconf



class LegoShelf(shelve.Shelf):
    '''
    #
    # generic class to provide shelves for various Lego objects
    #
    # { key : {key : value}}
    #
    '''
    
    def __init__(self, file_name):
        if not os.path.isdir(lconf.shelves_dir):
            os.mkdir(lconf.shelves_dir)    

        self.shelf = shelve.open(file_name, flag='c', writeback=True)
        
    def __len__(self):
        return len(self.shelf)
    
    def __getitem__(self, key):
        return self.shelf[key]

    def __setitem__(self, key, value):
        self.shelf[key]=value
        self.shelf.sync()

    def __delitem__(self, key):
        del(self.shelf[key])
        
    def __contains__(self, obj):
        return (obj in self.shelf)
        
    def keys(self):
        return self.shelf.keys()
        
    def close(self):
        self.shelf.close()
        
    def sync(self):
        self.shelf.sync()
        
    def get_dataframe(self):
        return (pd.DataFrame.from_dict(self.shelf, dtype='str', \
                                       orient='index'))
            
        
 
###############################################################################    
    
class LegoColour(dict):
    """
    # 
    # { 'id'            : <int>,
    #   'name'          : <string>,
    #   'rgb'           : <string>,
    #   'is_trans'      : <boolean>,
    #   }
    #
    """

    def __init__(self, lc_id, lc_name, lc_rgb, lc_is_trans):

        self['id'] = lc_id
        self['name'] = lc_name
        self['rgb'] = lc_rgb
        self['is_trans'] = lc_is_trans
        
    def get_id(self):
        return self['id']
        
    def get_name(self):
        return self['name']
        
    def get_rgb(self):
        return self['rgb']
        
    def is_trans(self):
        return self['is_trans']

class LegoColourShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'colours'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)
        
    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('colour_')
        return (df)
     
###############################################################################    

class LegoTheme(dict):
    """
    # 
    # { 'id'            : <int>,
    #   'name'          : <string>,
    #   'parent_id'     : <int>
    # }
    #    
    """
    
    def __init__(self, lt_id, lt_name, lt_parent_id):

        self['id'] = lt_id
        self['name'] = lt_name
        self['parent_id'] = lt_parent_id
        
    def get_id(self):
        return self['id']
        
    def get_name(self):
        return self['name']
    
    def get_parent_id(self):
        return self['parent_id']

class LegoThemeShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'themes'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)

    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('theme_')
        return (df)


###############################################################################    

class LegoPartCategory(dict):
    """
    # 
    # { 'id'            : <int>,
    #   'name'          : <string>
    # }
    #    
    """
    
    def __init__(self, ct_id, ct_name):

        self['id'] = ct_id
        self['name'] = ct_name
        
    def get_id(self):
        return self['id']
        
    def get_name(self):
        return self['name']

class LegoPartCategoryShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'part_categories'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)        

    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('part_category_')
        return (df)

       
###############################################################################    

class LegoPart(dict):
    '''
    # { 'num'           : <string>,
    #   'name'          : <string>,
    #   'cat_id'        : <int>,
    #   'url'           : <string>,
    #   'img_url'       : <string> or None
    #   'local_img_url' : <string> or None
    #   'box'           : <string> or None
    # }
    '''

    def __init__(self, lp_num, lp_name, lp_cat_id, lp_url, lp_img_url):

        self['num'] = lp_num
        self['name'] = lp_name
        self['cat_id'] = lp_cat_id
        self['url'] = lp_url
        self['img_url'] = lp_img_url
        self['box_num'] = None
        if type(lp_img_url) == type(None) : # no image URL
            self['local_img_url'] = lconf.element_img_dir + 'ni.png'
        else :
            self['local_img_url'] = lconf.element_img_dir + \
                                    lp_img_url.split('/')[-1]
                           
    def get_num(self):
        return self['num']
        
    def get_name(self):
        return self['name']

    def get_cat_id(self):
        return self['cat_id']
        
    def get_url(self):
        return self['url']
    
    def get_img_url(self):
        return self['img_url']
    
    def get_box_num(self):
        return self['box_num']
    
    def set_box_num(self, bn):
        self['box_num'] = bn

    def get_local_img_url(self):
        return self['local_img_url']
    
                  
        
class LegoPartShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'parts'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)


    def fetch_boxes(self):
        '''
        # Gets the box_num per part_id from part_box.csv and 
        # sets the box_num in the corresponding LegoPart object
        #
        # If box_num == 00 or XX in csv file, sets box_num to '??' in LegoPart
        # 
        # ignores the part_ids in csv file not in the shelf
        #
        # After going through the csv file, for all LegoParts with box_num as 
        # None, sets box_num to '??'
        '''
        
        with open(lconf.part_box_csv_file, 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                part_id = row[0]
                box_num = row[1]
                if debug:
                    print ("Part: ", part_id, " Box: ", box_num)
                if part_id in self:
                    self[part_id].set_box_num(box_num)
        for lp in self.keys():
            if self[lp].get_box_num() is None:
                self[lp].set_box_num('00')
        self.shelf.sync()
                    
    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('part_')
        return (df)
        
        
###############################################################################    

class LegoElement(dict):
    '''
    # { 'part_num'        : <string>
    #   'colour_id'       : <int>
    #   'id'              : <int>,
    #   'design_id'       : <int>,
    #   'img_url'         : <string>,
    #   'local_img_url    : <string>,
    #   'quantity'        : <int>  ---  used to store the number of elements in 
    #                                   a lego set
    # }
    '''
    def __init__(self, le_id, le_design_id, le_part_num, le_colour_id, 
                 le_img_url, le_qty):
        
        self['id'] = le_id
        self['design_id'] = le_design_id
        self['part_num'] = le_part_num
        self['colour_id'] = le_colour_id
        self['quantity'] = le_qty
        self['img_url'] = le_img_url     
        if type(le_img_url) == type(None) : # no image URL
            self['local_img_url'] = 'img/elements/ni.png'
        else :
            self['local_img_url'] = 'img/elements/' + le_img_url.split('/')[-1]
        
    def get_id(self):
        return self['id'] 
    
    def get_design_id(self):
        return self['design_id']
    
    def get_part_num(self):
        return self['part_num']
    
    def get_colour_id(self):
        return self['colour_id']
    
    def get_img_url(self):
        return self['img_url']
    
    def get_local_img_url(self):
        return self['local_img_url']
    
    def get_quantity(self):
        return self['quantity']
    
    def set_quantity(self, qty):
        self['quantity'] = qty


class LegoElementShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'elements'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)        

    def __setitem__(self, key, value):
        if key not in self.shelf:
            self.shelf[str(key)]=value
        else:
            le = self.shelf[key]
            le.set_quantity(le.get_quantity() + value.get_quantity())
            self.shelf[str(key)] = le
        self.shelf.sync()

    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('element_')
        df['element_quantity'] = df['element_quantity'].astype(int)
        return (df)


###############################################################################    

class LegoSet(dict):
    """
    # { 'num'           : <string>,
    #   'name'          : <string>,
    #   'year'          : <int>,
    #   'theme_id'      : <int>,
    #   'num_parts'     : <int>,
    #   'url'           : <string>,
    #   'img_url'       : <string>,
    #   'local_img_url' : <string>,
    #   'elements'      : {<element_id>:<qty> ... },
    #   'quantity'      : <int>  --- use to store how many of this set 
    #                                the collection holds
    # }
    """
    
    def __init__(self, ls_num, ls_name, ls_year, ls_theme_id, ls_num_parts,
                 ls_url, ls_img_url, ls_elements, ls_qty):

        self['num'] = ls_num
        self['name'] = ls_name
        self['year'] = ls_year
        self['theme_id'] = ls_theme_id
        self['num_parts'] = ls_num_parts
        self['url'] = ls_url
        self['img_url'] = ls_img_url
        self['elements'] = ls_elements
        if type(ls_img_url) == type(None) : # no image URL
            self['local_img_url'] = lconf.set_img_dir + 'ni.png'
        else :
            self['local_img_url'] = lconf.set_img_dir + \
                                    ls_img_url.split('/')[-1]
        self['quantity'] = ls_qty
        

    def get_num(self):
        return self['num']

    def get_name(self):
        return self['name']
    
    def get_year(self):
        return self['year']

    def get_theme_id(self):
        return self['theme_id']

    def get_num_parts(self):
        return self['num_parts']
    
    def get_url(self):
        return self['url']

    def get_img_url(self):
        return self['img_url']

    def get_local_img_url(self):
        return self['local_img_url']

    def get_elements(self):
        return self['elements']    
    
    def get_quantity(self):
        return self['quantity']
 
    def set_quantity(self, qty):
        self['quantity'] = qty


class LegoSetShelf(LegoShelf):
    
    file_name = lconf.shelves_dir +  'sets'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)    
        
        
    def get_dataframe(self):
        
        num_list = []
        name_list = []
        year_list = []
        theme_id_list = []
        num_parts_list = []
        img_url_list = []
        local_img_url_list = []
        url_list = []
        element_id_list = []
        element_quantity_list = []
        set_quantity_list = []
        
        for ls in self.keys():
            n = len(self[ls].get_elements())
            num_list += [self[ls].get_num()]*n
            name_list += [self[ls].get_name()]*n
            year_list += [self[ls].get_year()]*n
            theme_id_list += [self[ls].get_theme_id()]*n
            num_parts_list += [self[ls].get_num_parts()]*n
            img_url_list += [self[ls].get_img_url()]*n
            local_img_url_list += [self[ls].get_local_img_url()]*n
            url_list += [self[ls].get_url()]*n
            set_quantity_list += [self[ls].get_quantity()]*n
            for el in self[ls].get_elements().keys():
                element_id_list.append(el)
                element_quantity_list.append(self[ls].get_elements()[el])
            
        data = {'set_num':num_list,
               'set_name':name_list,
               'set_year': year_list,
               'set_theme_id': theme_id_list,
               'set_num_parts': num_parts_list,
               'set_img_url': img_url_list,
               'set_local_img_url': local_img_url_list,
               'set_url': url_list,
               'set_quantity': set_quantity_list,
               'set_element_id': element_id_list,
               'set_element_quantity': element_quantity_list}     
       
        df = pd.DataFrame(data)
        df = df.astype(str)
        df[["set_quantity", "set_element_quantity", "set_num_parts"]] = \
            df[["set_quantity", "set_element_quantity", \
                "set_num_parts"]].astype(int)
        return (df)     

###############################################################################    


class LegoBox(dict):
    '''
    # { 'num'           : <string>,
    # }
    '''
    
    def __init__(self, box_num):
        self['num']=box_num
        self['element_ids']=[] # create an empty LegoBox 
        
    def get_num(self):
        return(self['num'])
             
        
class LegoBoxShelf(LegoShelf):
    
    file_name = lconf.shelves_dir +  'boxes'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)
        
    def fetch_boxes(self):
        '''
        # Gets the box numbers from boxes.csv and creates and for each box
        # number adds a LegoBox object with that number to the shelf
        '''
        
        with open(lconf.part_box_csv_file, 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                box_num = row[1]
                if box_num not in self.shelf:
                    self.shelf[box_num] = LegoBox(box_num)
        self.shelf.sync()

    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('box_')
        return (df)




###############################################################################

if __name__ == '__main__':

    while 1:
        print ("Menú:")
        print ("1 - LegoBoxShelf.fetch_boxes()")
        print ("2 - LegoPartShelf.fetch_boxes()")
        print ("3 - get_dataframe()")
        print ("4 - get boxes from parts")
        print ("5 - LegoSetShelf.get_dataframe()")
        print ("s - Salir")
        option = input("Selecciona una opción: ")
        if (option == "1"):
            print ("Has escogido 1 - LegoBoxShelf.fetch_boxes()")
            lbs = LegoBoxShelf()
            lbs.fetch_boxes()
            for k in lbs.keys():
                print (k , lbs[k])
            print (len(lbs))
            lbs.close()
        if (option == "2"):
            print ("Has escogido 2 - LegoPartShelf.fetch_boxes()")
            lps = LegoPartShelf()
            lps.fetch_boxes()
            lps.sync()
            for k in lps.keys():
                print (k , lps[k].get_box_num())
            lps.close()
        if (option == "4"):
            print ("Has escogido 4 - get boxes from parts")
            lps = LegoPartShelf()
            for k in lps.keys():
                print (k , lps[k])
            lps.close()
        if (option == "3"):
            print ("Has escogido 3 - get_dataframe()")
            les = LegoElementShelf()
            df = les.get_dataframe()
            print (df)
            les.close()
        if (option == "5"):
            print ("Has escogido 5 - LegoSetShelf.get_dataframe()")
            lss = LegoSetShelf()
            df = lss.get_dataframe()
            print (df)
            lss.close()
        elif (option == "s"):
            break
        else:
            print ("Prueba otra vez")
        
       