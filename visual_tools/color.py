'''
Description: 
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2024-01-02 16:22:43
LastEditors: ShuaiLei
LastEditTime: 2024-01-02 17:00:35
'''
class Color:
    def __init__(self) -> None:
        pass
        
    
    def segmentation_color_map(self):
        pass


    def catname2catid(self, catname):
        cat_nameTocat_id = {"C1": 0, "C2": 1, "C3": 2, "C4": 3, "C5": 4, "C6": 5, "C7": 6, 
                            "T1": 7, "T2": 8, "T3": 9, "T4": 10, "T5": 11, "T6": 12, "T7": 13, "T8": 14, "T9": 15, "T10": 16, "T11": 17, "T12": 18,
                            "L1": 19, "L2": 20, "L3": 21, "L4": 22, "L5": 23}
        catid = cat_nameTocat_id[catname]
        return catid
 
    
    def catid2rgb(self, catid):
        """
        Converts a label index to a color. 
        :param label: The label index.
        :return: RGB color as a list.
        """
        colormap = [[255, 0, 0], [0, 205, 0], [0, 0, 255], [0, 255, 255],
            [255, 0, 255], [255, 127, 0], [0, 100, 0], [138, 43, 226],
            [139, 35, 35], [0, 0, 128], [139, 139, 0], [255, 62, 150],
            [139, 76, 57], [0, 134, 139], [205, 104, 57], [191, 62, 255],
            [0, 139, 69], [199, 21, 133], [205, 55, 0], [32, 178, 170],
            [106, 90, 205], [255, 20, 147], [69, 139, 116], [72, 118, 255],
            [205, 79, 57], [0, 0, 205], [139, 34, 82], [139, 0, 139],
            [238, 130, 238], [139, 0, 0]]
        color = colormap[catid % len(colormap)]
        return color