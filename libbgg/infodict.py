
import xml.etree.ElementTree as ET
import re

__all__ = ['InfoDict']

"""
This is a simple library that will convert a valid XML document to 
a dictionary and return it.

Example:

from libbgg.infodict import InfoDict

xml = '''<?xml version="1.0" encoding="UTF-8"?>
<myroot>
  <item>blah</item>
  <item>foo</item>
</myroot>
'''

d = InfoDict.xml_to_info_dict(xml)
print d['myroot']
# You can also access items like objects, and multiple elements will the same
# name will be a list:
print d.myroot.item[1]
"""

class InfoDict(dict):
    """
    Subclassing dict to add a classmethod which builds a dict from xml
    """
    # Take advantage of compilation for performance
    strip_NS_re = re.compile('^\{?[^\}]*\}')

    def __getattr__(self, name):
        """
        Add attribute access as an option
        """
        return self[name]

    @classmethod
    def xml_to_info_dict(cls, xml, strip_NS=True):
        """
        Return an InfoDict which contains the xml tree

        xml:str         The xml string to convert
        stripNS:bool    If True, the namespace prefix will be stripped
                        from the tags (keys) default: True
        """
        d = cls()
        root = ET.fromstring(xml.strip())
        d._build_dict_from_xml(d, root, strip_NS)
        return d

    def _build_dict_from_xml(self, d, el, strip_NS):
        """
        Recursively construct an InfoDict from an ElementTree object

        d:InfoDict      An empty instance of ourself to start and
                        subsequent instances as we recurse through
                        the tree
        el:xml.etree.ElementTree.Element    The current element in the tree
        stripNS:bool    If this is True, the namespace will be stripped from
                        tags
        """
        children = el.getchildren()
        if strip_NS:
            tag = self._strip_NS(el.tag)
        new_dict = InfoDict(el.attrib)
        if tag in d:
            if not isinstance(d[tag], list):
                # Handle multiple entries at the same level
                val = d[tag]
                d[tag] = [val]
        else:
            # Instantiate this otherwise
            d[tag] = None
        if children:
            # We have children
            if isinstance(d[tag], list):
                d[tag].append(new_dict)
            else:
                d[tag] = new_dict
            for c in children:
                self._build_dict_from_xml(new_dict, c, strip_NS)
        else:
            # handle multiple tags with the same name by creating and 
            # appending to a list
            if el.text:
                new_dict['TEXT'] = el.text
            if isinstance(d[tag], list):
                #d[tag].append(el.text)
                d[tag].append(new_dict)
            else:
                # By defaul, the value will be a string
                d[tag] = new_dict

    def _strip_NS(self, tag):
        """
        Strips off the namespace tag prefix
        """
        return self.strip_NS_re.sub('', tag)
