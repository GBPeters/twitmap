import tkMessageBox
from Tkinter import Frame, Button, Entry, StringVar, Label, DISABLED, NORMAL

from twitterharvest import HarvestThread


class TwitGUI(Frame):
    """
    GUI Class
    """

    def __init__(self):
        """
        Public constructor
        """
        Frame.__init__(self)
        self.latvar1 = StringVar()
        self.lonvar1 = StringVar()
        self.latvar2 = StringVar()
        self.lonvar2 = StringVar()
        self.n = StringVar()
        self._setDefaults()
        self.label1 = Label(self, text="Lower Left Lat, Lon:")
        self.latBox1 = Entry(self, textvariable=self.latvar1)
        self.lonBox1 = Entry(self, textvariable=self.lonvar1)
        self.label2 = Label(self, text="Upper Right Lat, Lon:")
        self.latBox2 = Entry(self, textvariable=self.latvar2)
        self.lonBox2 = Entry(self, textvariable=self.lonvar2)
        self.labelN = Label(self, text="Number of Tweets:")
        self.nBox = Entry(self, textvariable=self.n)
        self.button = Button(self, command=self._run, text="Harvest!")

        self.label1.grid(row=0, column=0)
        self.latBox1.grid(row=0, column=1)
        self.lonBox1.grid(row=0, column=2)
        self.label2.grid(row=1, column=0)
        self.latBox2.grid(row=1, column=1)
        self.lonBox2.grid(row=1, column=2)
        self.labelN.grid(row=2, column=0)
        self.nBox.grid(row=2, column=1)
        self.button.grid(row=2, column=2)

        self.grid()

    def _setDefaults(self):
        """
        Private method resets values to defaults (Greater New York)
        :return: None
        """
        self.latvar1.set("40")
        self.latvar2.set("41")
        self.lonvar1.set("-74")
        self.lonvar2.set("-73")
        self.n.set("10")

    def _run(self):
        """
        Private method checks values and starts Twitter harvest.
        Called on button click
        :return: None
        """
        try:
            lat1 = float(self.latvar1.get())
            lon1 = float(self.lonvar1.get())
            lat2 = float(self.latvar2.get())
            lon2 = float(self.lonvar2.get())
            n = int(self.n.get())
            assert -90 <= lat1 <= 90
            assert -90 <= lat2 <= 90
            assert -180 <= lon1 <= 180
            assert -180 <= lon2 <= 180
            assert n > 0
        except Exception, e:
            print e.message
            tkMessageBox.showerror("Invalid Input", "Please enter valid coordinates and number of tweets.")
            self._setDefaults()
        else:
            bbox = (lon1, lat1, lon2, lat2)
            hthread = HarvestThread(bbox, n, self.enable)
            self.button["state"] = DISABLED
            hthread.start()
            tkMessageBox.showinfo("Harvest started", "Map will load when harvest finishes.")

    def enable(self):
        self.button["state"] = NORMAL


def runApp():
    """
    Main Function
    :return: None
    """
    gui = TwitGUI()
    gui.mainloop()


if __name__ == "__main__":
    runApp()
