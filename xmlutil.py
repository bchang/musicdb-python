'''
Created on Jan 10, 2013

@author: bchang
'''
from xml.dom import Node

def getChildren(parent):
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE:
            yield node

def getChildrenByTagName(parent, name):
    for node in getChildren(parent):
        if node.tagName == name:
            yield node

def firstChildElement(node):
    node = node.firstChild
    return __ensureElement__(node)

def nextSiblingElement(node):
    node = node.nextSibling
    return __ensureElement__(node)

def __ensureElement__(node):
    while node is not None and node.nodeType != Node.ELEMENT_NODE:
        node = node.nextSibling
    return node
