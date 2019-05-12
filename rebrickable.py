# -*- coding: utf-8 -*-

# rebrickable.py
#
# implements the class Rebrickable as an interface to rebrickable.com API V3

global debug, sleep_time

debug = 1
sleep_time = 0.5    # set to half a second to avoid that the requests to 
                    # Rebrickable.com are throttled


import requests
import time
import os

import lego as lg
import lego_shelves as lgs
import lego_conf as lconf


class Rebrickable:
    """
    # provides an interface to rebrickable.com API v3
    """
    

    def fetch_colour_shelf(self):
        """
        #
        # calls https://rebrickable.com/api/v3/lego/colors
        #                   ?key={api_key}&page=1
        #
        # returns all colours in Rebrickable.com as a LegoColourShelf 
        # of LegoColour objects
        #
        """     
        lcs = lgs.LegoColourShelf()
        next_page = 1
        while next_page > 0:
            try:
                payload = {'key': lconf.api_key , 'page': next_page}
                r = requests.get('https://rebrickable.com/api/v3/lego/colors', 
                                 params=payload)
                r.raise_for_status()    # raise exception if bad request 
                                        # (a 4XX client error or 5XX server 
                                        # error response)
                for i in r.json()['results']:
                    c = lg.LegoColour(
                            i['id'],
                            i['name'],
                            i['rgb'],
                            i['is_trans'])
                    lcs[str(i['id'])] = c
            except requests.exceptions.HTTPError as e:
                print ('An error occurred: %s\n' % e , 'Detail:' , 
                       r.json()['detail'])
            if r.json()['next']:
                next_page += 1
                time.sleep(sleep_time)
            else:
                next_page = 0
        
        lcs.close() 

    def fetch_theme_shelf(self):
        """
        #
        # calls https://rebrickable.com/api/v3/lego/themes
        #                   ?key={api_key}
        #
        # returns all themes in Rebrickable.com as a LegoThemeShelf
        # of LegoTheme objects
        #
        """
        
        ths = lgs.LegoThemeShelf()
        next_page = 1
        while next_page > 0:
            try:
                payload = {'key': lconf.api_key , 'page': next_page}
                r = requests.get('https://rebrickable.com/api/v3/lego/themes', 
                                 params=payload)
                r.raise_for_status()
                for i in r.json()['results']:
                    th = lg.LegoTheme(i['id'], i['name'], i['parent_id'])
                    ths[str(i['id'])] = th
            except requests.exceptions.HTTPError as e:
                print ('An error occurred: %s\n' % e , 'Detail:' , 
                       r.json()['detail'])
            if r.json()['next']:
                next_page += 1
                time.sleep(sleep_time)
            else:
                next_page = 0
        
        ths.close()

    def fetch_part_category_shelf(self):
        """
        # calls https://rebrickable.com/api/v3/lego/part_categories
        #                   ?key={api_key}
        #
        # returns all part categories in Rebrickable.com as a
        # LegoPartCategoryShelf of LegoPartCategory objects
        #
        """
        
        pcs = lgs.LegoPartCategoryShelf()
        next_page = 1
        while next_page > 0:
            try:
                payload = {'key': lconf.api_key , 'page': next_page}
                r = requests.get(
                        'https://rebrickable.com/api/v3/lego/part_categories', 
                        params=payload)
                r.raise_for_status()
                for i in r.json()['results']:
                    pc = lg.LegoPartCategory(i['id'], i['name'])
                    pcs[str(i['id'])] = pc
            except requests.exceptions.HTTPError as e:
                print ('An error occurred: %s\n' % e , 'Detail:' , 
                       r.json()['detail'])
            if r.json()['next']:
                next_page += 1
                time.sleep(sleep_time)
            else:
                next_page = 0
        
        pcs.close()

    
    def fetch_main_shelves(self):
        '''
        # Fetches the parts, elements and sets shelves
        '''
        
        ps = lgs.LegoPartShelf()
        es = lgs.LegoElementShelf()
        us = lgs.LegoSetShelf()
        
        # first get a dictionary <set_num:qty> with all the user sets
        
        sd = {}
        
        next_page = 1
        while next_page > 0:
            try:
                payload = {'key': lconf.api_key , 'page': next_page}
                if debug:
                    print ('Fetching sets in list, page', next_page, ' ...')
                r = requests.get('https://rebrickable.com/api/v3/users/' + 
                                 lconf.user_token + '/setlists/' +
                                 lconf.list_id + '/sets', params=payload)
                r.raise_for_status()
                
                for i in r.json()['results']:
                    sd[str(i['set']['set_num'])] = i['quantity']
                    
            except requests.exceptions.HTTPError as e:
                print ('An error occurred: %s\n' % e , 'Detail:' , 
                       r.json()['detail'])
            if r.json()['next']:
                next_page += 1
                time.sleep(sleep_time)
            else:
                next_page = 0
                
        # next, for all the set numbers, call   
        #
        # https://rebrickable.com/api/v3/lego/sets/{ls_num}
        #           ?key={api_key}
        # and
        # https://rebrickable.com/api/v3/lego/sets/{ls_num}/parts/
        #           ?key={api_key}
        
        for ls_num in sd.keys():
            
            if debug:
                print('Fetching set :', ls_num, ' ...')
        
            try:
                # fetch set basic information
                
                payload = {'key': lconf.api_key }
                r = requests.get('https://rebrickable.com/api/v3/lego/sets/' + 
                                 ls_num, params=payload)
                r.raise_for_status()
        
                ls_name = r.json()['name']
                ls_year = r.json()['year']
                ls_theme_id = r.json()['theme_id']
                ls_num_parts = r.json()['num_parts']
                ls_url = r.json()['set_url']
                ls_img_url = r.json()['set_img_url']
                
            
                # now fetch the set elements
                
                ls_ed = {} # dictionary to store <element_id, qty> pairs
                            # to create the LegoSet object
                
                next_page = 1
                while next_page > 0:
                    payload = {'key': lconf.api_key , 'page': next_page}
                    if debug:
                        print ('Fetching elements, page', next_page, 
                               ' ...')
                    r = requests.get(
                            'https://rebrickable.com/api/v3/lego/sets/'
                            + ls_num + '/parts/', params=payload)
                    r.raise_for_status()
                    for i in r.json()['results']:
                        lp = lg.LegoPart( # constructs the part
                                i['part']['part_num'],
                                i['part']['name'],
                                i['part']['part_cat_id'],
                                i['part']['part_url'],
                                i['part']['part_img_url']) 
                            
                        ps[i['part']['part_num']] = lp  # add the part to 
                                                        # shelf
                        le = lg.LegoElement( # constructs the element
                                i['id'],
                                i['inv_part_id'],
                                i['part']['part_num'],
                                i['color']['id'],
                                i['part']['part_img_url'],
                                i['quantity'] * sd[ls_num]) # multiply by
                                                            # qty of sets
                        
                        es[str(i['id'])] = le # add the element to the shelf
                        ls_ed[i['id']] = i['quantity']  # attribute of the 
                                                        # LegoSet object

                    if r.json()['next']:
                        next_page += 1
                        time.sleep(sleep_time)
                    else:
                        next_page = 0
            
                ls = lg.LegoSet(
                        ls_num,
                        ls_name,
                        ls_year,
                        ls_theme_id,
                        ls_num_parts,
                        ls_url,
                        ls_img_url,
                        ls_ed, # dictionary <element_id, qty>
                        sd[ls_num]) # qty of sets
                us[str(ls_num)] = ls # add the lego set to the shelf
            
            except requests.exceptions.HTTPError as e:
                print ('An error occurred: %s\n' % e , 'Detail:' , 
                           r.json()['detail'])
        
        ps.close()
        es.close()
        us.close()


    def fetch_img (self, remote_url, local_url) :
        """
        # fetches a remote file to a local destination
        """
        if not os.path.isfile(local_url):
            try:
                r = requests.get(remote_url)
                with open(local_url, 'wb') as f:
                    f.write(r.content)
            except requests.exceptions.HTTPError as e:
                print ('An error occurred: %s\n' % e , 'Detail:' , 
                           r.json()['detail'])
            except IOError:
                print ('Error creating %s\n' % local_url)
    
    
            
            
        
        
        
        

###############################################################################

if __name__ == '__main__':

    rb = Rebrickable()
    
    while 1:
        print ("Rebrickable - Menú:")
        print ("1 - fetch_colour_shelf()")
        print ("2 - fetch_theme_shelf()")
        print ("3 - fetch_part_category_shelf()")
        print ("4 - fetch_main_shelves()")
        print ("5 - fetch element images")
        print ("6 - fetch set images")
        print ("s - salir")
        option = input("Selecciona una opción: ")
        if (option == "1"):
            print ("Has escogido 1 - fetch_colour_shelf()")
            rb.fetch_colour_shelf()
            ls = lgs.LegoColourShelf()
            for k in ls.keys():
                print (k , ls[k])
            print (len(ls))
            ls.close()
        if (option == "2"):
            print ("Has escogido 2 - fetch_theme_shelf()")
            rb.fetch_theme_shelf()
            ls = lgs.LegoThemeShelf()
            for k in ls.keys():
                print (k , ls[k])
            print (len(ls))
            ls.close()
        if (option == "3"):
            print ("Has escogido 3 - fetch_part_category_shelf()")
            rb.fetch_part_category_shelf()
            ls = lgs.LegoPartCategoryShelf()
            for k in ls.keys():
                print (k , ls[k])
            print (len(ls))
            ls.close()
        if (option == "4"):
            print ("Has escogido 4 - fetch_main_shelves()")
            rb.fetch_main_shelves()
        if (option == "5"):
            print ("Has escogido 5 - fetch element images")
            els = lgs.LegoElementShelf()
            for el in els.keys():
                print ('Fetching img for element ', el)
                rb.fetch_img(els[el].get_img_url(), 
                             els[el].get_local_img_url())
        if (option == "6"):
            print ("Has escogido 6 - fetch set images")
            ss = lgs.LegoSetShelf()
            for s in ss.keys():
                print ('Fetching img for set ', s)
                rb.fetch_img(ss[s].get_img_url(), 
                             ss[s].get_local_img_url())
        elif (option == "s"):
            break
        else:
            print ("Prueba otra vez")
