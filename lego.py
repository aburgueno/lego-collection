# -*- coding: utf-8 -*-

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


       
###############################################################################    
        
        
###############################################################################    


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


###############################################################################    



###############################################################################

