"""
poppler- folder to be extracted and then path to be added to env system variable.(https://blog.alivate.com.au/poppler-window/)
easyocr works with opencv-python(4.5.2.52)
easyocr works with torch, torchvision, torchaudio (gpu version CU117)
"""

import easyocr
from functools import cmp_to_key




class OCR:
    reader = easyocr.Reader(["en", 'hi'])

    # it will return the result extracted by OCR (all the OCR related functionality are here)
    def get_textBoxes(self, img):
        results = self.reader.readtext(img, detail=1, paragraph=False, width_ths=0.1)
        return results

    def get_texts(self, img):
        result=self.word_natural_sort(img)
        image_text = ""
        for res in result:
            image_text += res[1] + " "
        return image_text

    # this function will sort the words in their natural order.
    def word_natural_sort(self,img):
        bbox = self.get_textBoxes(img)
        # taking only bbox coordinates and text of every Bbox from extracted result.
        # It returns an array of top-left coordinate and text of every Bbox.
        results=[]
        for tb in bbox:
            results.append((tb[0],tb[1]))

        results=sorted(results, key=cmp_to_key(self.__comparator))
        return results

    # this comparator is used by word_natural_sort method while sorting.
    def __comparator(self,a,b):
        if a[0][0][1]<b[0][0][1]:
            return 1
        elif a[0][0][1]==b[0][0][1]:
            return a[0][0][0]<b[0][0][0]
        return 0

    # this function is used to find texts inside a rectangle section on the image
    # here sorted_list is the array of text boxes in a image sorted in natural order of reading
    # here (x1,y1) is the top left coordinate of rectangle section
    # here (x2,y2) is the bottom right coordinate of rectangle section
    def find_texts(self,sorted_list,x1,y1,x2,y2):
        result = ""
        for item in sorted_list:
            center_point=self.find_center_point(item[0])
            if(center_point[0] in range(x1,x2) and center_point[1] in range(y1,y2)):
                result+=item[1]+" "
        return result

    # it find the center point of a rectangle with its 4 coordinates
    def find_center_point(self,points):
        x1=points[0][0]
        y1=points[0][1]
        x2 = points[2][0]
        y2 = points[2][1]
        return [(x1 + x2)/2, (y1 + y2)/2]






# Driver code goes here............................................................................................


# img=glob.glob(r'test3.jpg')


# obj1=OCR()

#print(obj1.word_natural_sort(img[0]))
#print(obj1.get_texts(img[0]))
#sorted_list=obj1.word_natural_sort(img[0])
#print(sorted_list)
#print(obj1.find_texts(sorted_list,222,150,1052,369))

