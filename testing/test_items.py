import unittest
import json

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from items import Item
import config
import pygame
# must set for items class to work (sprites)
screen = pygame.display.set_mode((800, 600))
class TestItem(unittest.TestCase):
    def test_item_attribute(self):
        f = open(os.path.join(parentdir,"data/item_data.json"),"r")
        data = json.load(f)
        f.close()
        items = data.keys()
        for item in items: 
            new_item = Item(item)
            attr = new_item.item_attr
            self.assertEqual(data[item]["attributes"], attr)
            

if __name__ == '__main__':
    unittest.main()
