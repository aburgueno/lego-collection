# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 09:07:49 2018

@author: Augusto
"""

global debug 
debug = 1

import os
import pandas as pd

import lego as lg
import rebrickable as rb
import lego_conf as lconf

from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader(lconf.jinja2_template_dir), # path to template files
    autoescape=select_autoescape(['html', 'xml'])
) 


class LegoCollection: 

    def __init__(self):

        self.reb = rb.Rebrickable()

        self.lcs = lg.LegoColourShelf()
        self.lts = lg.LegoThemeShelf()       
        self.lpcs = lg.LegoPartCategoryShelf()        
        self.lps = lg.LegoPartShelf()        
        self.les = lg.LegoElementShelf()        
        self.lss = lg.LegoSetShelf()        
        self.lbs = lg.LegoBoxShelf()

    def build_collection(self):
        
        # create the shelves directory if it doesn't exist
        # empty the shelves directory if not empty
        
        reb = rb.Rebrickable()
                
        if os.path.isdir(lconf.shelves_dir):
            list(map(os.unlink, (os.path.join(lconf.shelves_dir,f) \
                                 for f in os.listdir(lconf.shelves_dir))))
        else:
            os.mkdir(lconf.shelves_dir)    

        # fetch data from rebrickable
        
        reb.fetch_colour_shelf()
        reb.fetch_theme_shelf()
        reb.fetch_part_category_shelf()
        reb.fetch_main_shelves()
        
        # fetch element images
        
        for el in self.les.keys():
            if debug:
                print ('Fetching img for element ', el)
            self.reb.fetch_img(self.les[el].get_img_url(), 
                         self.les[el].get_local_img_url())

        # fetch set images
            
        for s in self.lss.keys():
            if debug:
                print ('Fetching img for set ', s)
            self.reb.fetch_img(self.lss[s].get_img_url(), 
                         self.lss[s].get_local_img_url())

        # fetch local data

        lg.LegoBoxShelf().fetch_boxes()
        lg.LegoPartShelf().fetch_boxes()
        

       
        
    def merge_collection(self):
        '''
        # merges the collection shelves and returns a pandas dataframe
        '''

      
        ledf = self.les.get_dataframe()
        lcdf = self.lcs.get_dataframe()
        lpdf = self.lps.get_dataframe()
        lpcdf = self.lpcs.get_dataframe()
        lsdf = self.lss.get_dataframe()
        ltdf = self.lts.get_dataframe()
        
        '''
        # first group the element dataframe to get the total number of 
        # elements per part_num and colour_id
        legdf = ledf.groupby(['part_num','colour_id', 'local_img_url']).sum().\
                reset_index()
        '''
        
        # merge element with colour dataframe
        df = pd.merge(ledf, lcdf, left_on='element_colour_id', \
                                  right_on='colour_id', how='left')
        # merge the result with part dataframe
        df = pd.merge(df, lpdf, left_on='element_part_num', \
                                right_on='part_num', how='left')
        # merge the result with part categorie dataframe
        df = pd.merge(df, lpcdf, left_on='part_cat_id', 
                                 right_on='part_category_id', how='left')
        # merge the set dataframe with the result
        df = pd.merge(lsdf, df, left_on='set_element_id', 
                                right_on='element_id', how='left')
        # merge the result with the theme dataframe 
        df = pd.merge(df, ltdf, left_on='set_theme_id', 
                                right_on='theme_id', how='left')
        
        
        # drop unnecessary colums
        df = df.drop(['set_element_id', 'element_part_num', 'set_theme_id', \
                      'element_colour_id', 'part_category_id', \
                      'set_element_quantity'], axis = 1)
        
#        df.to_csv("dataframe.csv")

        return (df) # returns a data frame (see structure in doc)

###############################################################################                            

    def build_html(self, param=None):
        
        if param == None:
            print ("build_html: expects one parameter")
        elif param == "boxes":
            
            df  = lc.merge_collection() 
        
            # create the box index

            template = env.get_template(lconf.boxes_template_file)
               
            gdf = df.groupby(['part_name', 'part_category_name', \
                              'part_local_img_url', \
                              'part_box_num']).sum().reset_index()

       
            ed = gdf.to_dict(orient='index')

            el = []
            for i in ed.keys():
                el.append(ed[i])

            with open(lconf.box_html_dir + "boxes.html", mode="w", \
                      encoding='utf-8') as file_a:
                file_a.write(template.render(elements = el))

            # create the individual box pages
        
            template = env.get_template(lconf.box_template_file)

            for box_num in self.lbs.keys():

                if debug:
                    print ("Processing box: ", box_num)
             
                fdf = df.loc[df['part_box_num'] == box_num]
                fdf = fdf.groupby(['part_category_name', 'part_name', \
                               'colour_id', 'colour_name', 'part_num', \
                               'element_local_img_url']).sum().reset_index()
        
                ed = fdf.to_dict(orient='index')

                el = []
                for i in ed.keys():
                    el.append(ed[i])
            
                file_name = lconf.box_html_dir + "box-" + box_num +".html"

                with open(file_name, mode="w", encoding='utf-8') \
                    as file_a:
                        file_a.write(template.render(box_num = box_num, \
                                                     elements = el))

        elif param == "sets":
        
            df  = lc.merge_collection() 

            # create the set index

            template = env.get_template(lconf.sets_template_file)
               
            gdf = df.groupby(['set_num', 'set_name', 'set_num_parts', \
                              'set_local_img_url', \
                              'theme_name']).sum().reset_index()
   
            ed = gdf.to_dict(orient='index')

            el = []
            for i in ed.keys():
                el.append(ed[i])

            with open(lconf.set_html_dir + "sets.html", mode="w", \
                      encoding='utf-8') as file_a:
                file_a.write(template.render(sets = el))

            # create the individual set pages

            template = env.get_template(lconf.set_template_file)
               
            gdf = df.groupby(['set_num', 'set_name', 'set_num_parts', \
                              'set_local_img_url', 'theme_name', \
                              'part_box_num', 'part_name', \
                              'colour_name', 'colour_id', \
                              'element_local_img_url']).sum().reset_index()

            for set_num in self.lss.keys():
            
                fdf = gdf.loc[gdf['set_num'] == set_num] # filter by set num
            
                ed = fdf.to_dict(orient='index')

                el = []
                for i in ed.keys():
                    el.append(ed[i])

                with open(lconf.set_html_dir + set_num + ".html", \
                          mode="w", encoding='utf-8') as file_a:
                    file_a.write(template.render( \
                                set_num = el[0]['set_num'],
                                set_name = el[0]['set_name'],
                                set_num_parts = el[0]['set_num_parts'],
                                set_local_img_url = el[0]['set_local_img_url'],
                                theme_name = el[0]['theme_name'],
                                elements = el))

        else: 
            print ("build_html: expects 'boxes or sets'")



   
###############################################################################

   
if __name__ == '__main__':

    lc = LegoCollection()
      
    while 1:
        print ("Menú:")
        print ("1 - build_collection()")
        print ("2 - build_html('sets')")
        print ("3 - build_html('boxes')")
        print ("s - Salir")
        option = input("Selecciona una opción: ")
        if (option == "1"):
            print ("Has escogido 1 - build_collection()")
            print (lc.build_collection())
        elif (option == "2"):
            print ("Has escogido 2 - build_html('sets')")
            lc.build_html('sets')
        elif (option == "3"):
            print ("Has escogido 2 - build_html('boxes')")
            lc.build_html('boxes')
        elif  (option == "s"):
            break
        else:
            print ("Prueba otra vez")


