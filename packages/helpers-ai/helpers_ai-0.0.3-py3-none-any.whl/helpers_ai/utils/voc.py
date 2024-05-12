def element_node(doc:object, tag:str, attr:str) -> None:
    
    ele = doc.createElement(tag)
    
    if attr is not None:
        text = doc.createTextNode(attr)
        ele.appendChild(text)
    
    return ele

def child_node(doc:object, tag:str, attr:str, parent_node:object) -> None:
    
    child = element_node(doc,tag,attr)
    parent_node.appendChild(child)

def object_node(doc:object, attr:list|tuple, box:list|tuple, seg:list[list,list]=None) -> object:
    
    object = doc.createElement("object")
    child_node(doc,"name",box[0],object)
    child_node(doc,"pose",str(attr[0]),object)
    child_node(doc,"truncated",str(attr[1]),object)
    child_node(doc,"difficult",str(attr[2]),object)
    child_node(doc,"occluded",str(attr[3]),object)

    bnd = doc.createElement("bndbox")
    child_node(doc,"xmin",str(box[1]),bnd)
    child_node(doc,"xmax",str(box[3]),bnd)
    child_node(doc,"ymin",str(box[2]),bnd)
    child_node(doc,"ymax",str(box[4]),bnd)
    object.appendChild(bnd)
    
    if seg is not None:

        poly = doc.createElement("polygon")
        
        for idx, (x, y) in enumerate(zip(*seg)):
            child_node(doc,"x"+str(idx+1),str(x),poly)
            child_node(doc,"y"+str(idx+1),str(y),poly)
        object.appendChild(poly)

    return object