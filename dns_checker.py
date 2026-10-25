import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import dns.resolver
from plyer import notification  # Switched to plyer

# Configuration: List of public DNS servers to check
DNS_SERVERS = [
    "8.8.8.8",       # Google
    "1.1.1.1",       # Cloudflare
    "9.9.9.9",        # Quad9
    "208.67.222.222", # OpenDNS
    "8.8.4.4"         # Google Secondary
]

class DNSPropagatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Propagation Monitor")
        self.root.geometry("400x450")

        # UI Elements
        tk.Label(root, text="Domain Name (e.g., example.com):", font=("Arial", 10, "bold")).pack(pady=5)
        self.domain_entry = tk.Entry(root, width=30)
        self.domain_entry.insert(0, "example.com")
        self.domain_entry.pack(pady=5)

        tk.Label(root, text="Expected IP Address:", font=("Arial", 10, "bold")).pack(pady=5)
        self.ip_entry = tk.Entry(root, width=30)
        self.ip_entry.insert(0, "1.2.3.4")
        self.ip_entry.pack(pady=5)

        tk.Label(root, text="Check Interval (seconds):", font=("Arial", 10, "bold")).pack(pady=5)
        self.interval_entry = tk.Entry(root, width=30)
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(pady=5)

        self.status_label = tk.Label(root, text="Status: Idle", fg="blue")
        self.status_label.pack(pady=20)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100, length=300)
        self.progress_bar.pack(pady=5)

        self.start_btn = tk.Button(root, text="Start Monitoring", command=self.start_thread, bg="green", fg="white")
        self.start_btn.pack(pady=20)

        self.stop_flag = False

    def start_thread(self):
        self.stop_flag = False
        self.start_btn.config(state="disabled", text="Monitoring...")
        threading.Thread(target=self.monitor_dns, daemon=True).start()

    def monitor_dns(self):
        domain = self.domain_entry.get()
        expected_ip = self.ip_entry.get().strip()
        try:
            interval = int(self.interval_entry.get())
        except ValueError:
            interval = 60

        while not self.stop_flag:
            self.status_label.config(text="Status: Checking...", fg="orange")
            results = []
            
            for server in DNS_SERVERS:
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = [server]
                    answers = resolver.resolve(domain, 'A')
                    ip = str(answers[0].to_text()).rstrip('.')
                    results.append(ip == expected_ip)
                except Exception:
                    results.append(False)

            success_count = sum(1 for r in results if r is True)
            progress = (success_count / len(DNS_SERVERS)) * 100
            self.progress_var.set(progress)

            if success_count == len(DNS_SERVERS):
                self.status_label.config(text="Status: COMPLETE!", fg="green")
                # Using plyer for notification
                notification.notify(
                    title="DNS Propagation Complete!",
                    message=f"The domain {domain} is now resolving to {expected_ip} on all checked servers.",
                    timeout=10
                )
                break
            else:
                self.status_label.config(text=f"Status: {success_count}/{len(DNS_SERVERS)} Servers Updated")
            
            time.sleep(interval)

        self.start_btn.config(state="normal", text="Start Monitoring")

if __name__ == "__main__":
    root = tk.Tk()
    app = DNSPropagatorApp(root)
    root.mainloop()

