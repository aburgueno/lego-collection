"""lego.py module

This module defines the classes used to represent the components of a 
collection of Lego sets. In this collection, Lego bricks are stored 
in labelled boxes according to shape. This means that bricks of the 
same shape but different colour are stored in the same box. The 
classes attempt to mirror the data structures underlying 
Rebrickable.com as provided by its API.

Classes
-------
LegoBox : Dict
	A class to represent the physical place where Lego bricks 
	are stored, i.e. the label of the box. 
LegoColour : Dict
	A class to represent the color of Lego bricks. It uses 
	Rebrickable.com and RGB colour IDs.
LegoElement : Dict
	A class to represent Lego bricks in the collection. 
	It provides the more detailed description of a Lego brick 
	and has to be distinguished from LegoPart. 
	LegoPart identifies the shape of a Lego brick, but not 
	its colour. LegoElement also provides the colour of a Lego
	brick, among other additional attributes, such as the total
	number of bricks with that shape and colour in the collection.
LegoPart : Dict
	A class to represent the shape of a Lego brick and its location
	in the collection (the box where it is stored - remember blocks 
	are stored by shape, and not colour)
LegoPartCategory : Dict
	A class to represent the category of a Lego part. The categories
	are the ones provided by Rebrickable.com, and not necessarily
	the ones defined by Lego
LegoSet : Dict
	A class to represent Lego sets, such as set 75159 'The Death
	Star'. 
LegoTheme : Dict
	A class to represent the theme to which a Lego set belongs. 
	For example, set 75159 'The Death Star' belongs to the theme
	'Star Wars'
"""

# -*- coding: utf-8 -*-

class LegoBox(dict):
	"""
	A class to represent the physical place where Lego bricks 
	are stored, i.e. the label of the box. In this collection
	all boxes are identified by unique labels such as "1.1" or
	"10"
	
	Attributes
	----------
	num : str
		the label of the box. Example: "10", "1.1", etc
	
	Methods
	-------
    get_num() -> str
		returns the label of the box
	"""
    
    def __init__(self, box_num):
		"""
		Initialises the object with the label provided in the
		parameter box_num
		
		Parameters
		----------
		box_num : str
			The label of the box
		"""
        self['num']=box_num
    #    self['element_ids']=[] # create an empty LegoBox 
	# TODO: I believe the attribute element_ids is legacy from previous 
	# 		versions and not used anymore. Doublecheck! 
        
    def get_num(self):
		"""
		Returns the label of the box as a string
		"""
        return(self['num'])        
 
###############################################################################    
    
class LegoColour(dict):
    """
    A class to represent the color of Lego bricks. It uses 
	RGB colour IDs.
	
	Attributes
	----------
	id : int
		Colour ID as provided by Rebrickable.com
	name : str
		Colour name as provided by Rebrickable.com
	rgb : str
		RGB id
	is_trans : bool
		True is colour is transparent
	
	Methods
	-------
	get_id() -> int
		Returns the Rebrickable colour ID as an int
	get_name() -> str
		Returns the name of the colour as a string
	get_rgb () -> str
		Returns the rgb code as a string
	is_trans() -> bool
		Returns true is the colour is transparent, false otherwise
    """

    def __init__(self, lc_id, lc_name, lc_rgb, lc_is_trans):
		"""
		Initialises the object
		
		Parameters
		----------
		lc_id : int
			Rebrickable colour ID
		lc_name : str
			Name of the colour
		lc_rgb : str
			RGB code
		lc_is_trans : bool
			True if the colour is transparent, false otherwise
		NOTE: lc stands for (l)ego (c)olour
		"""
 
        self['id'] = lc_id
        self['name'] = lc_name
        self['rgb'] = lc_rgb
        self['is_trans'] = lc_is_trans
        
    def get_id(self):
		"""
		Returns the Rebrickable colour ID as an int
		"""
        return self['id']
        
    def get_name(self):
 		"""
		Returns the name of the colour as a string
		"""
        return self['name']
        
    def get_rgb(self):
 		"""
		Returns the RGB code of the colour as a string
		"""
        return self['rgb']
        
    def is_trans(self):
		"""
		Returns TRUE if the colour is transparent, FALSE otherwise
		"""
        return self['is_trans']

# TODO: Continue documenting from here

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

