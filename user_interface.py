import tkinter as tk
from tkinter import filedialog

class Setting:

    def __init__(self, root):
        self.root = root
        self.root.title(' Monitoring system settings ')
        self.init_gui()
        self.upload = False
    
    def get_mode(self):
        return self.mode.get()
    
    def get_critical_load(self):
        return self.critical_load.get()
    
    def get_sensor_interval(self):
        return self.sensor_interval.get()
    
    def get_camera(self):
        return self.camera.get()
    
    def get_crop(self):
        return self.crop.get()
    
    def get_crop_position(self):
        return self.crop_x.get(), self.crop_y.get(), self.crop_width.get(), self.crop_height.get()
    
    def get_scan_interval(self):
        return self.interval_day.get() * 1440 + \
                             self.interval_hour.get() * 60 + \
                             self.interval_min.get()
    
    def get_sender_email(self):
        return self.sender.get()
    
    def get_password(self):
        return self.password.get()
    
    def get_recipients(self):
        return self.recipients.get().split(',')
    
    def uploadAction(self, even=None):
        self.upload = True
        self.filename = filedialog.askopenfilename()
        return self.filename
    
    def create_top_frame(self):
        self.top_frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        self.top_frame.pack(side=tk.TOP)
        #top_title = tk.Label(self.top_frame, text='System configuration')
        #top_title.configure(font='Arial 20')
        #top_title.pack()
        
    def create_bottom_frame(self):
        self.bottom_frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        self.bottom_frame.pack(side=tk.BOTTOM)
        #bottom_title = tk.Label(self.bottom_frame, text='Scan and sensor settings')
        #bottom_title.configure(font='Arial 20')
        #bottom_title.pack()
        
    def create_mode_frame(self):
        mode_frame = tk.Frame(self.top_frame, relief=tk.SUNKEN, borderwidth=1)
        mode_frame.pack(side=tk.LEFT)
        mode_title = tk.Label(mode_frame, text='Mode setting')
        mode_title.configure(font='Arial 15')
        mode_title.grid(row=0, columnspan=7)
        tk.Label(mode_frame, text='Please select the appropriate mode:').grid(row=1, column=0)
        self.mode = tk.StringVar()
        tk.OptionMenu(mode_frame, self.mode, "load monitoring and scan", "load monitoring only", "scan only").grid(row=1, column=1, columnspan=3)
        
    def create_sensor_frame(self):
        sensor_frame = tk.Frame(self.bottom_frame, relief=tk.SUNKEN, borderwidth=1)
        sensor_frame.pack(side=tk.TOP)
        sensor_title = tk.Label(sensor_frame, text='Monitoring setting')
        sensor_title.configure(font='Arial 15')
        sensor_title.grid(row=0, column=0, columnspan=4)
        tk.Label(sensor_frame, text='Critical load:').grid(row=1, column=1)
        self.critical_load = tk.DoubleVar()
        tk.Entry(sensor_frame,width=7, textvariable=self.critical_load).grid(row=1, column=2)
        tk.Label(sensor_frame, text='N').grid(row=1, column=3)
        
        tk.Label(sensor_frame, text='Monitoring interval:').grid(row=2, column=1)
        self.sensor_interval = tk.IntVar()
        tk.Entry(sensor_frame,width=7, textvariable=self.sensor_interval).grid(row=2, column=2)
        tk.Label(sensor_frame, text='seconds').grid(row=2, column=3)
    
    def create_scan_frame(self):
        scan_frame = tk.Frame(self.bottom_frame, relief=tk.SUNKEN, borderwidth=1)
        scan_frame.pack()
        scan_title = tk.Label(scan_frame, text='Scan setting')
        scan_title.configure(font='Arial 15')
        scan_title.grid(row=0, columnspan=7)        
        tk.Label(scan_frame, text='camera installed: ').grid(row=1, column=0)
        self.camera = tk.StringVar()
        tk.OptionMenu(scan_frame, self.camera, "True", "False").grid(row=1, column=1)
        upload_button = tk.Button(scan_frame, text='upload scan image', command=self.uploadAction)
        upload_button.grid(row=1, column=3, columnspan=3)
        
        tk.Label(scan_frame, text='crop image: ').grid(row=2, column=0)
        self.crop = tk.StringVar()
        tk.OptionMenu(scan_frame, self.crop, "Yes", "No").grid(row=2, column=1)
        self.crop_x = tk.IntVar()
        self.crop_y = tk.IntVar()
        self.crop_width = tk.IntVar()
        self.crop_height = tk.IntVar()
        tk.Label(scan_frame, text='Enter position:   X:').grid(row=3, column=0)        
        tk.Entry(scan_frame, textvariable=self.crop_x, width=4).grid(row=3, column=1)
        tk.Label(scan_frame, text='Y:').grid(row=3, column=2)
        tk.Entry(scan_frame, textvariable=self.crop_y, width=4).grid(row=3, column=3)
        tk.Label(scan_frame, text='width:').grid(row=3, column=4)
        tk.Entry(scan_frame, textvariable=self.crop_width, width=4).grid(row=3, column=5)
        tk.Label(scan_frame, text='height:').grid(row=3, column=6)
        tk.Entry(scan_frame, textvariable=self.crop_height, width=4).grid(row=3, column=7)
                
        tk.Label(scan_frame, text='scan interval:').grid(row=4, column=0)
        self.interval_day = tk.IntVar()
        self.interval_hour = tk.IntVar()
        self.interval_min = tk.IntVar()
        tk.Entry(scan_frame, textvariable=self.interval_day, width=5).grid(row=4, column=1)
        tk.Label(scan_frame, text='days').grid(row=4, column=2)
        tk.Entry(scan_frame, textvariable=self.interval_hour, width=5).grid(row=4, column=3)
        tk.Label(scan_frame, text='hours').grid(row=4, column=4)
        tk.Entry(scan_frame, textvariable=self.interval_min, width=5).grid(row=4, column=5)
        tk.Label(scan_frame, text='minutes').grid(row=4, column=6)
        
    def create_email_frame(self):
        email_frame = tk.Frame(self.bottom_frame, relief=tk.SUNKEN, borderwidth=1)
        email_frame.pack(side=tk.LEFT)
        email_title = tk.Label(email_frame, text='Alert email setting')
        email_title.configure(font='Arial 15')
        email_title.grid(row=0, columnspan=4)
        
        tk.Label(email_frame, text="Send from (prefer gmail address): ").grid(row=1, column=0)
        self.sender = tk.StringVar()
        tk.Entry(email_frame, width=28, textvariable=self.sender).grid(row=2, column=0, columnspan=5)
        self.sender.set("12345@gmail.com")
        tk.Label(email_frame, text="Send from (enter login password): ").grid(row=3, column=0)
        self.password = tk.StringVar()
        tk.Entry(email_frame, width=28, show="*", textvariable=self.password).grid(row=4, column=0, columnspan=5)
        self.password.set("thisisapassword")
        tk.Label(email_frame, text="Recipients (use ','): ").grid(row=5, column=0)
        self.recipients = tk.StringVar()
        tk.Entry(email_frame, width=30, textvariable=self.recipients).grid(row=6, column=0, columnspan=6)
        self.recipients.set("12345@u.nus.edu,7890@hotmail.com")
        
    def create_submit_button(self):
        self.button = tk.Button(self.bottom_frame, text="Confirm", command=self.show)
        self.button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    
    def init_gui(self):
        self.create_top_frame()
        self.create_bottom_frame()
        self.create_mode_frame()
        self.create_sensor_frame()
        self.create_scan_frame()
        self.create_email_frame()
        self.create_submit_button()
        
    def show(self):
        print( "You entered:")
        print( "Mode: ", self.get_mode())
        print( "Critical loading: ", self.get_critical_load())
        print( "interval: ", self.get_sensor_interval())
        print( "camera: ", self.get_camera())
        if self.upload == True:
            print("filename: ", self.filename)
        print('crop image: ', self.get_crop())
        if self.get_crop() == 'Yes':
            print('crop postion', self.get_crop_position())
        print( 'interval: ', self.get_scan_interval())
        print( "alert email sent from: ", self.get_sender_email())
        print("email password: ", self.get_password())
        print("alert email recipients: ", self.get_recipients())
        print( '*'*20)
        
if __name__ == '__main__':
    root = tk.Tk()
    s = Setting(root)
    root.mainloop()