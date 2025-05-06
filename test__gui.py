import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from person2 import find_matches
from naive import naive_search
from mergeSort import merge_sort
import re
import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#changed mergesort capitalization
class DocumentInfo:
    """A class for storing and extracting document information and metadata."""
    def __init__(self, path):
        self.path = path
        self.title = ""
        self.author = ""
        self.date = ""
        self.content = ""
        self.references = []
        self.keywords = []
        self.abstract = ""
        self.sections = {}
        self.extract_metadata()
    
    def extract_metadata(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                self.content = file.read()
                self._extract_basic_metadata()
                self._extract_abstract()
                self._extract_references()
                self._extract_keywords()
                self._extract_sections()
        except Exception as e:
            print(f"Error reading file {self.path}: {str(e)}")
    
    def _extract_basic_metadata(self):
        # Extract title
        title_patterns = [
            r'Title:\s*(.*?)(?:\n|$)',
            r'^\s*#\s+(.*?)(?:\n|$)',
            r'^\s*TITLE:\s*(.*?)(?:\n|$)',
            r'^\s*<title>(.*?)</title>'
        ]
        
        for pattern in title_patterns:
            title_match = re.search(pattern, self.content, re.IGNORECASE | re.MULTILINE)
            if title_match:
                self.title = title_match.group(1).strip()
                break
        
        if not self.title:
            self.title = os.path.basename(self.path)
        
        # Extract author
        author_patterns = [
            r'Author:\s*(.*?)(?:\n|$)',
            r'By:\s*(.*?)(?:\n|$)',
            r'^\s*AUTHOR:\s*(.*?)(?:\n|$)',
            r'Written by\s*[:;]\s*(.*?)(?:\n|$)'
        ]
        
        for pattern in author_patterns:
            author_match = re.search(pattern, self.content, re.IGNORECASE | re.MULTILINE)
            if author_match:
                self.author = author_match.group(1).strip()
                break
        
        # Extract date
        date_patterns = [
            r'Date:\s*(.*?)(?:\n|$)',
            r'Published:\s*(.*?)(?:\n|$)',
            r'^\s*DATE:\s*(.*?)(?:\n|$)',
            r'\((\d{4}(?:-\d{2}-\d{2})?)\)',
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})'
        ]
        
        for pattern in date_patterns:
            date_match = re.search(pattern, self.content, re.IGNORECASE | re.MULTILINE)
            if date_match:
                self.date = date_match.group(1).strip()
                break
    
    def _extract_abstract(self):
        abstract_patterns = [
            r'Abstract[:\s]+(.*?)(?:\n\n|\n[A-Z]|\n\d|\n\t|$)',
            r'ABSTRACT[:\s]+(.*?)(?:\n\n|\n[A-Z]|\n\d|\n\t|$)',
            r'Summary[:\s]+(.*?)(?:\n\n|\n[A-Z]|\n\d|\n\t|$)'
        ]
        
        for pattern in abstract_patterns:
            abstract_match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
            if abstract_match:
                raw_abstract = abstract_match.group(1).strip()
                self.abstract = re.sub(r'\n(?!\n)', ' ', raw_abstract)
                self.abstract = re.sub(r'\s+', ' ', self.abstract).strip()
                break
    
    def _extract_references(self):
        ref_section_patterns = [
            r'References:(.*?)(?:\n\n|$)',
            r'REFERENCES[:\s]+(.*?)(?:\n\n|$)',
            r'Bibliography:(.*?)(?:\n\n|$)',
            r'Works Cited:(.*?)(?:\n\n|$)'
        ]
        
        self.references = []
        
        for pattern in ref_section_patterns:
            ref_section = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
            if ref_section:
                ref_text = ref_section.group(1)
                
                # Try different reference formats
                ref_matches = re.findall(r'\[\d+\]\s*(.*?)(?:\.\s|\.\n|$)', ref_text)
                if ref_matches:
                    self.references.extend([ref.strip() for ref in ref_matches])
                    continue
                
                ref_matches = re.findall(r'\d+\.\s*(.*?)(?:\.\s|\.\n|$)', ref_text)
                if ref_matches:
                    self.references.extend([ref.strip() for ref in ref_matches])
                    continue
                
                ref_matches = re.findall(r'([A-Z][^\.]+\(\d{4}\)[^\.]+\.)', ref_text)
                if ref_matches:
                    self.references.extend([ref.strip() for ref in ref_matches])
                    continue
                
                if not self.references:
                    lines = [line.strip() for line in ref_text.split('\n') if line.strip()]
                    self.references.extend(lines)
        
        if not self.references:
            citations = re.findall(r'[\(\[]([\w\s]+,\s*\d{4})[\)\]]', self.content)
            self.references = list(set(citations))
    
    def _extract_keywords(self):
        keyword_patterns = [
            r'Keywords?[:\s]+(.*?)(?:\n\n|\n[A-Z]|\n\d|\n\t|$)',
            r'Key\s*words?[:\s]+(.*?)(?:\n\n|\n[A-Z]|\n\d|\n\t|$)',
            r'Tags?[:\s]+(.*?)(?:\n\n|\n[A-Z]|\n\d|\n\t|$)'
        ]
        
        for pattern in keyword_patterns:
            keyword_match = re.search(pattern, self.content, re.IGNORECASE | re.MULTILINE)
            if keyword_match:
                keyword_text = keyword_match.group(1).strip()
                if ';' in keyword_text:
                    self.keywords = [k.strip() for k in keyword_text.split(';')]
                else:
                    self.keywords = [k.strip() for k in keyword_text.split(',')]
                break
    
    def _extract_sections(self):
        section_pattern = r'(?:^|\n)(?:\d+\.\s*)?([A-Z][^a-z\n]{2,}[A-Za-z\s]+)(?:\n|\:)(.*?)(?=(?:\n(?:\d+\.\s*)?[A-Z][^a-z\n]{2,}[A-Za-z\s]+(?:\n|\:))|$)'
        
        section_matches = re.finditer(section_pattern, self.content, re.DOTALL)
        
        for match in section_matches:
            section_title = match.group(1).strip()
            section_content = match.group(2).strip()
            section_content = re.sub(r'\n+', '\n', section_content)
            self.sections[section_title] = section_content
    
    def get_citation_info(self):
        authors_cited = []
        
        citation_pattern = r'\(([A-Z][a-z]+(?:\s+et\s+al\.)?),\s*(\d{4})\)'
        citations = re.findall(citation_pattern, self.content)
        
        for author, year in citations:
            authors_cited.append(f"{author} ({year})")
        
        for ref in self.references:
            author_match = re.search(r'([A-Z][a-z]+(?:\s+et\s+al\.)?)[,\s]+\(?(\d{4})\)?', ref)
            if author_match:
                author, year = author_match.groups()
                authors_cited.append(f"{author} ({year})")
        
        return {
            "title": self.title,
            "author": self.author,
            "date": self.date,
            "authors_cited": list(set(authors_cited))
        }
    
    def get_content_summary(self):
        if self.abstract:
            if len(self.abstract) > 200:
                return self.abstract[:197] + "..."
            return self.abstract
        
        paragraphs = re.split(r'\n\s*\n', self.content)
        
        for paragraph in paragraphs:
            if ":" in paragraph or len(paragraph) < 50:
                continue
                
            if len(paragraph) > 200:
                return paragraph[:197] + "..."
            return paragraph
            
        for paragraph in paragraphs:
            if paragraph.strip():
                if len(paragraph) > 200:
                    return paragraph[:197] + "..."
                return paragraph
                
        return "No content summary available."
    
    def __str__(self):
        if self.author and self.date:
            return f"{self.title} by {self.author} ({self.date})"
        elif self.author:
            return f"{self.title} by {self.author}"
        else:
            return self.title

class DocumentAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Analysis System")
        self.root.geometry("900x700")
        
        # Documents list
        self.documents = []
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Document Management
        self.doc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.doc_frame, text="Document Management")
        
        # Document upload section
        upload_frame = ttk.LabelFrame(self.doc_frame, text="Upload Documents")
        upload_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(upload_frame, text="Add Documents", command=self.add_document).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Document list section with remove button
        list_frame = ttk.LabelFrame(self.doc_frame, text="Document List")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sorting options
        sort_frame = ttk.Frame(list_frame)
        sort_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Title", command=lambda: self.sort_documents("title")).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Author", command=lambda: self.sort_documents("author")).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Date", command=lambda: self.sort_documents("date")).pack(side=tk.LEFT, padx=5)
        
        # Remove button
        ttk.Button(sort_frame, text="Remove Selected", command=self.remove_document).pack(side=tk.RIGHT, padx=5)
        
        # Document listbox with multiple selection enabled
        self.doc_listbox = tk.Listbox(list_frame, height=10, selectmode=tk.MULTIPLE)
        self.doc_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 2: String Matching
        self.match_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.match_frame, text="String Matching")
        
        # File selection for string matching
        match_files_frame = ttk.LabelFrame(self.match_frame, text="Select Files to Compare")
        match_files_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # File 1 selection
        file1_frame = ttk.Frame(match_files_frame)
        file1_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(file1_frame, text="File 1:").pack(side=tk.LEFT, padx=5)
        self.file1_var = tk.StringVar()
        self.file1_combo = ttk.Combobox(file1_frame, textvariable=self.file1_var, width=50)
        self.file1_combo.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # File 2 selection
        file2_frame = ttk.Frame(match_files_frame)
        file2_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(file2_frame, text="File 2:").pack(side=tk.LEFT, padx=5)
        self.file2_var = tk.StringVar()
        self.file2_combo = ttk.Combobox(file2_frame, textvariable=self.file2_var, width=50)
        self.file2_combo.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Button for string matching
        ttk.Button(match_files_frame, text="Find Matches", 
                command=self.find_string_matches).pack(anchor=tk.W, padx=10, pady=5)
        
        # Naive search section
        naive_frame = ttk.LabelFrame(self.match_frame, text="Naive String Search")
        naive_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Pattern input
        pattern_frame = ttk.Frame(naive_frame)
        pattern_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(pattern_frame, text="Pattern:").pack(side=tk.LEFT, padx=5)
        self.pattern_entry = ttk.Entry(pattern_frame, width=50)
        self.pattern_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # File selection for naive search
        self.naive_file_var = tk.StringVar(value="file1")
        ttk.Radiobutton(naive_frame, text="Search in File 1", 
                        variable=self.naive_file_var, value="file1").pack(anchor=tk.W, padx=10)
        ttk.Radiobutton(naive_frame, text="Search in File 2", 
                        variable=self.naive_file_var, value="file2").pack(anchor=tk.W, padx=10)
        
        # Naive search button
        ttk.Button(naive_frame, text="Search", 
                command=self.perform_naive_search).pack(padx=10, pady=5)
        
        # Results area for string matching
        results_frame = ttk.LabelFrame(self.match_frame, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a summary section
        self.results_text = scrolledtext.ScrolledText(results_frame, height=7)
        self.results_text.pack(fill=tk.X, expand=False, padx=5, pady=5)
        self.results_text.tag_configure("highlight", background="yellow")
        self.results_text.tag_configure("title", font=("TkDefaultFont", 12, "bold"))
        self.results_text.tag_configure("section", font=("TkDefaultFont", 10, "bold"))
        self.results_text.tag_configure("alert", foreground="red")
        self.results_text.tag_configure("moderate", foreground="orange")
        self.results_text.tag_configure("info", foreground="blue")
        self.results_text.tag_configure("good", foreground="green")
        
        # Create a paned window for document display
        doc_paned = ttk.PanedWindow(results_frame, orient=tk.HORIZONTAL)
        doc_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Document 1 display
        doc1_frame = ttk.LabelFrame(doc_paned, text="Document 1")
        self.doc1_text = scrolledtext.ScrolledText(doc1_frame, wrap=tk.WORD)
        self.doc1_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.doc1_text.tag_configure("highlight", background="yellow")
        doc_paned.add(doc1_frame)
        
        # Document 2 display
        doc2_frame = ttk.LabelFrame(doc_paned, text="Document 2")
        self.doc2_text = scrolledtext.ScrolledText(doc2_frame, wrap=tk.WORD)
        self.doc2_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.doc2_text.tag_configure("highlight", background="yellow")
        doc_paned.add(doc2_frame)
        
        # Tab 3: Citation Graph
        self.graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="Citation Graph")
        
        # Create graph button
        ttk.Button(self.graph_frame, text="Create Citation Graph", 
                  command=self.create_citation_graph).pack(anchor=tk.W, padx=10, pady=10)
        
        # Graph display frame
        self.graph_display_frame = ttk.LabelFrame(self.graph_frame, text="Citation Graph Visualization")
        self.graph_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stats frame
        self.stats_frame = ttk.LabelFrame(self.graph_frame, text="Citation Statistics")
        self.stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_text = tk.Text(self.stats_frame, height=5, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 4: Compression
        self.compression_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.compression_frame, text="Compression")
        
        # Document selection for compression
        comp_select_frame = ttk.LabelFrame(self.compression_frame, text="Select Document")
        comp_select_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(comp_select_frame, text="Document:").pack(side=tk.LEFT, padx=5)
        self.compression_doc_var = tk.StringVar()
        self.compression_doc_combo = ttk.Combobox(comp_select_frame, textvariable=self.compression_doc_var, width=50)
        self.compression_doc_combo.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Compression buttons
        comp_buttons_frame = ttk.Frame(self.compression_frame)
        comp_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(comp_buttons_frame, text="Compress", 
                command=self.compress_document).pack(side=tk.LEFT, padx=5)
        ttk.Button(comp_buttons_frame, text="Decompress", 
                command=self.decompress_document).pack(side=tk.LEFT, padx=5)
        ttk.Button(comp_buttons_frame, text="Save Compressed File", 
                command=self.save_compressed_file).pack(side=tk.LEFT, padx=5)
        
        # Stats display
        self.compression_stats_frame = ttk.LabelFrame(self.compression_frame, text="Compression Statistics")
        self.compression_stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.compression_stats_text = tk.Text(self.compression_stats_frame, height=5, wrap=tk.WORD)
        self.compression_stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Content display
        content_frame = ttk.LabelFrame(self.compression_frame, text="Document Content")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text content
        self.original_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD)
        self.original_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def add_document(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Select Document(s)"
        )
        
        for file_path in file_paths:
            doc = DocumentInfo(file_path)
            self.documents.append(doc)
        
        self.update_document_list()
        self.update_file_combos()
    
    def remove_document(self):
        selected_indices = self.doc_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select document(s) to remove")
            return
        
        for index in sorted(selected_indices, reverse=True):
            del self.documents[index]
        
        self.update_document_list()
        self.update_file_combos()
    
    def update_document_list(self):
        self.doc_listbox.delete(0, tk.END)
        for doc in self.documents:
            self.doc_listbox.insert(tk.END, str(doc))
    
    def update_file_combos(self):
        doc_titles = [doc.title for doc in self.documents]
        
        # Update string matching combos
        self.file1_combo['values'] = doc_titles
        self.file2_combo['values'] = doc_titles
        
        # Update compression combo
        self.compression_doc_combo['values'] = doc_titles
        
        # Set defaults if documents are available
        if doc_titles:
            self.file1_combo.current(0)
            self.compression_doc_combo.current(0)
            if len(doc_titles) > 1:
                self.file2_combo.current(1)
            else:
                self.file2_combo.current(0)
    
    def sort_documents(self, sort_key):
        """
        Sort documents by title, author, or date using merge sort.
        
        Args:
            sort_key (str): Key to sort by ('title', 'author', or 'date')
        """
        if not self.documents:
            return
        
        # Create a list of document metadata for sorting
        docs_with_metadata = []
        for i, doc in enumerate(self.documents):
            # Store document and its metadata as [title, author, date, original_index]
            docs_with_metadata.append([
                doc.title if doc.title else "",
                doc.author if doc.author else "",
                doc.date if doc.date else "",
                i  # Store original index
            ])
        
        # Determine sort index based on key
        sort_index = 0  # title (default)
        if sort_key == "author":
            sort_index = 1
        elif sort_key == "date":
            sort_index = 2
        
        # Sort using our merge sort implementation
        merge_sort(docs_with_metadata, sort_index)
        
        # Reconstruct sorted document list
        sorted_docs = []
        for item in docs_with_metadata:
            original_index = item[3]
            sorted_docs.append(self.documents[original_index])
        
        # Update document list
        self.documents = sorted_docs
        self.update_document_list()
        
        # Show sorting feedback
        messagebox.showinfo("Sorting Complete", f"Documents sorted by {sort_key}")
    
    def find_string_matches(self):
        file1_title = self.file1_var.get()
        file2_title = self.file2_var.get()
        
        if not file1_title or not file2_title:
            messagebox.showwarning("Warning", "Please select two files to compare")
            return
        
        file1_content = None
        file2_content = None
        file1_doc = None
        file2_doc = None
        
        for doc in self.documents:
            if doc.title == file1_title:
                file1_content = doc.content
                file1_doc = doc
            if doc.title == file2_title:
                file2_content = doc.content
                file2_doc = doc
        
        if not file1_content or not file2_content:
            messagebox.showwarning("Warning", "Could not read one or both selected files")
            return
        
        # Clear all text displays
        self.results_text.delete(1.0, tk.END)
        self.doc1_text.delete(1.0, tk.END)
        self.doc2_text.delete(1.0, tk.END)
        
        # Show loading message
        self.results_text.insert(tk.END, "Analyzing documents for plagiarism...\n")
        self.results_text.update()
        
        # Get matches using the person2.py functionality
        matches = find_matches(file1_content, file2_content)
        
        # Display summary results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "📊 Plagiarism Detection Results\n\n", "title")
        
        self.results_text.insert(tk.END, "📄 Document Summary\n", "section")
        self.results_text.insert(tk.END, f"Document 1: {file1_doc.title}\n")
        if file1_doc.author:
            self.results_text.insert(tk.END, f"Author: {file1_doc.author}\n")
        
        self.results_text.insert(tk.END, f"\nDocument 2: {file2_doc.title}\n")
        if file2_doc.author:
            self.results_text.insert(tk.END, f"Author: {file2_doc.author}\n")
        
        similarity = matches.get("similarity_percentage", 0)
        self.results_text.insert(tk.END, f"\n🔍 Similarity Analysis\n", "section")
        
        bar_length = 20
        filled_bars = int((similarity / 100) * bar_length)
        similarity_display = "█" * filled_bars + "░" * (bar_length - filled_bars)
        
        self.results_text.insert(tk.END, f"Similarity Score: {similarity:.2f}%\n")
        self.results_text.insert(tk.END, f"{similarity_display}\n")
        
        if similarity > 75:
            self.results_text.insert(tk.END, "⚠️ Very high similarity detected! Significant plagiarism likely.\n", "alert")
        elif similarity > 50:
            self.results_text.insert(tk.END, "⚠️ High similarity detected. Substantial plagiarism likely.\n", "alert")
        elif similarity > 25:
            self.results_text.insert(tk.END, "⚠️ Moderate similarity detected. Some plagiarism possible.\n", "moderate")
        elif similarity > 10:
            self.results_text.insert(tk.END, "ℹ️ Low similarity detected. May involve common phrases only.\n", "info")
        else:
            self.results_text.insert(tk.END, "✓ Minimal similarity. Documents appear to be distinct.\n", "good")
            
        # Display document contents
        self.doc1_text.insert(tk.END, file1_content)
        self.doc2_text.insert(tk.END, file2_content)
        
        # Get the matched phrases for highlighting
        matched_phrases = matches.get("unique_matches", [])
        
        # Highlight matched phrases in both documents
        self.highlight_matched_content(file1_content, file2_content, matched_phrases)
    
    def highlight_matched_content(self, doc1_content, doc2_content, matched_phrases):
        """
        Highlight matching phrases in both document displays.
        
        Args:
            doc1_content (str): Content of first document
            doc2_content (str): Content of second document
            matched_phrases (list): List of matched phrases to highlight
        """
        from person2 import highlight_matched_phrases
        
        # Process each document
        for phrase in matched_phrases:
            # Find all instances of phrase in document 1
            doc1_indices = self.find_phrase_indices(doc1_content.lower(), phrase.lower())
            for start_idx in doc1_indices:
                end_idx = start_idx + len(phrase)
                # Convert to tkinter text widget indices
                start = f"1.0+{start_idx}c"
                end = f"1.0+{end_idx}c"
                # Add the highlight tag
                self.doc1_text.tag_add("highlight", start, end)
            
            # Find all instances of phrase in document 2
            doc2_indices = self.find_phrase_indices(doc2_content.lower(), phrase.lower())
            for start_idx in doc2_indices:
                end_idx = start_idx + len(phrase)
                # Convert to tkinter text widget indices
                start = f"1.0+{start_idx}c"
                end = f"1.0+{end_idx}c"
                # Add the highlight tag
                self.doc2_text.tag_add("highlight", start, end)
    
    def find_phrase_indices(self, text, phrase):
        """
        Find all occurrences of a phrase in text.
        
        Args:
            text (str): Text to search in
            phrase (str): Phrase to find
            
        Returns:
            list: List of indices where the phrase starts
        """
        indices = []
        start_idx = 0
        
        while True:
            idx = text.find(phrase, start_idx)
            if idx == -1:
                break
            indices.append(idx)
            start_idx = idx + 1
            
        return indices
    
    def perform_naive_search(self):
        pattern = self.pattern_entry.get().strip()
        if not pattern:
            messagebox.showwarning("Warning", "Please enter a pattern to search for")
            return
        
        file_var = self.naive_file_var.get()
        file_title = self.file1_var.get() if file_var == "file1" else self.file2_var.get()
        
        file_content = None
        for doc in self.documents:
            if doc.title == file_title:
                file_content = doc.content
                break
        
        if not file_content:
            messagebox.showwarning("Warning", f"Please select a valid file for {file_var}")
            return
        
        self.results_text.delete(1.0, tk.END)
        
        positions = naive_search(file_content, pattern)
        
        self.results_text.insert(tk.END, f"Naive Search Results for pattern \"{pattern}\" in {file_title}:\n\n")
        
        if not positions:
            self.results_text.insert(tk.END, "No matches found.\n")
        else:
            self.results_text.insert(tk.END, f"Found {len(positions)} matches at positions: {positions}\n")
            
            for i, pos in enumerate(positions, 1):
                start = max(0, pos - 20)
                end = min(len(file_content), pos + len(pattern) + 20)
                
                pre_context = file_content[start:pos].replace('\n', ' ')
                highlight = file_content[pos:pos+len(pattern)].replace('\n', ' ')
                post_context = file_content[pos+len(pattern):end].replace('\n', ' ')
                
                self.results_text.insert(tk.END, f"\n{i}. ...{pre_context}")
                self.results_text.insert(tk.END, f"{highlight}", "highlight")
                self.results_text.insert(tk.END, f"{post_context}...\n")
    
    def create_citation_graph(self):
        if len(self.documents) < 2:
            messagebox.showwarning("Warning", "Please add at least two documents to create a citation graph")
            return
        
        for widget in self.graph_display_frame.winfo_children():
            widget.destroy()
        
        citation_graph = self._build_citation_graph()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        graph_frame = ttk.Frame(self.graph_display_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        G = nx.DiGraph(citation_graph)
        pos = nx.spring_layout(G, seed=42)
        
        nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue', ax=ax)
        nx.draw_networkx_edges(G, pos, width=1.0, edge_color='gray', arrowsize=15, ax=ax)
        
        labels = {}
        for node in G.nodes():
            if len(node) > 20:
                labels[node] = node[:17] + "..."
            else:
                labels[node] = node
                
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight='bold', ax=ax)
        
        ax.set_title("Citation Network")
        ax.axis('off')
        
        canvas.draw()
        
        self.update_graph_stats(G)
    
    def _build_citation_graph(self):
        citation_graph = {}
        
        for doc in self.documents:
            citation_graph[doc.title] = []
        
        for doc in self.documents:
            citation_info = doc.get_citation_info()
            authors_cited = citation_info.get("authors_cited", [])
            
            for cited_author in authors_cited:
                for target_doc in self.documents:
                    if target_doc.author and cited_author and target_doc.author in cited_author:
                        if target_doc.title not in citation_graph[doc.title] and target_doc.title != doc.title:
                            citation_graph[doc.title].append(target_doc.title)
            
            for ref in doc.references:
                for target_doc in self.documents:
                    if target_doc.title in citation_graph[doc.title] or target_doc.title == doc.title:
                        continue
                        
                    if target_doc.author and target_doc.author in ref:
                        citation_graph[doc.title].append(target_doc.title)
                        break
                        
                    if target_doc.title and any(word in ref.lower() for word in target_doc.title.lower().split()):
                        citation_graph[doc.title].append(target_doc.title)
                        break
        
        return citation_graph
    
    def update_graph_stats(self, graph):
        self.stats_text.delete(1.0, tk.END)
        
        num_nodes = graph.number_of_nodes()
        num_edges = graph.number_of_edges()
        
        if num_nodes == 0:
            self.stats_text.insert(tk.END, "No documents in the citation graph.")
            return
        
        stats = f"Basic Statistics:\n"
        stats += f"• Number of documents: {num_nodes}\n"
        stats += f"• Number of citations: {num_edges}\n"
        
        if num_nodes > 1:
            max_possible_edges = num_nodes * (num_nodes - 1)
            density = (num_edges / max_possible_edges) * 100 if max_possible_edges > 0 else 0
            stats += f"• Network density: {density:.2f}%\n"
        
        self.stats_text.insert(tk.END, stats)
    
    def compress_document(self):
        """
        Compress the selected document using Huffman coding.
        """
        doc_title = self.compression_doc_var.get()
        if not doc_title:
            messagebox.showwarning("Warning", "Please select a document to compress")
            return
        
        selected_doc = None
        for doc in self.documents:
            if doc.title == doc_title:
                selected_doc = doc
                break
        
        if not selected_doc:
            messagebox.showwarning("Warning", "Could not find the selected document")
            return
        
        # Clear existing content
        self.compression_stats_text.delete(1.0, tk.END)
        self.original_text.delete(1.0, tk.END)
        
        # Show original content
        self.original_text.insert(tk.END, selected_doc.content)
        
        try:
            # Use our simplified Huffman implementation
            from Huffman import Huffman
            huffman = Huffman()
            
            # Compress the document content
            compressed_data = huffman.compress_text(selected_doc.content)
            
            # Store compressed data with the document
            selected_doc.compressed_data = compressed_data
            selected_doc.huffman_instance = huffman
            
            # Get and display compression statistics
            stats = huffman.get_compression_stats()
            self._display_compression_stats(stats)
            
            # Show success message
            messagebox.showinfo("Compression Complete", 
                               f"Document compressed! Size reduced from {stats['original_size']:,} bytes to {stats['compressed_size']:,} bytes.")
            
        except Exception as e:
            messagebox.showerror("Compression Error", f"Error during compression: {str(e)}")
            self.compression_stats_text.insert(tk.END, f"Error: {str(e)}")
    
    def _display_compression_stats(self, stats):
        """
        Display compression statistics in the stats text area.
        
        Args:
            stats (dict): Compression statistics from Huffman.get_compression_stats()
        """
        self.compression_stats_text.delete(1.0, tk.END)
        
        self.compression_stats_text.insert(tk.END, "📊 Compression Results\n\n", "title")
        
        original_bytes = stats["original_size"]
        self.compression_stats_text.insert(tk.END, f"Original size: {original_bytes:,} bytes\n")
        
        compressed_bytes = stats["compressed_size"]
        self.compression_stats_text.insert(tk.END, f"Compressed size: {compressed_bytes:,} bytes\n")
        
        compression_ratio = stats["compression_ratio"]
        space_saving = stats["space_saving"]
        
        # Determine the compression quality indicator
        indicator = "Minimal ⚠️"
        if space_saving > 75:
            indicator = "Excellent! 🌟"
        elif space_saving > 50:
            indicator = "Very good! ✓"
        elif space_saving > 25:
            indicator = "Good ✓"
        
        # Display the compression ratio and space saving
        self.compression_stats_text.insert(tk.END, f"Compression ratio: {compression_ratio:.2f}x {indicator}\n")
        self.compression_stats_text.insert(tk.END, f"Space saved: {space_saving:.2f}%\n")
        
        # Add a visual bar to show compression ratio
        if original_bytes > 0:
            bar_length = 20
            filled_bars = int((compressed_bytes / original_bytes) * bar_length)
            compression_display = "█" * filled_bars + "░" * (bar_length - filled_bars)
            self.compression_stats_text.insert(tk.END, f"\nCompression visualization: \n{compression_display}\n")
        
        # Configure text tags
        self.compression_stats_text.tag_configure("title", font=("TkDefaultFont", 12, "bold"))
    
    def decompress_document(self):
        """
        Decompress the selected document using Huffman coding.
        """
        doc_title = self.compression_doc_var.get()
        if not doc_title:
            messagebox.showwarning("Warning", "Please select a document to decompress")
            return
        
        selected_doc = None
        for doc in self.documents:
            if doc.title == doc_title:
                selected_doc = doc
                break
        
        if not selected_doc:
            messagebox.showwarning("Warning", "Could not find the selected document")
            return
        
        if not hasattr(selected_doc, 'compressed_data') or not hasattr(selected_doc, 'huffman_instance'):
            messagebox.showwarning("Warning", "Please compress the document first")
            return
        
        try:
            # Get the Huffman instance stored with the document
            huffman = selected_doc.huffman_instance
            
            # Decompress the data
            decompressed_text = huffman.decompress_data(selected_doc.compressed_data)
            
            # Display the decompressed text
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(tk.END, decompressed_text)
            
            # Verify the decompression
            if decompressed_text == selected_doc.content:
                self.compression_stats_text.insert(tk.END, "\n✅ Verification: Decompression successful!\n")
                self.compression_stats_text.insert(tk.END, "The decompressed text matches the original document.")
            else:
                self.compression_stats_text.insert(tk.END, "\n⚠️ Warning: Decompressed data differs from original!\n")
                self.compression_stats_text.insert(tk.END, "There may be issues with the compression/decompression process.")
            
        except Exception as e:
            messagebox.showerror("Decompression Error", f"Error during decompression: {str(e)}")
            self.compression_stats_text.insert(tk.END, f"\n\nError: {str(e)}")
    
    def save_compressed_file(self):
        """
        Save the compressed data to a file.
        """
        doc_title = self.compression_doc_var.get()
        if not doc_title:
            messagebox.showwarning("Warning", "Please select a document to save")
            return
        
        selected_doc = None
        for doc in self.documents:
            if doc.title == doc_title:
                selected_doc = doc
                break
        
        if not selected_doc:
            messagebox.showwarning("Warning", "Could not find the selected document")
            return
        
        if not hasattr(selected_doc, 'compressed_data'):
            messagebox.showwarning("Warning", "Please compress the document first")
            return
        
        # Show save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")],
            initialfile=f"{selected_doc.title.replace(' ', '_')}_compressed.bin"
        )
        
        if not file_path:
            return  # User canceled the dialog
        
        try:
            # Write compressed data to file
            with open(file_path, "wb") as file:
                file.write(selected_doc.compressed_data)
            
            messagebox.showinfo("Save Successful", f"Compressed file saved to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentAnalysisGUI(root)
    root.mainloop()
