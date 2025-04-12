from tkinter import messagebox, ttk
import tkinter as tk
import webbrowser
from datetime import datetime
import logging
from tb_rest_client.rest_client_pe import RestClientPE
from tb_rest_client.rest import ApiException
from commonData import DEVICE_ID, THINGSBOARD_HOST

class MainWindow:
    def __init__(self, rest_client, user_info, permissions):
        self.rest_client = rest_client
        self.user_info = user_info
        self.permissions = permissions
        
        self.root = tk.Tk()
        self.root.title("ThingsBoard IoT Dashboard")
        self.root.geometry("850x650")

        self.timestamp = ""
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Determine effective role and update UI
        self.effective_role = self.initialize_role_and_ui()

        # Start periodic data update
        self.update_device_data() 
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def open_selected_dashboard(self, event):
        selected_item = self.dashboard_tree.selection()
        if selected_item:
            item = self.dashboard_tree.item(selected_item)
            dashboard_name = item['values'][0]

            # Use ThingsBoard REST client to fetch dashboards
            with RestClientPE(base_url=f"{THINGSBOARD_HOST}") as rest_client:
                try:
                    # Authenticate with credentials
                    rest_client.login(username="super@gmail.com", password="12345678")

                    # Fetch dashboards
                    dashboard_data = rest_client.get_user_dashboards(page_size=10, page=0)

                    # Assuming `dashboard_data` is an instance of `PageDataDashboardInfo`
                    # Access the `data` attribute directly, which should contain a list of dashboards
                    if hasattr(dashboard_data, 'data'):
                        for dashboard in dashboard_data.data:  # Access the `data` attribute
                            if dashboard.title == dashboard_name:  # Access `title` directly
                                dashboard_id = dashboard.id.id  # Access `id` and then its `id` attribute
                                if dashboard_id:
                                    dashboard_url = f"{THINGSBOARD_HOST}/dashboards/all/{dashboard_id}"
                                    webbrowser.open_new_tab(dashboard_url)
                                    return

                    messagebox.showwarning("Warning", "Dashboard ID not found.")
                except ApiException as e:
                    logging.exception(f"Error occurred: {e}")
                    messagebox.showerror("Error", "An error occurred while fetching the dashboard.")


    def initialize_role_and_ui(self):
        try:
            devices_data = self.rest_client.get_devices()
            dashboards_data = self.rest_client.get_user_dashboards()
            has_devices = bool(devices_data.get('data'))
            has_dashboards = bool(dashboards_data.get('data'))

            # Clear any children in main_frame
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # User info section
            user_frame = ttk.LabelFrame(self.main_frame, text="User Information", padding="10")
            user_frame.pack(fill=tk.X, pady=5)

            # Determine role and tabs
            notebook = ttk.Notebook(self.main_frame)
            notebook.pack(fill=tk.BOTH, expand=True, pady=10)

            # Always show Sensor Data
            self.sensor_frame = ttk.Frame(notebook, padding="10")
            notebook.add(self.sensor_frame, text="Sensor Data")
            self.setup_sensor_tab()

            if not has_devices and not has_dashboards:
                self.effective_role = "Customer"

            elif not has_devices and has_dashboards:
                self.effective_role = "Sysadmin"
                self.dashboard_frame = ttk.Frame(notebook, padding="10")
                notebook.add(self.dashboard_frame, text="Dashboards")
                self.setup_dashboard_tab()

            else:
                self.effective_role = "Tenant"
                self.dashboard_frame = ttk.Frame(notebook, padding="10")
                notebook.add(self.dashboard_frame, text="Dashboards")
                self.setup_dashboard_tab()

                self.devices_frame = ttk.Frame(notebook, padding="10")
                notebook.add(self.devices_frame, text="Devices")
                self.setup_devices_tab()

            ttk.Label(user_frame, text=f"Email: {self.user_info.get('email', 'Unknown')}", font=("Helvetica", 10)).pack(anchor="w")
            ttk.Label(user_frame, text=f"Role: {self.effective_role}", font=("Helvetica", 10)).pack(anchor="w")
            ttk.Label(user_frame, text=self.role_description(self.effective_role), wraplength=700).pack(anchor="w")

            # Bottom buttons
            button_frame = ttk.Frame(self.main_frame)
            button_frame.pack(fill=tk.X, pady=5)
            ttk.Button(button_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT)

            return self.effective_role

        except Exception as e:
            messagebox.showerror("Error", f"Failed to determine user role: {str(e)}")
            return "UNKNOWN"

    def setup_sensor_tab(self):
        control_frame = ttk.Frame(self.sensor_frame)
        control_frame.pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Device ID:").pack(side=tk.LEFT, padx=5)
        self.device_id_entry = ttk.Entry(control_frame, width=40)
        self.device_id_entry.pack(side=tk.LEFT, padx=5)
        self.device_id_entry.insert(0, DEVICE_ID)

        ttk.Button(control_frame, text="Fetch Sensor Data", command=self.get_device_data).pack(side=tk.LEFT, padx=5)

        display_frame = ttk.LabelFrame(self.sensor_frame, text="Sensor Readings", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("parameter", "value", "timestamp")
        self.data_tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        self.data_tree.heading("parameter", text="Parameter")
        self.data_tree.heading("value", text="Value")
        self.data_tree.heading("timestamp", text="Timestamp")
        self.data_tree.column("parameter", width=150)
        self.data_tree.column("value", width=150)
        self.data_tree.column("timestamp", width=200)

        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        self.data_tree.configure(yscroll=scrollbar.set)

        self.data_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_dashboard_tab(self):
        ttk.Button(self.dashboard_frame, text="Fetch User Dashboards", command=self.get_user_dashboards).pack(anchor="w", pady=5)

        columns = ("name", "created")
        self.dashboard_tree = ttk.Treeview(self.dashboard_frame, columns=columns, show="headings")
        self.dashboard_tree.heading("name", text="Dashboard Name")
        self.dashboard_tree.heading("created", text="Created Date")
        self.dashboard_tree.column("name", width=300)
        self.dashboard_tree.column("created", width=200)

        scrollbar = ttk.Scrollbar(self.dashboard_frame, orient=tk.VERTICAL, command=self.dashboard_tree.yview)
        self.dashboard_tree.configure(yscroll=scrollbar.set)
        self.dashboard_tree.pack(fill=tk.BOTH, expand=True, pady=5, side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click to open dashboard
        self.dashboard_tree.bind("<Double-1>", self.open_selected_dashboard)


    def setup_devices_tab(self):
        ttk.Button(self.devices_frame, text="Fetch Devices", command=self.get_devices).pack(anchor="w", pady=5)
        columns = ("id", "name", "type", "active")
        self.devices_tree = ttk.Treeview(self.devices_frame, columns=columns, show="headings")
        self.devices_tree.heading("id", text="Device ID")
        self.devices_tree.heading("name", text="Device Name")
        self.devices_tree.heading("type", text="Device Type")
        self.devices_tree.heading("active", text="Active")
        self.devices_tree.column("id", width=250)
        self.devices_tree.column("name", width=200)
        self.devices_tree.column("type", width=150)
        self.devices_tree.column("active", width=100)

        scrollbar = ttk.Scrollbar(self.devices_frame, orient=tk.VERTICAL, command=self.devices_tree.yview)
        self.devices_tree.configure(yscroll=scrollbar.set)
        self.devices_tree.pack(fill=tk.BOTH, expand=True, pady=5, side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_device_data(self):
        self.get_device_data()
        self.root.after(2000, self.update_device_data)

    def get_device_data(self):
        device_id = self.device_id_entry.get()
        if not device_id:
            messagebox.showwarning("Warning", "Please enter a device ID")
            return

        try:
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)

            keys = ["temperature", "PM2.5", "PM10", "CO2"]
            data = self.rest_client.get_device_telemetry(device_id, keys)

            for key in data:
                if data[key] and len(data[key]) > 0:
                    value = data[key][0]['value']
                    self.timestamp = data[key][0].get('ts', 'N/A')

                    if isinstance(self.timestamp, (int, float)):
                        import datetime
                        self.timestamp = datetime.datetime.fromtimestamp(self.timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')

                    self.data_tree.insert("", tk.END, values=(key, value, self.timestamp))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch device data: {str(e)}")

    def get_user_dashboards(self):
        try:
            for item in self.dashboard_tree.get_children():
                self.dashboard_tree.delete(item)

            dashboard_data = self.rest_client.get_user_dashboards()

            if 'data' in dashboard_data:
                for dashboard in dashboard_data['data']:
                    name = dashboard.get('title', 'Unnamed')
                    created = dashboard.get('createdTime', 'N/A')

                    if isinstance(created, (int, float)):
                        import datetime
                        created = datetime.datetime.fromtimestamp(created/1000).strftime('%Y-%m-%d %H:%M:%S')

                    self.dashboard_tree.insert("", tk.END, values=(name, created))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch dashboards: {str(e)}")

    def get_devices(self):
        try:
            for item in self.devices_tree.get_children():
                self.devices_tree.delete(item)

            devices_data = self.rest_client.get_devices()

            if 'data' in devices_data:
                import time
                now = int(time.time() * 1000)  
                for device in devices_data['data']:
                    device_id = device.get('id', {}).get('id', 'Unknown ID')
                    name = device.get('name', 'Unnamed')
                    device_type = device.get('type', 'Unknown')

                    last_activity = self.timestamp

                    dt_obj = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
                    millis = int(dt_obj.timestamp() * 1000)
                    active = "Yes" if (now - millis) < 1 * 60 * 1000 else "No"

                    self.devices_tree.insert("", tk.END, values=(device_id, name, device_type, active))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch devices: {str(e)}")


    def role_description(self, effective_role):
        descriptions = {
            "Customer": "Customers can view only the data for assigned devices.",  
            "Sysadmin": "System Admins manage devices and dashboards.",
            "Tenant": "Tenant Admins can manage everything."
        }
        return descriptions.get(self.effective_role, f"{self.effective_role} has limited or unknown permissions.")

    def logout(self):
        self.root.destroy()
        import tkinter as tk
        from LoginWindowClass import LoginWindow  
        root = tk.Tk()
        LoginWindow(root)

    def on_closing(self):
        self.root.destroy()
