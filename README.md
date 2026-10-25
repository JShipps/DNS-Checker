# DNS Propagation Monitor

A lightweight desktop application that watches public DNS servers until they all resolve a domain name to an expected IP address. It's useful for verifying DNS propagation after updating A records on your authoritative nameserver — e.g., when pointing a new hosting provider, moving a subdomain, or confirming a record change has taken effect globally.

---

## Features

- **Multi-server validation** — checks the domain against 5 public resolvers:
  - Google (`8.8.8.8`, `8.8.4.4`)
  - Cloudflare (`1.1.1.1`)
  - Quad9 (`9.9.9.9`)
  - OpenDNS (`208.67.222.222`)
- **Progress tracking** — live progress bar showing how many servers have updated.
- **Automatic notification** — pops up a desktop notification when every server matches the expected IP.
- **Background monitoring** — runs in a separate thread so you can keep using the window while it checks.
- **Configurable interval** — set the polling frequency (default: 60 seconds).

---

## Requirements

| Requirement | Version / Notes |
| --- | --- |
| Python | 3.8 or newer (standard library only) |
| `dnspython` | Third-party DNS query library |
| `plyer` | Third-party notification library (Windows desktop notifications) |
| Windows | Required for the GUI (`tkinter`) |

---

## Installation

1. Make sure you have Python installed:

   ```cmd
   python --version
   ```

2. Install the required packages:

   ```cmd
   pip install dnspython plyer
   ```

3. (Optional) If `import tkinter` fails, install the Tcl/Tk runtime for Windows — e.g., [ActiveTcl](https://www.activetcl.com/downloads.html).

---

## Usage

1. Open a command prompt in this project folder and run:

   ```cmd
   python dns_checker.py
   ```

2. In the window that appears:
   - **Domain Name** — enter the domain to check (e.g., `example.com`).
   - **Expected IP Address** — enter the IP you expect it to resolve to (e.g., `1.2.3.4`).
   - **Check Interval** — how often to poll, in seconds (default: `60`).

3. Click **Start Monitoring**. The status will update as each server responds, and a notification will appear when all servers match.

---

## Configuration

Edit the top of `dns_checker.py` to change behavior:

```python
# Public DNS servers used for validation — add or remove as needed
DNS_SERVERS = [
    "8.8.8.8",       # Google
    "1.1.1.1",       # Cloudflare
    "9.9.9.9",        # Quad9
    "208.67.222.222", # OpenDNS
    "8.8.4.4"         # Google Secondary
]
```

> **Note:** The script currently checks `A` records only (IPv4). To monitor IPv6 (`AAAA`) records or other record types, extend the resolver logic in `monitor_dns()`.

---

## Development

To run the tests or verify behavior locally:

1. Install dependencies (see [Installation](#installation)).
2. Launch the app from a command prompt in this folder:

   ```cmd
   python dns_checker.py
   ```

3. Enter a domain and expected IP, then click **Start Monitoring**.
4. Stop monitoring with `Ctrl+C` in the terminal to close the window gracefully (if it doesn't respond, use the task manager).

> The application is single-purpose — no test suite or CI pipeline has been added yet. If you plan to grow this into a library, consider adding pytest cases that call `DNSPropagatorApp.monitor_dns()` directly without launching the GUI.

---

## Troubleshooting

- **"An interactive console application was launched without a supporting display environment"** — tkinter needs a graphical environment. Install the Tcl/Tk runtime for Windows as described above.
- **`ModuleNotFoundError: No module named 'dnspython'`** — run `pip install dnspython`. If you're using a virtual environment, make sure it's activated first.
- **No notification appears on completion** — ensure `plyer` is installed and that desktop notifications are enabled in your Windows settings.
- **"Query to resolver ... failed"** — the DNS server may be temporarily unavailable or blocking requests from your network; retry later.

---

## Project Structure

```
dns_checker/
├── dns_checker.py    # Main application script
└── README.md         # This file
```

---

## License

MIT License — feel free to use, modify, and distribute this project.