# TODO allow text for be written at an angle and determine it size then
import os
from epyseg.settings.global_settings import set_UI # set the UI to be used py qtpy
set_UI()
from epyseg.draw.shapes.Position import Position
from qtpy import QtCore
from qtpy.QtCore import QPointF, QRect
from qtpy.QtGui import QTextDocument, QTextOption
from qtpy.QtGui import QPainter, QImage, QColor, QFont, QBrush, QPen
from qtpy.QtCore import QRectF, QSizeF,QPointF
import sys
from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication
from epyseg.draw.shapes.rectangle2d import Rectangle2D
# log errors
from epyseg.tools.logger import TA_logger
logger = TA_logger()

class TAText2D(Rectangle2D):

    # TODO add bg to it so that it can be drawn
    def __init__(self, text=None, doc=None, opacity=1.,x=0, y=0, fill_color=None, color=None, placement=Position(), *args, **kwargs):
        if doc is not None and isinstance(doc, QTextDocument):
            self.doc = doc
            self.doc.setDocumentMargin(0)  # important so that the square is properly placed
            self.text = self.doc.toHtml()
        else:
            self.doc = QTextDocument()
            self.doc.setDocumentMargin(0) # important so that the square is properly placed

            textOption = self.doc.defaultTextOption()
            textOption.setWrapMode(QTextOption.NoWrap)
            self.doc.setDefaultTextOption(textOption)

            if text is not None:
                self.doc.setHtml(text)
            self.text = text
        # self.isSet = True
        self.doc.adjustSize()
        size = self.getSize()
        super(TAText2D, self).__init__(x, y, size.width(), size.height())
        self.opacity = opacity
        self.immutable=True
        self.line_style = None # useless just for compat with other shapes
        if not isinstance(placement, Position):
            placement = Position(placement)
        self.placement = placement
        self.fill_color = fill_color
        self.color = color


    def set_opacity(self, opacity):
        self.opacity = opacity

    def setText(self, html):
        self.doc.setHtml(html)
        self.doc.adjustSize()
        size = self.getSize()
        self.setWidth(size.width(), size.height())
        self.text = html

    def setDoc(self, doc):
        self.doc = doc
        self.doc.setDocumentMargin(0)
        self.doc.adjustSize()
        size = self.getSize()
        self.setWidth(size.width())
        self.setHeight( size.height())
        self.text = self.getHtmlText()

    def draw(self, painter, draw=True, parent=None):
        if draw:
            painter.save()

            painter.setPen(Qt.NoPen)
            painter.setBrush(Qt.NoBrush)

            # Get the current clip rect of the painter
            # current_clip_rect = painter.clipBoundingRect()
            # print('current_clip_rect',current_clip_rect)

            # print('self.placement, self.placement.isEmpty()',self.placement, self.placement.isEmpty())

            if self.placement is not None and not self.placement.isEmpty():
                # painter.setClipRect(self.getRect(scale=True)) # in fact this is needed to get text to work!!! # DO NOT DO THIS OTHERWISE THE TEXT IS NOT CLIPPED WHICH IS NOT WHAT I WANT!!!!
                # if text --> need center v or h --> TODO
                rect_to_plot = self.getRect(scale=True)
            else:
                rect_to_plot = self.getRect()

                if parent is not None and parent.scale is not None and parent.scale != 1:
                    rect_to_plot = QRectF(rect_to_plot.x() / parent.scale, rect_to_plot.y() / parent.scale, rect_to_plot.width() / parent.scale,rect_to_plot.height() / parent.scale)

                # print('rect_to_plot', rect_to_plot)
                if parent is not None:
                    rect_to_plot = rect_to_plot.translated(parent.topLeft())
                # print('rect_to_plot2',rect_to_plot)

            #DEBUG
            if False:

                painter.setPen(QtCore.Qt.red)
                painter.drawRect(rect_to_plot)

            # do not move this, this is where the fill color should be applied
            if self.fill_color:
                # if isinstance(self.fill_color, QColor):
                #     self.fill_color = self.fill_color.rgb() & 0xFFFFFF

                # print(self, self.fill_color, 'inside drawing')

                # somehow the rect pos is completely wrong

                # painter.setPen(QtCore.Qt.red)
                painter.setBrush(QBrush(QColor(self.fill_color)))
                painter.drawRect(rect_to_plot)


            if self.theta is not None and self.theta != 0:
              # I have added support for rotation to that maybe I will need something smarter if rotation 90 degrees or flips and images no same width and height
              painter.translate(rect_to_plot.center())
              painter.rotate(self.theta)
              painter.translate(-rect_to_plot.center())

            # if True: #TODO remove that debug only
            #     painter.drawRect(rect_to_plot)

            # if self.opacity is not None:
            # painter.setOpacity(self.opacity)

            # if False:
            painter.translate(rect_to_plot.x(), rect_to_plot.y())


            if False:
                text_width = self.doc.documentLayout().documentSize().width()
                text_height = self.doc.documentLayout().documentSize().height()
                # rect_of_doc = self.doc.documentRect()
                painter.setClipRect(QRectF(rect_to_plot.x(), rect_to_plot.y(),min(text_width, rect_to_plot.width()),min(text_height, rect_to_plot.height())))



            # painter.translate(self.x()+self.width()/2., self.y()+self.height()/2.) # if I do that the square and the

            # here I need a cliprect of just the size of the stuff and not even that but the intersection with the parent

            self.doc.drawContents(painter)



            painter.restore()
            # maybe activate this upon debug
            # painter.save()
            # painter.setPen(QtCore.Qt.red)
            # painter.drawRect(self)
            # painter.restore()

    # def set_to_scale(self, factor): # this object should not be rescalable
        # raise Exception('this should not be called --> this creates a bug because the size fo this object is immutable')
        # self.scale = 1

    def boundingRect(self): # is that ok also
        return self

    def getSize(self): # is that ok ???
        return self.doc.size()

    def getWidth(self):
        return self.boundingRect().width()

    def getHeight(self):
        return self.boundingRect().height()

    def setText(self, text):
        self.doc.setHtml(text)
        size = self.size()
        self.setWidth(size.width(), size.height())

    def sync_text(self): # TODO always make sure to call this whenever a change to the text is made -−> will ease the serialization
        self.text = self.getHtmlText()

    # def getRect(self,*args, **kwargs):
    #     print('self.scale of the text', self.scale)
    #
    #     # if args or kwargs:
    #     return QRectF(self.x(), self.y(), self.width(), self.height())

    # def __getstate__(self):
    #     # Return a dictionary containing the state of the object
    #     return {'text': self.getHtmlText()}
    #
    # def __setstate__(self, state):
    #     # Set the state of the object from the dictionary
    #     self.setText(state['text'])

    # shall I rather compute its size including the roitation so that it never gets truncated --> that does make sense -−> need compute the bounds of the rotated stuff
    # and the incompressible size should also depend on that

    # def getIncompressibleWidth(self):
    #     # TODO in fact take the rotated size --> much smarter here --> see how I can do
    #     return self.width()
    #
    # def getIncompressibleHeight(self):
    #     return self.height()
    #
    # def get_incompressible_size(self, axis=None):
    #     # if True:
    #     #     return self.width()
    #     # if self.theta is not None:
    #         # get width and or height
    #     if axis:
    #         if axis == 'X':
    #             return self.getIncompressibleWidth()
    #         else:
    #             return self.getIncompressibleHeight()

    def setTopLeft(self, *args):
        if args:
            # cur_top_left = self.topLeft()
            # print('cur_top_left', cur_top_left, args)
            if len(args)==1:
            #     # assume a QpointF
                self.moveTo(args[0].x(), args[0].y())
            elif len(args) == 2:
                self.moveTo(QPointF(args[0], args[1]))
            # self.update_bounds()
            # elif len(args)==2:
            #     for img in self.content:
            #         img.moveTopLeft(QPointF(args[0], args[1]))
            # else:
            #     # logger.error('invalid args for top left')
            #     print('invalid args for top left')


    # def set_P1(self, *args):
    #     if not args:
    #         logger.error("no coordinate set...")
    #         return
    #     if len(args) == 1:
    #         self.moveTo(args[0].x(), args[0].y())
    #     else:
    #         self.moveTo(QPointF(args[0], args[1]))
    #
    # def get_P1(self):
    #     return QPointF(self.x(), self.y())

    def getPlainText(self):
        return self.doc.toPlainText()

    def getHtmlText(self):
        return self.doc.toHtml()

    def __repr__(self):
        class_name = type(self).__name__
        memory_address = hex(id(self))
        return f"{class_name}-{memory_address}"

if __name__ == '__main__':
    # this could be a pb ...
    app = QApplication(sys.argv)# IMPORTANT KEEP !!!!!!!!!!!

    # window = MyWidget()
    # window.show()

    # ça marche car ça override la couleur par defaut du truc
    # c'est parfait et 2000X plus facile que ds java --> cool

    html = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Font Face</title>
  </head>
  <body>
    <font color="red">
      <font face="Symbol" size="5">Symbol</font><br />
      <font face="Times New Roman" size="5">Times New Roman</font><br />
      <font face="Verdana" size="5">Verdana</font><br />
      <font face="Comic Sans MS" size="5">Comic Sans MS</font><br />
      <font face="WildWest" size="5">WildWest</font><br />
      <font face="Bedrock" size="5">Bedrock</font><br />
    </font>
  </body>
</html>
'''

    # html = "<font color=blue size=24>this is a test<sup>2</sup><br></font><font color=green size=12>continued<sub>1</sub><br></font><font color=white size=12>test greek <font face='Symbol' size=32>a</font> another &alpha;<font face='Arial' color='Orange'>I am a sentence!</font>"
    text = TAText2D(html)

    # hexagon.append(QPointF(10, 20))
    print(text)

    # print(hexagon.translate(10, 20)) # why none ???
    # translate and so on can all be saved...

    image = QImage('/E/Sample_images/sample_images_PA/mini/focused_Series012/handCorrection.png')
    # image = QImage(QSize(400, 300), QImage.Format_RGB32)
    painter = QPainter()
    painter.begin(image)
    # painter.setOpacity(0.3);
    painter.drawImage(0, 0, image)
    painter.setPen(QtCore.Qt.blue)
    text.opacity = 0.7
    painter.translate(10, 20)
    painter.setPen(QColor(168, 34, 3))

    text.draw(painter) # ça marche pourrait overloader ça avec du svg

    painter.drawRect(text)# try to draw the bounds

    # painter.setPen(QtCore.Qt.green)
    # painter.setFont(QFont('SansSerif', 50))


    painter.setFont(QFont('Decorative', 10))
    painter.drawText(256, 256, "this is a test")

# nothing works it just doesn't draw for unknown reason ????
#     painter.drawText(QRect(60,60,256,256), Qt.AlignCenter, "this is a test")

    painter.setPen(QtGui.QColor(0, 255, 255)) # colors are weird !!!
    # painter.drawText(20, 20, "MetaGenerator") # fait planter le soft --> pkoi exit(139) ...
    painter.drawText(QRect(60,60,256,256), Qt.AlignCenter, "Text centerd in the drawing area")

    # painter.drawText(QRect(100, 100, 200, 100), "Text you want to draw...");
    print('here')
    painter.end()

    # image = QImage(QSize(400, 300), QImage::Format_RGB32);
    # QPainter
    # painter( & image);
    # painter.setBrush(QBrush(Qt::green));
    # painter.fillRect(QRectF(0, 0, 400, 300), Qt::green);
    # painter.fillRect(QRectF(100, 100, 200, 100), Qt::white);
    # painter.setPen(QPen(Qt::black));


    # painter.save()
    # painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
    # painter.eraseRect(r)
    # painter.restore()
    print('saving', '/E/trash//test_pyQT_draw_text.png')
    image.save('/E/trash/test_pyQT_draw_text.png', "PNG")


    # split text and find bounding rect of the stuff --> so that it is well positioned
    # or do everything in svg and just show what's needed ???

    #pas mal TODO faire une classe drawsmthg qui dessine n'importe quelle forme que l'on lui passe avec des parametres de couleur, transparence, ...

    # tt marche aps mal ça va très vite
    sys.exit(0)
