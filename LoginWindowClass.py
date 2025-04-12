import tkinter as tk
from tkinter import messagebox, ttk
from MainWindowClass import MainWindow
from RestClientClass import RestClient

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Sensor Access Control")
        self.root.geometry("400x420")
        self.rest_client = RestClient()
        
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", padding=5)
        style.configure("TEntry", padding=5)
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="ThingsBoard IoT Dashboard", font=("Helvetica", 14)).pack(pady=4)
        ttk.Label(main_frame, text="CIS5370 Group 1 Solution of proof-of-concept RBAC system.", font=("Helvetica", 8)).pack(pady=10)
        
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(login_frame, text="Email").grid(row=0, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(login_frame, width=30)
        self.email_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(login_frame, text="Password").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Login", command=self.login).pack(fill=tk.X, pady=5)
        
        # Example login info
        example_frame = ttk.LabelFrame(main_frame, text="Example Logins (Click on them to autocomplete credentials)")
        example_frame.pack(fill=tk.X, pady=10)
        
        self.create_example_login(example_frame, "Tenant", "super@gmail.com", "12345678")
        self.create_example_login(example_frame, "Customer", "Customer1@gmail.com", "12345678")
        self.create_example_login(example_frame, "Admin", "Admin1@gmail.com", "12345678")

    def create_example_login(self, frame, role, email, password):
        label = ttk.Label(frame, text=f"{role} - {email} / {password}")
        label.pack(anchor="w")
        label.bind("<Button-1>", lambda e, email=email, password=password: self.fill_example_login(email, password))

    def fill_example_login(self, email, password):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)
        self.password_entry.insert(0, password)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            if self.rest_client.login(email, password):
                user_info = self.rest_client.get_user()
                # Get user permissions and role
                permissions = self.rest_client.get_allowed_permissions()
                self.root.destroy()
                MainWindow(self.rest_client, user_info, permissions)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials or error logging in.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
