from OCRmodule import OCR
from DLAmodule import DLA
from functools import cmp_to_key
import json




class DLA_OCR:
    ocr_obj = None
    dla_obj = None

    def __init__(self):
        self.ocr_obj = OCR()
        self.dla_obj = DLA()

    def get_extracted_result(self, img):
        dla_output = self.dla_obj.get_output(img)
        # sorting the dla output sections in natural order in image
        sorted_dla_output = self.section_natural_sort(dla_output)
        sorted_text_list = self.ocr_obj.word_natural_sort(img)
        result=[]
        for i in range(len(sorted_dla_output)):
            top_left_coor = sorted_dla_output[i][0][0]
            bottom_right_coor = sorted_dla_output[i][0][1]
            section_lable = sorted_dla_output[i][1]
            section_text = self.ocr_obj.find_texts(sorted_text_list,top_left_coor[0],top_left_coor[1],bottom_right_coor[0],bottom_right_coor[1])
            result.append((section_lable, section_text))

        return result


    def section_natural_sort(self,lst):
        lst = sorted(lst, key=cmp_to_key(self.__comparator))
        return lst

    # this comparator is used by section_natural_sort method while sorting.
    def __comparator(self, a, b):
        if a[0][0][1] < b[0][0][1]:
            return 1
        elif a[0][0][1] == b[0][0][1]:
            return a[0][0][0] < b[0][0][0]
        return 0

    def generate_extracted_json_file(self, img):
        dla_ocr_output=self.get_extracted_result(img)
        section_dict={}
        for i in range(len(dla_ocr_output)):
            section_dict[f'obj{i}'] = {'lable': dla_ocr_output[i][0], 'content': dla_ocr_output[i][1]}

        #json_result = json.dumps(section_dict)

        return section_dict









#Driver code goes here---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# obj=DLA_OCR()
#
#print(obj.generate_extracted_json_file('test4.jpeg'))










