import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from person2 import find_matches
from naive import naive_search

class PlagiarismDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plagiarism Detector")
        self.root.geometry("700x700")  # Made taller for the additional section
        
        # File paths
        self.file1_path = ""
        self.file2_path = ""
        self.file1_content = ""
        self.file2_content = ""
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for file selection
        file_frame = tk.Frame(self.root, pady=10)
        file_frame.pack(fill=tk.X)
        
        # File 1 selection
        tk.Label(file_frame, text="File 1:").grid(row=0, column=0, padx=5)
        self.file1_entry = tk.Entry(file_frame, width=50)
        self.file1_entry.grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_file1).grid(row=0, column=2, padx=5)
        
        # File 2 selection
        tk.Label(file_frame, text="File 2:").grid(row=1, column=0, padx=5)
        self.file2_entry = tk.Entry(file_frame, width=50)
        self.file2_entry.grid(row=1, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_file2).grid(row=1, column=2, padx=5)
        
        # Compare button
        compare_btn = tk.Button(self.root, text="Compare Files", command=self.compare_files)
        compare_btn.pack(pady=10)
        
        # Results area
        tk.Label(self.root, text="Plagiarism Results:").pack(anchor=tk.W, padx=10)
        self.results_text = scrolledtext.ScrolledText(self.root, height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Naive Search Section
        naive_frame = tk.Frame(self.root, pady=10)
        naive_frame.pack(fill=tk.X)
        
        # Label for naive search section
        tk.Label(naive_frame, text="Naive String Search", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)
        
        # Pattern input
        tk.Label(naive_frame, text="Pattern to search:").grid(row=1, column=0, padx=5, sticky=tk.W)
        self.pattern_entry = tk.Entry(naive_frame, width=40)
        self.pattern_entry.grid(row=1, column=1, padx=5)
        
        # File selection for naive search
        self.file_var = tk.StringVar(value="file1")
        tk.Radiobutton(naive_frame, text="Search in File 1", variable=self.file_var, value="file1").grid(row=2, column=0, sticky=tk.W)
        tk.Radiobutton(naive_frame, text="Search in File 2", variable=self.file_var, value="file2").grid(row=2, column=1, sticky=tk.W)
        
        # Naive search button
        naive_btn = tk.Button(naive_frame, text="Search", command=self.perform_naive_search)
        naive_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Naive search results
        tk.Label(self.root, text="Naive Search Results:").pack(anchor=tk.W, padx=10)
        self.naive_results_text = scrolledtext.ScrolledText(self.root, height=10)
        self.naive_results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def browse_file1(self):
        self.file1_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file1_path:
            self.file1_entry.delete(0, tk.END)
            self.file1_entry.insert(0, self.file1_path)
            self.read_file1()
    
    def browse_file2(self):
        self.file2_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file2_path:
            self.file2_entry.delete(0, tk.END)
            self.file2_entry.insert(0, self.file2_path)
            self.read_file2()
    
    def read_file1(self):
        try:
            with open(self.file1_path, 'r') as file:
                self.file1_content = file.read()
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file 1: {str(e)}")
    
    def read_file2(self):
        try:
            with open(self.file2_path, 'r') as file:
                self.file2_content = file.read()
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file 2: {str(e)}")
    
    def compare_files(self):
        if not self.file1_content or not self.file2_content:
            messagebox.showwarning("Warning", "Please select two files to compare")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Find matches between the two files
        matches = find_matches(self.file1_content, self.file2_content)
        
        # Display results
        self.results_text.insert(tk.END, "Plagiarism Detection Results:\n\n")
        
        if not any(matches.values()):
            self.results_text.insert(tk.END, "No matching phrases found between the files.\n")
        else:
            total_matches = sum(len(m) for m in matches.values())
            self.results_text.insert(tk.END, f"Found {total_matches} total matches across all algorithms.\n\n")
            
            # Display matches for each algorithm
            for algo, algo_matches in matches.items():
                if algo_matches:
                    self.results_text.insert(tk.END, f"\n{algo} ({len(algo_matches)} matches):\n")
                    for i, (phrase, positions) in enumerate(algo_matches, 1):
                        self.results_text.insert(tk.END, f"{i}. \"{phrase}\" found at positions: {positions}\n")
    
    def perform_naive_search(self):
        pattern = self.pattern_entry.get().strip()
        if not pattern:
            messagebox.showwarning("Warning", "Please enter a pattern to search for")
            return
        
        # Determine which file to search in
        if self.file_var.get() == "file1":
            if not self.file1_content:
                messagebox.showwarning("Warning", "Please select File 1 first")
                return
            content = self.file1_content
            file_name = self.file1_path.split("/")[-1]
        else:
            if not self.file2_content:
                messagebox.showwarning("Warning", "Please select File 2 first")
                return
            content = self.file2_content
            file_name = self.file2_path.split("/")[-1]
        
        # Clear previous results
        self.naive_results_text.delete(1.0, tk.END)
        
        # Perform naive search
        positions = naive_search(content, pattern)
        
        # Display results
        self.naive_results_text.insert(tk.END, f"Naive Search Results for pattern \"{pattern}\" in {file_name}:\n\n")
        
        if not positions:
            self.naive_results_text.insert(tk.END, "No matches found.\n")
        else:
            self.naive_results_text.insert(tk.END, f"Found {len(positions)} matches at positions: {positions}\n")
            
            # Show context for each match (optional)
            for i, pos in enumerate(positions, 1):
                start = max(0, pos - 20)
                end = min(len(content), pos + len(pattern) + 20)
                context = content[start:end].replace('\n', ' ')
                
                # Highlight the matched pattern
                pre_context = content[start:pos].replace('\n', ' ')
                highlight = content[pos:pos+len(pattern)].replace('\n', ' ')
                post_context = content[pos+len(pattern):end].replace('\n', ' ')
                
                self.naive_results_text.insert(tk.END, f"\n{i}. ...{pre_context}")
                self.naive_results_text.insert(tk.END, f"{highlight}", "highlight")
                self.naive_results_text.insert(tk.END, f"{post_context}...\n")
            
            # Configure tag for highlighting
            self.naive_results_text.tag_configure("highlight", background="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlagiarismDetectorGUI(root)
    root.mainloop()
