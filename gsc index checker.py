import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import threading
from urllib.parse import urlparse, quote
import time
from fake_useragent import UserAgent
import webbrowser

class GSCInspector:
    def __init__(self, root):
        self.root = root
        self.root.title("GSC-like URL Inspector")
        self.root.geometry("1100x800")
        self.root.minsize(1000, 700)
        
        # User agent generator
        self.ua = UserAgent()
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        self.style.configure("TButton", font=('Arial', 10))
        self.style.configure("Success.TLabel", foreground="green")
        self.style.configure("Warning.TLabel", foreground="orange")
        self.style.configure("Error.TLabel", foreground="red")
        self.style.configure("Info.TLabel", foreground="blue")
        
        self.create_widgets()
        self.running = False
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame (similar to GSC)
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Logo and title
        logo_label = ttk.Label(header_frame, text="🔍", font=('Arial', 20))
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title_label = ttk.Label(title_frame, text="URL Inspection Tool", font=('Arial', 16, 'bold'))
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(title_frame, text="Check Google indexing status and troubleshoot issues", style="Info.TLabel")
        subtitle_label.pack(anchor=tk.W)
        
        # URL input frame (like GSC search bar)
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=80, font=('Arial', 11))
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Action buttons
        inspect_button = ttk.Button(url_frame, text="Inspect URL", command=self.start_inspection)
        inspect_button.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_button = ttk.Button(url_frame, text="Clear", command=self.clear_all)
        clear_button.pack(side=tk.LEFT)
        
        # Results notebook (tabbed interface)
        self.results_notebook = ttk.Notebook(main_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Coverage tab (like GSC)
        self.coverage_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.coverage_frame, text="Coverage")
        self.create_coverage_tab()
        
        # Enhancements tab
        self.enhancements_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.enhancements_frame, text="Enhancements")
        self.create_enhancements_tab()
        
        # Mobile Usability tab
        self.mobile_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.mobile_frame, text="Mobile Usability")
        self.create_mobile_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to inspect URLs")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Tooltip window
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip_label = tk.Label(
            self.tooltip, 
            text="", 
            background="#ffffe0", 
            relief="solid", 
            borderwidth=1,
            wraplength=400,
            justify="left",
            padx=10,
            pady=5
        )
        self.tooltip_label.pack()
    
    def create_coverage_tab(self):
        """Create the coverage tab similar to GSC"""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.coverage_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Indexing status section
        status_frame = ttk.LabelFrame(scrollable_frame, text="Indexing status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.indexing_status_var = tk.StringVar(value="Not checked yet")
        status_label = ttk.Label(
            status_frame, 
            textvariable=self.indexing_status_var,
            font=('Arial', 12),
            wraplength=800
        )
        status_label.pack(fill=tk.X)
        
        # Last crawl section
        crawl_frame = ttk.LabelFrame(scrollable_frame, text="Last crawl", padding=10)
        crawl_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.crawl_date_var = tk.StringVar(value="Not available")
        self.crawl_rendered_var = tk.StringVar(value="Not available")
        
        ttk.Label(crawl_frame, text="Date:").pack(anchor=tk.W)
        ttk.Label(crawl_frame, textvariable=self.crawl_date_var, font=('Arial', 10)).pack(anchor=tk.W, padx=20)
        
        ttk.Label(crawl_frame, text="Rendered version:").pack(anchor=tk.W, pady=(5,0))
        ttk.Label(crawl_frame, textvariable=self.crawl_rendered_var, font=('Arial', 10)).pack(anchor=tk.W, padx=20)
        
        # Page availability section
        availability_frame = ttk.LabelFrame(scrollable_frame, text="Page availability", padding=10)
        availability_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.robots_var = tk.StringVar(value="Not checked")
        self.canonical_var = tk.StringVar(value="Not checked")
        
        ttk.Label(availability_frame, text="Robots.txt:").pack(anchor=tk.W)
        ttk.Label(availability_frame, textvariable=self.robots_var, font=('Arial', 10)).pack(anchor=tk.W, padx=20)
        
        ttk.Label(availability_frame, text="Canonical:").pack(anchor=tk.W, pady=(5,0))
        ttk.Label(availability_frame, textvariable=self.canonical_var, font=('Arial', 10)).pack(anchor=tk.W, padx=20)
        
        # Indexing allowed section
        indexing_frame = ttk.LabelFrame(scrollable_frame, text="Indexing allowed", padding=10)
        indexing_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.indexing_allowed_var = tk.StringVar(value="Not checked")
        self.noindex_var = tk.StringVar(value="Not checked")
        
        ttk.Label(indexing_frame, text="Indexing:").pack(anchor=tk.W)
        ttk.Label(indexing_frame, textvariable=self.indexing_allowed_var, font=('Arial', 10)).pack(anchor=tk.W, padx=20)
        
        ttk.Label(indexing_frame, text="Noindex directive:").pack(anchor=tk.W, pady=(5,0))
        ttk.Label(indexing_frame, textvariable=self.noindex_var, font=('Arial', 10)).pack(anchor=tk.W, padx=20)
        
        # Troubleshooting section
        troubleshoot_frame = ttk.LabelFrame(scrollable_frame, text="Troubleshooting", padding=10)
        troubleshoot_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.troubleshoot_text = tk.Text(
            troubleshoot_frame, 
            height=8, 
            wrap=tk.WORD, 
            font=('Arial', 10),
            padx=5,
            pady=5
        )
        self.troubleshoot_text.pack(fill=tk.BOTH)
        self.troubleshoot_text.insert("1.0", "Inspection results will appear here")
        self.troubleshoot_text.config(state=tk.DISABLED)
        
        # Open in GSC button
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        gsc_button = ttk.Button(
            button_frame, 
            text="Open in Google Search Console", 
            command=self.open_in_gsc
        )
        gsc_button.pack(pady=5)
    
    def create_enhancements_tab(self):
        """Create empty enhancements tab"""
        label = ttk.Label(
            self.enhancements_frame, 
            text="This tool currently focuses on indexing status.\n\n"
                 "Future versions may include enhancements analysis like:\n"
                 "- Schema markup detection\n- Breadcrumbs check\n- AMP validation",
            justify=tk.CENTER
        )
        label.pack(pady=50)
    
    def create_mobile_tab(self):
        """Create empty mobile usability tab"""
        label = ttk.Label(
            self.mobile_frame, 
            text="This tool currently focuses on indexing status.\n\n"
                 "Future versions may include mobile usability checks like:\n"
                 "- Viewport configuration\n- Tap target sizing\n- Font sizing",
            justify=tk.CENTER
        )
        label.pack(pady=50)
    
    def start_inspection(self):
        """Start URL inspection"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL to inspect")
            return
        
        if self.running:
            return
            
        self.running = True
        self.status_var.set(f"Checking: {url}")
        
        # Reset UI
        self.indexing_status_var.set("Checking...")
        self.crawl_date_var.set("Checking...")
        self.crawl_rendered_var.set("Checking...")
        self.robots_var.set("Checking...")
        self.canonical_var.set("Checking...")
        self.indexing_allowed_var.set("Checking...")
        self.noindex_var.set("Checking...")
        
        self.troubleshoot_text.config(state=tk.NORMAL)
        self.troubleshoot_text.delete("1.0", tk.END)
        self.troubleshoot_text.insert("1.0", f"Running inspection for: {url}\n\nPlease wait...")
        self.troubleshoot_text.config(state=tk.DISABLED)
        
        # Start inspection in separate thread
        threading.Thread(target=self.inspect_url, args=(url,), daemon=True).start()
    
    def inspect_url(self, url):
        """Main inspection logic"""
        try:
            # Normalize URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("Invalid URL format - missing domain")
            
            # Simulate checking different aspects
            time.sleep(1)  # Simulate delay
            
            # Check indexing status (simulated)
            is_indexed = self.check_google_index(url)
            
            # Update UI with results
            self.root.after(0, self.update_results, url, is_indexed)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.running = False
            self.root.after(0, lambda: self.status_var.set("Inspection complete"))
    
    def check_google_index(self, url):
        """Check if URL is indexed (simulated)"""
        # In a real implementation, this would actually check Google
        # Here we simulate different possible outcomes
        
        # Randomly determine status for demo purposes
        import random
        status = random.choice([
            "indexed", 
            "not_indexed_robots", 
            "not_indexed_noindex", 
            "not_indexed_404",
            "not_indexed_other"
        ])
        
        if status == "indexed":
            return {
                "indexing_status": "URL is on Google",
                "status_style": "Success.TLabel",
                "crawl_date": self.get_random_date(),
                "rendered": "Successfully rendered",
                "robots": "Allowed by robots.txt",
                "canonical": "Self-referential canonical",
                "indexing_allowed": "Yes",
                "noindex": "No",
                "troubleshooting": "No issues detected. This URL is properly indexed by Google."
            }
        elif status == "not_indexed_robots":
            return {
                "indexing_status": "URL is not on Google: Blocked by robots.txt",
                "status_style": "Error.TLabel",
                "crawl_date": "Not crawled",
                "rendered": "Not rendered",
                "robots": "Blocked by robots.txt",
                "canonical": "Not available",
                "indexing_allowed": "No",
                "noindex": "Not applicable",
                "troubleshooting": "Troubleshooting:\n\n"
                                  "• This URL is blocked by robots.txt\n"
                                  "• Googlebot cannot crawl this page\n"
                                  "• Solution: Update your robots.txt file to allow access"
            }
        elif status == "not_indexed_noindex":
            return {
                "indexing_status": "URL is not on Google: Noindex tag detected",
                "status_style": "Warning.TLabel",
                "crawl_date": self.get_random_date(),
                "rendered": "Rendered but not indexed",
                "robots": "Allowed by robots.txt",
                "canonical": "Self-referential canonical",
                "indexing_allowed": "No",
                "noindex": "Yes",
                "troubleshooting": "Troubleshooting:\n\n"
                                  "• This page has a 'noindex' directive\n"
                                  "• Google found the page but was told not to index it\n"
                                  "• Solution: Remove noindex meta tag if you want it indexed"
            }
        elif status == "not_indexed_404":
            return {
                "indexing_status": "URL is not on Google: Page not found (404)",
                "status_style": "Error.TLabel",
                "crawl_date": self.get_random_date(),
                "rendered": "Error during rendering",
                "robots": "Allowed by robots.txt",
                "canonical": "Not available",
                "indexing_allowed": "No",
                "noindex": "Not applicable",
                "troubleshooting": "Troubleshooting:\n\n"
                                  "• This URL returns a 404 (Not Found) error\n"
                                  "• The page may have been moved or deleted\n"
                                  "• Solution: Fix the URL or implement a proper redirect"
            }
        else:
            return {
                "indexing_status": "URL is not on Google: Discovered - currently not indexed",
                "status_style": "Warning.TLabel",
                "crawl_date": "Not crawled yet",
                "rendered": "Not rendered",
                "robots": "Allowed by robots.txt",
                "canonical": "Not available",
                "indexing_allowed": "Yes",
                "noindex": "No",
                "troubleshooting": "Troubleshooting:\n\n"
                                  "• Google has discovered this URL but hasn't crawled it yet\n"
                                  "• This is common for new or low-priority pages\n"
                                  "• Solution: Request indexing in GSC or improve internal linking"
            }
    
    def get_random_date(self):
        """Generate a random recent date for simulation"""
        import random
        from datetime import datetime, timedelta
        days_ago = random.randint(1, 30)
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d %H:%M:%S")
    
    def update_results(self, url, results):
        """Update UI with inspection results"""
        self.indexing_status_var.set(results["indexing_status"])
        self.crawl_date_var.set(results["crawl_date"])
        self.crawl_rendered_var.set(results["rendered"])
        self.robots_var.set(results["robots"])
        self.canonical_var.set(results["canonical"])
        self.indexing_allowed_var.set(results["indexing_allowed"])
        self.noindex_var.set(results["noindex"])
        
        # Apply appropriate styling
        for widget in [self.indexing_status_var]:
            self.style.configure("Status.TLabel", foreground="black")
            if "Success" in results["status_style"]:
                self.style.configure("Status.TLabel", foreground="green")
            elif "Warning" in results["status_style"]:
                self.style.configure("Status.TLabel", foreground="orange")
            elif "Error" in results["status_style"]:
                self.style.configure("Status.TLabel", foreground="red")
        
        # Update troubleshooting info
        self.troubleshoot_text.config(state=tk.NORMAL)
        self.troubleshoot_text.delete("1.0", tk.END)
        
        # Add header
        self.troubleshoot_text.insert("1.0", f"Inspection results for: {url}\n\n", "header")
        self.troubleshoot_text.tag_configure("header", font=('Arial', 10, 'bold'))
        
        # Add status
        self.troubleshoot_text.insert(tk.END, "Indexing status: ", "label")
        self.troubleshoot_text.insert(tk.END, f"{results['indexing_status']}\n\n", results["status_style"].replace(".TLabel", ""))
        self.troubleshoot_text.tag_configure("label", font=('Arial', 10, 'bold'))
        
        # Add troubleshooting info
        self.troubleshoot_text.insert(tk.END, results["troubleshooting"])
        
        # Add footer
        self.troubleshoot_text.insert(tk.END, "\n\nNote: This is a simulated inspection. For accurate results, use Google Search Console.", "footer")
        self.troubleshoot_text.tag_configure("footer", font=('Arial', 9), foreground="gray")
        
        self.troubleshoot_text.config(state=tk.DISABLED)
        
        # Switch to coverage tab
        self.results_notebook.select(self.coverage_frame)
    
    def show_error(self, error_msg):
        """Show error message in UI"""
        self.indexing_status_var.set("Inspection failed")
        self.crawl_date_var.set("Error")
        self.crawl_rendered_var.set("Error")
        self.robots_var.set("Error")
        self.canonical_var.set("Error")
        self.indexing_allowed_var.set("Error")
        self.noindex_var.set("Error")
        
        self.troubleshoot_text.config(state=tk.NORMAL)
        self.troubleshoot_text.delete("1.0", tk.END)
        self.troubleshoot_text.insert("1.0", f"Inspection failed:\n\n{error_msg}\n\nPlease check the URL and try again.")
        self.troubleshoot_text.config(state=tk.DISABLED)
        
        self.style.configure("Status.TLabel", foreground="red")
    
    def open_in_gsc(self):
        """Open current URL in Google Search Console"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "No URL to open in GSC")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        gsc_url = f"https://search.google.com/search-console/inspect?resource_id={quote(url)}"
        webbrowser.open(gsc_url)
    
    def clear_all(self):
        """Clear all fields"""
        self.url_var.set("")
        self.indexing_status_var.set("Not checked yet")
        self.crawl_date_var.set("Not available")
        self.crawl_rendered_var.set("Not available")
        self.robots_var.set("Not checked")
        self.canonical_var.set("Not checked")
        self.indexing_allowed_var.set("Not checked")
        self.noindex_var.set("Not checked")
        
        self.troubleshoot_text.config(state=tk.NORMAL)
        self.troubleshoot_text.delete("1.0", tk.END)
        self.troubleshoot_text.insert("1.0", "Inspection results will appear here")
        self.troubleshoot_text.config(state=tk.DISABLED)
        
        self.status_var.set("Ready to inspect URLs")

if __name__ == "__main__":
    root = tk.Tk()
    app = GSCInspector(root)
    root.mainloop()