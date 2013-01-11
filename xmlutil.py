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

def nextElement(node):
    while True:
        node = node.nextSibling
        if node is None or node.nodeType == Node.ELEMENT_NODE:
            break
    return node
