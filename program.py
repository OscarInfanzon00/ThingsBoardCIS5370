
import tkinter as tk
from LoginWindowClass import LoginWindow
from sendDataToSensor import start_mqtt_thread

# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    start_mqtt_thread()
    root.mainloop()