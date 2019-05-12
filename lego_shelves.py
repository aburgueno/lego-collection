# -*- coding: utf-8 -*-

global debug
debug = 1


import os
import csv
import shelve
import pandas as pd

import lego_conf as lconf
import lego as lg


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
                    self.shelf[box_num] = lg.LegoBox(box_num)
        self.shelf.sync()

    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('box_')
        return (df)





class LegoColourShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'colours'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)
        
    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('colour_')
        return (df)

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
        



class LegoPartCategoryShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'part_categories'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)        

    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('part_category_')
        return (df)

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



class LegoThemeShelf(LegoShelf):
    
    file_name = lconf.shelves_dir + 'themes'
    
    def __init__(self):
        LegoShelf.__init__(self, self.file_name)

    def get_dataframe(self):
        df = LegoShelf.get_dataframe(self)
        df = df.add_prefix('theme_')
        return (df)

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
        
       



