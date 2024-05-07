from builtins import int
from epyseg.settings.global_settings import set_UI  # set the UI to be used py qtpy
set_UI()
import xml.etree.ElementTree as ET
import xml.dom.minidom
from epyseg.draw.shapes.txt2d import TAText2D
from epyseg.draw.shapes.Position import Position
# from epyseg.serialization.tools import deserialize_to_dict

def object_to_xml(obj, element=None, keys_to_ignore=['img','renderer','doc','qimage'], is_list=False):
    obj_dict = None
    if element is None:
        # if is_list:
        #     element = ET.Element("list")
        # else:
            element = ET.Element(type(obj).__name__)

    if hasattr(obj, 'to_dict'):
        obj_dict = obj.to_dict()
    elif isinstance(obj, (list, tuple)):
        if is_list:
            for item in obj:
                child = ET.SubElement(element, type(item).__name__)
                object_to_xml(item, child)
        else:
            obj_dict = [object_to_xml(item) for item in obj]
    elif isinstance(obj, dict):
        obj_dict = {k: object_to_xml(v) for k, v in obj.items()}
    elif isinstance(obj, (str, int, float, bool)):
        obj_dict = obj
    else:
        obj_dict = obj.__dict__
    if isinstance(obj_dict, dict):
        for key, value in obj_dict.items():
            if keys_to_ignore and key in keys_to_ignore:
                continue

            child = ET.SubElement(element, key)

            if isinstance(value, TAText2D):
                child.text = value.getHtmlText()
            elif isinstance(value, Position): # force serialization of Position as a string because it is much better
                child.text = str(value)
            elif isinstance(value, (list, tuple)):

                    for item in value:
                        grandchild = ET.SubElement(child, type(item).__name__)
                        object_to_xml(item, grandchild) # --> this makes an infinite loop but just with the Image2D with annotation = []
            # elif hasattr(value, '__dict__'):
            #     object_to_xml(value, child)
            else:
                if isinstance(value, str) and not key=='coords_as_list':
                    child.text = f'""{str(value)}""'
                else:
                    child.text = str(value)
    else:
        if obj_dict:
            element.text = str(obj_dict)
        else:
            element.text = None

    rough_string = ET.tostring(element, encoding='unicode', method='xml', xml_declaration=False)
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_objects_from_dict(objects_dict):
    annotations = []
    for obj_type, parameters in objects_dict.items():
        try:
            if isinstance(parameters, list): # if there are many objects then one deserializes then all
                for parameter in parameters:
                    annotations.append(create_object(obj_type, parameter))
            else:
                annotations.append(create_object(obj_type, parameters))
        except:
            print(f'ERROR deserialization: {obj_type} with parameters {parameters}') # ok that is my error when there are many objects of the same type
    return annotations


def clone_object(objects, auto_unpack_if_single=True):
    clones = []
    if not objects:
        return clones
    if not isinstance(objects,list):
        objects=[objects]
    for object in objects:
        xml_string = object_to_xml(object)
        # get the class of the instance
        instance_class = type(object)
        # get the name of the class
        class_name = instance_class.__name__
        clones.append(create_object(class_name, deserialize_to_dict(xml_string)))
    if auto_unpack_if_single and len(clones)==1:
        return clones[0]
    return clones

def create_object(object_type,properties):
    from epyseg.draw.shapes.circle2d import Circle2D
    from epyseg.draw.shapes.image2d import Image2D
    from epyseg.draw.shapes.ellipse2d import Ellipse2D
    from epyseg.draw.shapes.freehand2d import Freehand2D
    from epyseg.draw.shapes.rectangle2d import Rectangle2D
    from epyseg.draw.shapes.line2d import Line2D
    from epyseg.draw.shapes.point2d import Point2D
    from epyseg.draw.shapes.polygon2d import Polygon2D
    from epyseg.draw.shapes.polyline2d import PolyLine2D
    from epyseg.draw.shapes.scalebar import ScaleBar
    from epyseg.draw.shapes.square2d import Square2D
    from personal.FigGen_EzFig2.group import Group

    if  object_type == list.__name__:
        return create_objects_from_dict(properties)
    elif object_type == Image2D.__name__:
        # I can code custom shit in there
        # if not 'args' in properties and 'filename' in properties:
        #     properties['args']=properties['filename']
        # print('trying to create an image', properties)
        return Image2D(**properties)
    elif object_type == Line2D.__name__:
        return Line2D(**properties)
    elif object_type == TAText2D.__name__:
        return TAText2D(**properties)
    elif object_type == Point2D.__name__:
        return Point2D(**properties)
    elif object_type == Ellipse2D.__name__:
        return Ellipse2D(**properties)
    elif object_type == Circle2D.__name__:
        return Circle2D(**properties)
    elif object_type == Freehand2D.__name__:
        return Freehand2D(**properties)
    elif object_type == Polygon2D.__name__:
        return Polygon2D(**properties)
    elif object_type == PolyLine2D.__name__:
        return PolyLine2D(**properties)
    elif object_type == Rectangle2D.__name__:
        return Rectangle2D(**properties)
    elif object_type == Square2D.__name__:
        return Square2D(**properties)
    elif object_type == ScaleBar.__name__:
        return ScaleBar(**properties)
    elif object_type == Group.__name__:
        return Group(**properties)
    else:
        print(f'unknown type for deserialization {object_type}')


def is_float(str):
    try:
        float(str)
        return True
    except:
        return False


def deserialize_to_dict(xml_string):
    root = ET.fromstring(xml_string)
    return element_to_dict(root)


def element_to_dict(element):
    properties = {}

    for child in element:
        tag = child.tag

        if list(child):  # check if current element has any sub-elements
            # Recursively parse sub-elements and store the resulting dictionary
            value = element_to_dict(child)
        else:
            value = child.text

        if value is None:
            value = {}
            for grandchild in child:
                if grandchild.tag == 'metadata':
                    value = eval(grandchild.text)
                elif grandchild.tag == 'positions':
                    print('INSIDE POSITIONS', grandchild.text)
                    value[grandchild.tag] = eval(grandchild.text)
                elif grandchild.tag == 'annotations':
                    print('inside annotations', grandchild)
                else:
                    value[grandchild.tag] = element_to_dict(grandchild)
        else:
            if isinstance(value, dict):
                # If value is a dictionary, leave it as is
                # print('ignored', tag, value)
                # --> the annotations are ignored and they should not
                # print('value ignored', tag, len(value)) # this is the dict of the values of the annotations --> somehow I need to take them
                pass
            elif value in ['None', 'True', 'False']:
                if value == 'None':
                    value = None
                elif value == 'True':
                    value = True
                elif value == 'False':
                    value = False
            elif isinstance(value, str) and value.startswith('""') and value.endswith('""'):
                value = value[2:-2]
            elif isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                value = eval(value)  # recreate the dict from string
            elif value.isdigit():
                value = int(value)
            elif is_float(value):
                value = float(value)

        # if tag == 'annotations':
        #     print('annotations--> ',tag, value)
        # properties[tag] = value # if it contains it already it will override it --> that is the error
        # Check if tag already exists in properties
        if tag in properties:
            # If tag already exists, check if the value is a list
            if not isinstance(properties[tag], list):
                # If the value is not a list, convert it to a list
                properties[tag] = [properties[tag]]
            # Append the new value to the list
            properties[tag].append(value)
        else:
            # If tag does not exist, add it with the new value
            properties[tag] = value

    return properties


if __name__ == '__main__':
    # from epyseg.serialization.tools import object_to_xml, create_object
    from epyseg.settings.global_settings import set_UI  # set the UI to be used py qtpy

    set_UI()
    from epyseg.draw.shapes.image2d import Rectangle2D
    from qtpy.QtCore import QRect, Qt, QRectF
    from epyseg.draw.shapes.image2d import Image2D
    import numpy as np
    import sys
    from qtpy.QtWidgets import QApplication
    from personal.FigGen_EzFig2.group import Group

    app = QApplication(sys.argv)  # IMPORTANT KEEP !!!!!!!!!!!

    if True:
        img0 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test_asym_size.png')
        img1 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')

        img3 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')
        img4 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')

        grp = Group(img3, img4)

        lst = [img0, img1, grp]

        # try to serialize this stuff --> this can be seen as an image --> TODO
        xml_string = object_to_xml(lst, is_list=True)

        # print(xml_string)

        properties = deserialize_to_dict(xml_string)
        # print(properties)
        clone = create_object(list.__name__, properties)

        print(clone)

        # now try to deserialize it

        sys.exit(0)

    if True:

        if False:
            rect = Rectangle2D(10, 16, 200, 512)
            obj_type = Rectangle2D.__name__

        if False:
            rect = Ellipse2D(10, 16, 200, 512)
            obj_type = Ellipse2D.__name__

        if False:
            rect = Circle2D(10, 16, 200)
            obj_type = Circle2D.__name__

        if False:
            rect = Point2D(10, 16)
            obj_type = Point2D.__name__

        if False:
            rect = Line2D(10, 16, 200, 512)
            obj_type = Line2D.__name__

        if False:
            rect = Polygon2D(100, 100, 110, 100, 110, 120, 10, 120, 100, 100)
            obj_type = Polygon2D.__name__

        if False:
            rect = PolyLine2D(100, 100, 110, 100, 110, 120, 10, 120, 100, 100)
            obj_type = PolyLine2D.__name__

        if False:  # no clue why they are ot equal because they seem to be...
            rect = Square2D(10, 16, 200)
            obj_type = Square2D.__name__

        if False:
            rect = Freehand2D(100, 100, 110, 100, 110, 120, 10, 120, 100, 100)
            obj_type = Freehand2D.__name__

        if False:
            rect = TAText2D(
                'this is a test of your system')  # they are nbot equal because of the doc --> no big deal and expected
            obj_type = TAText2D.__name__

        if False:
            rect = TAText2D('this is a test of your system',
                            placement='top-left')  # they are nbot equal because of the doc --> no big deal and expected
            obj_type = TAText2D.__name__

        if False:
            rect = ScaleBar(10, legend='10µm',
                            placement='top-left')  # they are nbot equal because of the doc --> no big deal and expected
            obj_type = ScaleBar.__name__

        if False:
            rect = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')
            obj_type = Image2D.__name__

        test_text = '''
                </head><body style=" font-family:'Comic Sans MS'; font-size:22pt; font-weight:400; font-style:normal;">
                <p style="color:#00ff00;"><span style=" color:#ff0000;">toto</span><br />tu<span style=" vertical-align:super;">tu</span></p>
                '''
        test_text2 = '''
                    </head><body style=" font-family:'Comic Sans MS'; font-size:22pt; font-weight:400; font-style:normal;">
                    <p style="color:#00ff00;"><span style=" color:#0000ff;">tititi</span>
                    '''
        test_text3 = '''
                    </head><body style=" font-family:'Comic Sans MS'; font-size:22pt; font-weight:400; font-style:normal;">
                    <p style="color:#00ff00;"><span style=" color:#00ffff;">tata</span>
                    '''

        if False:
            img0 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test_asym_size.png')
            img1 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')
            rect = img1
            obj_type = Image2D.__name__

            if True:
                if True:
                    img1.border_size = 3  # make sure it displays an edge
                    # img1.annotations = []
                    img1.annotations.append(img0)  # add an inset

                if True:
                    # img1.setLettering(TAText2D(text=test_text))
                    img1.annotations.append(TAText2D(text=test_text, placement='top-left'))
                    img1.annotations.append(TAText2D(text=test_text2, placement='top-left'))
                    img1.annotations.append(Line2D(0, 0, img1.width() / 2, img1.height() / 2, stroke=3, color=0xFF00FF))
                    img1.annotations.append(Rectangle2D(128, 128, 64, 128, stroke=3, color=0xFF00FF))
                    img1.annotations.append(Point2D(img1.width() / 2, img1.height() / 2, stroke=6, color=0xFF00FF))
                    img1.annotations.append(
                        Ellipse2D(img1.width() / 2 - img1.width() / 8, img1.height() / 2 - img1.height() / 12,
                                  img1.width() / 4, img1.height() / 6, stroke=3, color=0xFF00FF))
                    img1.annotations.append(
                        Circle2D(img1.width() / 2 - img1.width() / 10, img1.height() / 2 - img1.height() / 10,
                                 img1.width() / 5, stroke=3, color=0xFF00FF))
                    img1.annotations.append(
                        Polygon2D(100, 100, 110, 100, 110, 120, 10, 120, 100, 100, color=0x0000FF, fill_color=0x00FFFF,
                                  stroke=2))
                    img1.annotations.append(PolyLine2D(10, 16, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
                    img1.annotations.append(PolyLine2D(10, 16, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
                    img1.annotations.append(Square2D(72.5, 151.5, 30, stroke=3))
                    # img1.annotations.append(Freehand2D(10, 10, 20, 10, 20, 30, 288, 30, color=0xFFFF00, stroke=3))
                    img1.annotations.append(
                        Freehand2D(75, 25, 116.50, 50, 116.50, 100, 75, 125, 33.50, 100, 33.50, 50, color=0xFFFF00,
                                   stroke=3))  # a beautiful hexagon !!!
                    # try a floating text
                    img1.annotations.append(TAText2D(x=img1.width() / 2, y=img1.height() / 2,
                                                     text='<font color="#FFFF00">free floating text</font>'))
                    img1.annotations.append(ScaleBar(30, '<font color="#FF00FF">right µm</font>',
                                                     placement='top-right'))  # here I specify the bar to be top right specifically

        if False:
            img0 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test_asym_size.png')
            img1 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')
            img1.annotations.append(TAText2D(text=test_text, placement='top-left'))
            img1.annotations.append(TAText2D(text=test_text2, placement='top-left'))
            img1.annotations.append(Line2D(0, 0, img1.width() / 2, img1.height() / 2, stroke=3, color=0xFF00FF))
            img1.annotations.append(Rectangle2D(128, 128, 64, 128, stroke=3, color=0xFF00FF))
            rect = Group(img0, img1)
            obj_type = Group.__name__

        rect.translate(120, 160)
        if isinstance(rect, Image2D):
            print('init Image', rect.img.shape)

        print('to_dict orig', rect.to_dict())

        # if True:
        #     print(type(rect.to_dict()['coords_as_list']), rect.to_dict()['coords_as_list'], rect.to_dict()['coords_as_list'][0])
        # all is ok --> error is somewhere else then

        print('orig', rect)

        print('orig rect', rect.getRect())

        xml_string = object_to_xml(rect)

        if False:
            print('#' * 20)
            print(xml_string)
            print('#' * 20)

        properties = deserialize_to_dict(xml_string)
        if False:
            print(properties)
            print(len(properties['annotations']))  # only 12 --> that is not the pb
            print(properties['annotations'])
            for elm, value in properties['annotations'].items():
                if elm == 'TAText2D':
                    print(elm, len(value), type(value), type(value[
                                                                 1]))  # value is a list of dict --> bingo I wil manage soon # ok so there are 14 stored in there and that is what I missed --> try to fix it -> this is a list so that is why I failed
                    # print(value)
                    for txt in value:  # why is first value None ???
                        print(txt)
                    print(value)
            sys.exit(0)

        clone = create_object(obj_type, properties)

        if isinstance(clone, Image2D):
            print('copy Image', clone.img)

        print('clone', clone)

        print('to_dict clone', clone.to_dict())
        print('clone rect', clone.getRect())

        print('equal', rect == clone)

        print('types', type(rect), type(clone))

        try:
            print('initial', rect.x(), rect.y(), rect.width(), rect.height())  # all ok
            print('clone', clone.x(), clone.y(), clone.width(), clone.height())  # all 0
        except:
            pass  # no big deal if fails

        success = False
        try:
            print('equal dict', rect.__dict__ == clone.__dict__)
            success = rect.__dict__ == clone.__dict__
        except:
            print('skipping equal dict')

        if not success:
            for k1, v1 in rect.__dict__.items():
                for k2, v2 in clone.__dict__.items():
                    if k1 == k2:
                        if k1 in ['doc', 'img']:
                            continue
                        try:
                            if v1 != v2:
                                if isinstance(v2, Position):
                                    if str(v2) == str(v1):
                                        continue
                                print('not same values for', k1, v1, 'vs', v2, type(v1), type(v2))
                        except:
                            print(v1, 'vs', v2)

        xml_of_clone = object_to_xml(clone)
        print('serialization equality', xml_string == xml_of_clone)

        if False:
            if xml_string != xml_of_clone:
                print('#' * 30)
                print(xml_of_clone)
                print('#' * 30)

                import difflib

                # string1 = "This is the first string."
                # string2 = "This is the second string."

                diff = difflib.ndiff(xml_string.splitlines(), xml_of_clone.splitlines())

                print('difference:')
                print(" vs ".join(diff))
                # for dif in diff:
                #     print(dif)
                # print(diff)

        if isinstance(rect, Image2D):
            print('annitations nb', len(rect.annotations),
                  len(clone.annotations))  # 15 texts are missing --> the error is in deserialization because serilaization is ok

        sys.exit(0)

    if False:  # old
        # if this is a string --> make it save as '''value''' -−> unpack it --> maybe need an extra check for a count of the values or maybe use """ or maybe use something unique so that it does not compete with python such as two '' or two "" at beginning and at the end

        img1 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')
        img0 = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test_asym_size.png')
        test_text = '''
            </head><body style=" font-family:'Comic Sans MS'; font-size:22pt; font-weight:400; font-style:normal;">
            <p style="color:#00ff00;"><span style=" color:#ff0000;">toto</span><br />tu<span style=" vertical-align:super;">tu</span></p>
            '''
        test_text2 = '''
                </head><body style=" font-family:'Comic Sans MS'; font-size:22pt; font-weight:400; font-style:normal;">
                <p style="color:#00ff00;"><span style=" color:#0000ff;">tititi</span>
                '''
        test_text3 = '''
                </head><body style=" font-family:'Comic Sans MS'; font-size:22pt; font-weight:400; font-style:normal;">
                <p style="color:#00ff00;"><span style=" color:#00ffff;">tata</span>
                '''

        if True:
            if True:
                img1.border_size = 3  # make sure it displays an edge
                # img1.annotations = []
                img1.annotations.append(img0)  # add an inset

            if True:
                # img1.setLettering(TAText2D(text=test_text))
                img1.annotations.append(TAText2D(text=test_text, placement='top-left'))
                img1.annotations.append(TAText2D(text=test_text2, placement='top-left'))
                img1.annotations.append(TAText2D(text=test_text3, placement='top-left'))

                img1.annotations.append(TAText2D(text=test_text, placement='bottom-right'))
                img1.annotations.append(TAText2D(text=test_text2, placement='bottom-right'))
                img1.annotations.append(TAText2D(text=test_text3, placement='bottom-right'))

                img1.annotations.append(TAText2D(text=test_text, placement='bottom-left'))
                img1.annotations.append(TAText2D(text=test_text2, placement='bottom-left'))

                img1.annotations.append(TAText2D(text=test_text, placement='top-right'))
                img1.annotations.append(TAText2D(text=test_text2, placement='top-right'))

                img1.annotations.append(TAText2D(text=test_text, placement='center_h-center_v'))
                img1.annotations.append(TAText2D(text=test_text2, placement='center_h-center_v'))

                # print('TADAM',img1.width()/2., img1.height()/2.)
                img1.annotations.append(Line2D(0, 0, img1.width() / 2, img1.height() / 2, stroke=3, color=0xFF00FF))
                img1.annotations.append(Rectangle2D(128, 128, 64, 128, stroke=3, color=0xFF00FF))
                img1.annotations.append(Point2D(img1.width() / 2, img1.height() / 2, stroke=6, color=0xFF00FF))
                img1.annotations.append(
                    Ellipse2D(img1.width() / 2 - img1.width() / 8, img1.height() / 2 - img1.height() / 12,
                              img1.width() / 4, img1.height() / 6, stroke=3, color=0xFF00FF))
                img1.annotations.append(
                    Circle2D(img1.width() / 2 - img1.width() / 10, img1.height() / 2 - img1.height() / 10,
                             img1.width() / 5, stroke=3, color=0xFF00FF))
                img1.annotations.append(
                    Polygon2D(100, 100, 110, 100, 110, 120, 10, 120, 100, 100, color=0x0000FF, fill_color=0x00FFFF,
                              stroke=2))
                img1.annotations.append(PolyLine2D(10, 16, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
                img1.annotations.append(PolyLine2D(10, 16, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
                img1.annotations.append(Square2D(72.5, 151.5, 30, stroke=3))
                # img1.annotations.append(Freehand2D(10, 10, 20, 10, 20, 30, 288, 30, color=0xFFFF00, stroke=3))
                img1.annotations.append(
                    Freehand2D(75, 25, 116.50, 50, 116.50, 100, 75, 125, 33.50, 100, 33.50, 50, color=0xFFFF00,
                               stroke=3))  # a beautiful hexagon !!!

                # try a floating text
                img1.annotations.append(TAText2D(text='<font color="#FF0000">top left by coords</font>'))
                img1.annotations.append(TAText2D(x=img1.width() / 2, y=img1.height() / 2,
                                                 text='<font color="#FFFF00">free floating text</font>'))
                img1.annotations.append(
                    ScaleBar(30, '<font color="#FF00FF">10µm</font>'))  # default scale bar placement is bottom right
                img1.annotations.append(ScaleBar(30, '<font color="#FF00FF">right µm</font>',
                                                 placement='top-right'))  # here I specify the bar to be top right specifically
        # very good now try

        img1.scale = 0.5

        # print(img1.width())
        # print(img1.height())

        # print(same_img.__dict__)
        xml_string = object_to_xml(img1)

        print(xml_string)
        print('#' * 40)

        # xml_string = '''<?xml version="1.0" ?>
        # <Rectangle2D>
        #   <color>""16776960""</color>
        #   <fill_color>None</fill_color>
        #   <stroke>0.65</stroke>
        #   <opacity>1.0</opacity>
        #   <isSet>False</isSet>
        #   <scale>1</scale>
        #   <line_style>None</line_style>
        #   <theta>0</theta>
        #   <incompressible_width>0</incompressible_width>
        #   <incompressible_height>0</incompressible_height>
        #   <immutable>False</immutable>
        #   <__init_called__>True</__init_called__>
        # </Rectangle2D>'''

        # test ='16776960'

        # print(test.isdigit())
        # print(int(test)+1)

        properties = deserialize_to_dict(xml_string)
        if 'filename' in properties:
            properties['args'] = properties['filename']
        print('#' * 2000)
        print(properties)
        print('#-' * 2000)

        # rect = xml_to_object(xml_string)
        # print(rect.__dict__)

        # print(rect.__dict__ == same_img.__dict__)

        # plt.imshow(rect.img)
        # plt.show()

        rect = Image2D(**properties)
        print('testing keys', rect.__dict__.keys() == img1.__dict__.keys())

        # removing the image is required for that
        # rect.__dict__['img']=None
        # same_img.__dict__['img']=None

        try:
            print(rect.__dict__ == img1.__dict__)
        except:
            # Check all pairwise comparisons between the dictionaries
            for k1, v1 in rect.__dict__.items():
                for k2, v2 in img1.__dict__.items():
                    if k1 == k2:
                        try:
                            if v1 != v2 or abs(v1 - v2) > 1e-9:
                                if isinstance(v2, Position):
                                    if str(v2) == str(v1):
                                        continue

                                print('not same values for', k1, v1, 'vs', v2, type(v1), type(v2))
                                if k1 == 'annotations':
                                    # print(type(v1))
                                    # k1 = eval(v1)
                                    # print(type(k1))
                                    if v1:
                                        for key, val in v1.items():
                                            print(key, '-->', val)
                                            try:
                                                print(create_object(key, val))
                                            except:
                                                traceback.print_exc()
                                    # bingo -−> can be easy TODO too -−> do deserialize that too!!
                                # else:

                        except:
                            if not np.array_equal(v1, v2):
                                print('images', k1, 'not the same')
                        # if not np.array_equal(v1, v2):
                        #     print(f"Error: The '{k1}' arrays are not equal.")
                        #     print(f"Array 1: {v1}")
                        #     print(f"Array 2: {v2}")
                        #     print()
                        # pass
                    # else:
                    #     print(f"Error: The dictionaries have different keys: '{k1}' and '{k2}'.")

        '''
        there is a minor bug due to:

        'placement':<personal.FigGen_EzFig2.Position.Position object at 0x7fded71d1480>
        <placement>
            <positions>{'top': True, 'bottom': False, 'left': False, 'right': True, 'center_h': False, 'center_v': False}</positions>
        </placement>

        # see how I can fix that
        '''

        print(rect, img1)  # -> that rougly seems to work
        # --> see how to handle the things that need to be duplicated

        if False:
            test2 = Rectangle2D(
                QRectF(10, 0, 100, 256))  # the serialization is great but now I need to see how to reload the shit

            print(test2)

            if True:
                xml_string = object_to_xml(test2)

            rect = deserialize_rectangle2d(xml_string)
            print(rect.__dict__)

            print(rect)

            print(
                rect == test2)  # very good --> that works and that is cool --> these are really two objects but they are interchangeable
            print(test2.__dict__)

            print(test2.__dict__ == rect.__dict__)

        # print

#
#
# if __name__ == '__main__':
#     from epyseg.settings.global_settings import set_UI  # set the UI to be used py qtpy
#
#     set_UI()
#     from epyseg.draw.shapes.image2d import Rectangle2D
#     from qtpy.QtCore import QRect, Qt, QRectF
#
#     test2 = Rectangle2D(QRectF(10, 0, 100, 256)) # the serialization is great but now I need to see how to reload the shit
#     xml_version =object_to_xml(test2)
#     print(xml_version)
#
#     print('Deserialization')
#
#     # print(xml_to_object(xml_version))
#
#
#     if False:
#         from epyseg.draw.shapes.image2d import Image2D
#
#
#         same_img = Image2D('/E/Sample_images/EZF_SF_scientifig_EZFig/sample_images_svg/test.png')
#         same_img.scale = 0.5
#
#         print(same_img.width())
#         print(same_img.height())
#
#
#         # when it loops into position it should just get the position as a string
#
#
#         # see also how to handle the embedded images -> shall I store them separately or not
#         # can I use magic unique names to avoid repetitions ???
#
#
#
#         print(object_to_xml(same_img))
#
#
#         # try to reload it maybe


