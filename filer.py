#!/usr/bin/env python
import gtk
import os
from os import listdir
from os.path import isfile, isdir, join


class DragImage(gtk.Image):

    spacerX = 16
    spacerY = 16

    def __init__(self, image, layout, fpath, fname):
        gtk.Image.__init__(self)
        self.drag = False
        self.drag_x = 0
        self.drag_y = 0
        self.layout = layout
        self.x = DragImage.spacerX
        self.y = DragImage.spacerY
        self.set_from_file(image)
        self.fpath = fpath
        self.fname = fname
        self.label = gtk.Label(fname)
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000000'))
        self.event_box = gtk.EventBox()
        self.event_box.set_visible_window(False)
        self.event_box.add(self)
        self.event_box.add_events(
            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)
        self.event_box.connect("button-press-event", self.click)
        self.event_box.connect("button-release-event", self.release)
        self.event_box.connect("motion-notify-event", self.mousemove)
        self.layout.put(self.label, DragImage.spacerX, DragImage.spacerY + 16)
        self.layout.put(self.event_box, DragImage.spacerX, DragImage.spacerY)
        DragImage.spacerX += 32

    def click(self, widget, event):
        self.drag = True
        self.drag_x = event.x
        self.drag_y = event.y
        if event.type == gtk.gdk.BUTTON_PRESS:
            print("single click on:", self.fname)
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            if os.path.isdir(os.path.join(self.fpath, self.fname)):
                DragImage.spacerX = 16
                window(self.fpath + "/" + self.fname)

    def release(self, widget, event):
        self.drag = False

    def mousemove(self, widget, event):
        if self.drag:
            self.layout.move(
                self.event_box, self.x + int(event.x - self.drag_x), self.y + int(event.y - self.drag_y))
            self.x, self.y = self.layout.child_get(self.event_box, 'x', 'y')
            self.layout.move(self.label, self.x, self.y + 16)


class window(object):

    def __init__(self, path):
        self.path = path
        win = gtk.Window()
        win.set_title(path.split('/')[-1])
        layout = gtk.Layout()
        win.add(layout)

        # win.connect("delete-event", gtk.main_quit)
        backdrop = gtk.image_new_from_file("pattern.png")
        layout.put(backdrop, 0, 0)

        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                print("file =", name)
                DragImage('file.png', layout, path, name)
            if os.path.isdir(os.path.join(path, name)):
                print("dire =", name)
                DragImage('directory.png', layout, path, name)

        win.show_all()


window("test-tree")
gtk.main()
