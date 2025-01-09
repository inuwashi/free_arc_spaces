

import json
from pprint import pprint


class ArcElem(object):
    parent = None
    parent_id: str = None
    children: list = set()
    
    icon: str = None
    name: str = None
    created: float = None
    emoji: int = None
    url: str = None
    elem_type: str = None
    
    def __init__(self, id: str):
        self.id: str = id
        
    def find(self, lookup):
        
        if self.id == lookup:
            return self
        
        for elem in self.children:
            return False or elem.find(lookup)
            
        return False 
    

    
    def __repr__(self):
        ident = self.name or self.id
        return f"{self.elem_type}: {ident}"

root = ArcElem("0")
root.name = "root"
root.elem_type = "Root"


if __name__ == '__main__':   
    
    with open('StorableSidebar.json') as f:
        d = json.load(f)
        
        # for space_id in d['sidebarSyncState']['container']['value']['orderedSpaceIDs']:
        #     print(space_id)
        
        #Set up the spaces
        for space in d['sidebarSyncState']['spaceModels']:
            if type(space) == str:
                space_id = space
                
                print(f"Processing space {space_id}")
            else:
                elem = ArcElem(space['value']["id"])
                
                
                elem.name = space['value']["title"]
                elem.icon = space['value']['customInfo']["iconType"]["emoji_v2"]
                elem.emoji = space['value']['customInfo']["iconType"]["emoji"]
                elem.parent = root
                elem.children = set()
                elem.elem_type = "Space"        
                
                root.children.add(elem)
                
        run_count = 0
        no_orphens = True
        while no_orphens == True and run_count < 10:
            run_count += 1
            print(f"   ###    Run {run_count}   ###")
            
            item_count = 0
            for item in d['sidebarSyncState']['items']:

                if type(item) == str:
                    item_id = item
                    item_count += 1
                    
                    print(f"Processing item #{item_count} {item_id}")
                else:
                    ivalues = item['value']
                    
                    arch_item = ArcElem(ivalues['id'])
                    arch_item.created = ivalues['createdAt']
                    arch_item.children = set()
                    
                    if len(ivalues['childrenIds']) > 0:
                        # Folders have content in their childrenIds array
                        arch_item.elem_type = "Folder"
                    else:
                        if "itemContainer" in ivalues["data"].keys():
                            # Contaioners dont get a title, or childrenIds for some reson 
                            arch_item.elem_type = "Container"
                            arch_item.parent_id = ivalues['data']["itemContainer"]["containerType"]["spaceItems"]["_0"] 
                        else:
                            arch_item.elem_type = "Bookmark"
                            arch_item.name = ivalues['title']
                            arch_item.url = ivalues['data']['tab']['savedURL']
                            arch_item.parent_id = ivalues['parentID']        
                
                    parent = root.find(arch_item.parent_id)
                    if parent: 
                        arch_item.parent = parent
                        parent.children.add(arch_item)
                        
                
print(f"Root: {len(root.children)} Children")
for space in root.children:
    print(f" * {space}: {len(space.children)} Children")
    for elem in space.children:
        print(f"  **  {elem}: {len(elem.children)} Children")