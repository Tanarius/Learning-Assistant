#!/usr/bin/env python3
"""
Learning Assistant Bot - Technical Knowledge Extractor
=====================================================

Analyzes code you've built and generates personalized learning materials.
Perfect for understanding what you've accomplished and preparing for interviews.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import os
import re
import ast
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading

class LearningAssistant:
    def __init__(self):
        self.knowledge_base = {
            'concepts': {},
            'technologies': {},
            'patterns': {},
            'interview_questions': [],
            'learning_path': []
        }
    
    def analyze_codebase(self, directory_path="."):
        """Analyze all Python files in directory"""
        analysis = {
            'files_analyzed': [],
            'imports_used': set(),
            'classes_found': [],
            'functions_found': [],
            'concepts_identified': set(),
            'complexity_patterns': [],
            'interview_topics': set()
        }
        
        python_files = list(Path(directory_path).glob("*.py"))
        
        for file_path in python_files:
            if self.should_analyze_file(file_path):
                file_analysis = self.analyze_python_file(file_path)
                
                analysis['files_analyzed'].append(str(file_path))
                analysis['imports_used'].update(file_analysis['imports'])
                analysis['classes_found'].extend(file_analysis['classes'])
                analysis['functions_found'].extend(file_analysis['functions'])
                analysis['concepts_identified'].update(file_analysis['concepts'])
                analysis['complexity_patterns'].extend(file_analysis['patterns'])
                analysis['interview_topics'].update(file_analysis['interview_topics'])
        
        return analysis
    
    def should_analyze_file(self, file_path):
        """Check if file should be analyzed"""
        filename = file_path.name
        
        # Skip certain files
        skip_patterns = ['__pycache__', '.pyc', 'test_', '_test']
        if any(pattern in filename for pattern in skip_patterns):
            return False
        
        # Focus on our main bot files
        focus_files = [
            'job-bot', 'tailored-apply-bot', 'github-dev-logger', 
            'github-development-logger', 'learning-assistant'
        ]
        
        return any(pattern in filename for pattern in focus_files)
    
    def analyze_python_file(self, file_path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return self.fallback_analysis(content)
            
            analysis = {
                'imports': set(),
                'classes': [],
                'functions': [],
                'concepts': set(),
                'patterns': [],
                'interview_topics': set()
            }
            
            # Analyze AST
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].add(alias.name)
                        analysis['concepts'].update(self.map_import_to_concepts(alias.name))
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].add(node.module)
                        analysis['concepts'].update(self.map_import_to_concepts(node.module))
                
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        'file': file_path.name
                    }
                    analysis['classes'].append(class_info)
                    analysis['concepts'].add('object_oriented_programming')
                    analysis['interview_topics'].add('class_design')
                
                elif isinstance(node, ast.FunctionDef):
                    if not self.is_method(node, tree):  # Only count standalone functions
                        func_info = {
                            'name': node.name,
                            'args': len(node.args.args),
                            'file': file_path.name
                        }
                        analysis['functions'].append(func_info)
            
            # Text-based analysis for patterns
            analysis['patterns'].extend(self.identify_patterns(content))
            analysis['interview_topics'].update(self.identify_interview_topics(content))
            
            return analysis
            
        except Exception as e:
            return self.fallback_analysis(content if 'content' in locals() else "")
    
    def is_method(self, func_node, tree):
        """Check if function is a method inside a class"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item == func_node:
                        return True
        return False
    
    def fallback_analysis(self, content):
        """Simple text-based analysis if AST fails"""
        analysis = {
            'imports': set(),
            'classes': [],
            'functions': [],
            'concepts': set(),
            'patterns': [],
            'interview_topics': set()
        }
        
        # Find imports with regex
        import_matches = re.findall(r'(?:from\s+(\w+)|import\s+(\w+))', content)
        for match in import_matches:
            module = match[0] or match[1]
            if module:
                analysis['imports'].add(module)
                analysis['concepts'].update(self.map_import_to_concepts(module))
        
        return analysis
    
    def map_import_to_concepts(self, module_name):
        """Map imports to programming concepts"""
        concept_map = {
            'tkinter': ['gui_programming', 'event_driven_programming', 'desktop_applications'],
            'requests': ['http_apis', 'web_requests', 'network_programming'],
            'beautifulsoup4': ['web_scraping', 'html_parsing', 'data_extraction'],
            'bs4': ['web_scraping', 'html_parsing', 'data_extraction'],
            'threading': ['concurrency', 'parallel_processing', 'background_tasks'],
            'json': ['data_serialization', 'api_communication', 'data_formats'],
            'datetime': ['time_handling', 'data_processing', 'timestamp_management'],
            'pathlib': ['file_system_operations', 'modern_python', 'path_handling'],
            'os': ['system_operations', 'file_management', 'cross_platform'],
            'sys': ['system_programming', 'command_line', 'python_internals'],
            're': ['regular_expressions', 'text_processing', 'pattern_matching'],
            'ast': ['code_analysis', 'meta_programming', 'syntax_trees'],
            'subprocess': ['process_management', 'system_integration', 'external_commands']
        }
        
        return concept_map.get(module_name, [])
    
    def identify_patterns(self, content):
        """Identify programming patterns in code"""
        patterns = []
        
        # GUI patterns
        if 'ttk.Frame' in content and 'grid' in content:
            patterns.append({
                'name': 'GUI Layout Management',
                'description': 'Using tkinter grid system for widget positioning',
                'example': 'ttk.Frame().grid(row=0, column=0)',
                'concept': 'GUI layout managers'
            })
        
        if 'threading.Thread' in content:
            patterns.append({
                'name': 'Background Processing',
                'description': 'Using threads to prevent GUI freezing during long operations',
                'example': 'thread = threading.Thread(target=function)',
                'concept': 'Concurrent programming'
            })
        
        # API patterns
        if 'requests.get' in content:
            patterns.append({
                'name': 'REST API Consumption',
                'description': 'Making HTTP requests to external APIs',
                'example': 'requests.get(url, headers=headers)',
                'concept': 'API integration'
            })
        
        # Error handling patterns
        if 'try:' in content and 'except' in content:
            patterns.append({
                'name': 'Exception Handling',
                'description': 'Graceful error handling and user feedback',
                'example': 'try/except blocks with user notifications',
                'concept': 'Robust error handling'
            })
        
        # Data processing patterns
        if 'BeautifulSoup' in content:
            patterns.append({
                'name': 'Web Scraping',
                'description': 'Extracting data from HTML using CSS selectors',
                'example': 'soup.select_one(selector)',
                'concept': 'Data extraction from web pages'
            })
        
        return patterns
    
    def identify_interview_topics(self, content):
        """Identify relevant interview topics from code"""
        topics = set()
        
        # Technical topics
        if 'class ' in content:
            topics.add('object_oriented_programming')
        
        if 'def ' in content:
            topics.add('function_design')
        
        if 'requests.' in content:
            topics.add('api_integration')
        
        if 'threading' in content:
            topics.add('concurrency')
        
        if 'tkinter' in content:
            topics.add('gui_development')
        
        if 'json.' in content:
            topics.add('data_formats')
        
        if '.get(' in content or '.post(' in content:
            topics.add('http_methods')
        
        if 'try:' in content:
            topics.add('error_handling')
        
        return topics
    
    def generate_learning_report(self, analysis):
        """Generate comprehensive learning report"""
        report = {
            'summary': self.generate_summary(analysis),
            'concepts_learned': self.generate_concepts_explanation(analysis),
            'technologies_mastered': self.generate_tech_explanation(analysis),
            'interview_preparation': self.generate_interview_prep(analysis),
            'next_learning_steps': self.generate_learning_path(analysis),
            'practical_examples': self.generate_examples(analysis)
        }
        
        return report
    
    def generate_summary(self, analysis):
        """Generate executive summary of learning"""
        files_count = len(analysis['files_analyzed'])
        concepts_count = len(analysis['concepts_identified'])
        imports_count = len(analysis['imports_used'])
        
        summary = f"""LEARNING SUMMARY - {datetime.now().strftime('%Y-%m-%d')}

📊 CODE ANALYSIS RESULTS:
• Files Analyzed: {files_count} Python applications
• Technologies Used: {imports_count} different libraries/modules  
• Programming Concepts Applied: {concepts_count} distinct concepts
• Classes Designed: {len(analysis['classes_found'])} object-oriented structures
• Functions Written: {len(analysis['functions_found'])} reusable functions

🎯 SKILL DEVELOPMENT EVIDENCE:
You've successfully implemented professional-grade automation tools demonstrating:
• GUI Development (tkinter applications with complex layouts)
• API Integration (GitHub API, web scraping with requests/BeautifulSoup)
• Concurrent Programming (background threading for responsive UIs)
• Data Processing (JSON handling, text analysis, content generation)
• Software Architecture (modular design, class hierarchies, separation of concerns)

💼 CAREER TRANSITION PROGRESS:
Infrastructure Engineer → AI/Automation Specialist
✓ Practical Python development experience
✓ API integration and data processing skills
✓ User interface design and development
✓ System automation and content generation
✓ Professional documentation and code organization

This analysis shows you've moved beyond basic scripting to building complete applications with professional software engineering practices."""
        
        return summary
    
    def generate_concepts_explanation(self, analysis):
        """Explain programming concepts found in code"""
        explanations = {}
        
        concept_definitions = {
            'gui_programming': {
                'definition': 'Creating graphical user interfaces with windows, buttons, and interactive elements',
                'your_usage': 'Built desktop applications using tkinter with professional layouts, tabs, and user interaction',
                'interview_answer': 'I\'ve created GUI applications using tkinter, implementing features like tabbed interfaces, background processing, and responsive user interactions. My Job Bot and GitHub Logger demonstrate practical GUI development skills.'
            },
            
            'api_integration': {
                'definition': 'Connecting applications to external services and data sources via APIs',
                'your_usage': 'Integrated GitHub API for activity data and implemented web scraping for job postings',
                'interview_answer': 'I have experience with REST API consumption using the requests library. I\'ve integrated the GitHub API to fetch user activity data and implemented web scraping to extract job posting information from various career sites.'
            },
            
            'concurrency': {
                'definition': 'Running multiple operations simultaneously or in parallel',
                'your_usage': 'Used threading to prevent GUI freezing during network requests and data processing',
                'interview_answer': 'I\'ve implemented multi-threading in GUI applications to maintain responsiveness during long-running operations like API calls and web scraping. This prevents the user interface from freezing and improves user experience.'
            },
            
            'web_scraping': {
                'definition': 'Automatically extracting data from websites and web pages',
                'your_usage': 'Built job posting scraper using BeautifulSoup to extract company names, job titles, and descriptions',
                'interview_answer': 'I\'ve developed web scraping solutions using BeautifulSoup to extract structured data from HTML pages. My job application bot scrapes job postings from multiple platforms and intelligently extracts relevant information.'
            },
            
            'object_oriented_programming': {
                'definition': 'Programming paradigm using classes and objects to organize code',
                'your_usage': 'Designed GUI applications as classes with methods for different functionalities',
                'interview_answer': 'I structure my applications using OOP principles, creating classes that encapsulate related functionality. My GUI applications are built as classes with methods for different operations, making the code organized and maintainable.'
            }
        }
        
        for concept in analysis['concepts_identified']:
            if concept in concept_definitions:
                explanations[concept] = concept_definitions[concept]
        
        return explanations
    
    def generate_tech_explanation(self, analysis):
        """Explain technologies used"""
        tech_explanations = {}
        
        tech_details = {
            'tkinter': {
                'what_it_is': 'Python\'s built-in GUI framework for creating desktop applications',
                'how_you_used_it': 'Created professional desktop applications with complex layouts, tabs, buttons, and text areas',
                'business_value': 'Enables rapid development of desktop tools without additional dependencies',
                'interview_talking_point': 'I\'ve built complete desktop applications using tkinter, including multi-tab interfaces and background processing integration'
            },
            
            'requests': {
                'what_it_is': 'HTTP library for making web requests and API calls',
                'how_you_used_it': 'Integrated with GitHub API and scraped job posting websites',
                'business_value': 'Essential for connecting applications to external data sources and services',
                'interview_talking_point': 'I use requests for API integration and web scraping, handling authentication, error cases, and data extraction'
            },
            
            'bs4': {
                'what_it_is': 'BeautifulSoup - library for parsing HTML and extracting data from web pages',
                'how_you_used_it': 'Built intelligent job posting scraper that extracts structured data from various career sites',
                'business_value': 'Enables automation of data collection from websites without APIs',
                'interview_talking_point': 'I\'ve implemented web scraping solutions that intelligently extract data from HTML using CSS selectors and handle different site structures'
            },
            
            'threading': {
                'what_it_is': 'Python module for concurrent execution and background processing',
                'how_you_used_it': 'Prevented GUI applications from freezing during network operations',
                'business_value': 'Critical for responsive user interfaces and efficient resource utilization',
                'interview_talking_point': 'I implement threading to maintain responsive UIs during long-running operations, ensuring good user experience'
            },
            
            'json': {
                'what_it_is': 'Standard format for data exchange and storage',
                'how_you_used_it': 'Processed API responses and stored application data in structured format',
                'business_value': 'Universal data format for APIs, configuration, and data persistence',
                'interview_talking_point': 'I work with JSON for API communication and data storage, handling parsing and serialization in my applications'
            }
        }
        
        for tech in analysis['imports_used']:
            if tech in tech_details:
                tech_explanations[tech] = tech_details[tech]
        
        return tech_explanations
    
    def generate_interview_prep(self, analysis):
        """Generate interview questions and answers based on code"""
        questions = []
        
        # Based on identified concepts
        if 'gui_programming' in analysis['concepts_identified']:
            questions.append({
                'question': 'Describe your experience with GUI development.',
                'your_answer': 'I\'ve built desktop applications using tkinter, creating professional interfaces with tabbed layouts, background processing, and responsive user interactions. My applications include features like progress bars, multi-threaded operations, and organized file output.',
                'technical_details': 'Used tkinter widgets, grid layout management, event handling, and threading integration'
            })
        
        if 'api_integration' in analysis['concepts_identified']:
            questions.append({
                'question': 'How do you handle API integration and error cases?',
                'your_answer': 'I use the requests library with proper error handling, timeouts, and user feedback. My GitHub Logger integrates with the GitHub API to fetch user activity data, and my Job Bot scrapes multiple job sites with fallback strategies.',
                'technical_details': 'Implemented HTTP requests with headers, error handling, timeouts, and response parsing'
            })
        
        if 'web_scraping' in analysis['concepts_identified']:
            questions.append({
                'question': 'Explain your approach to web scraping and data extraction.',
                'your_answer': 'I use BeautifulSoup for HTML parsing with multiple CSS selector strategies to handle different website structures. My job application bot extracts company names, job titles, and descriptions from various career sites.',
                'technical_details': 'CSS selectors, HTML parsing, fallback strategies, and structured data extraction'
            })
        
        if 'concurrency' in analysis['concepts_identified']:
            questions.append({
                'question': 'How do you handle concurrent operations in your applications?',
                'your_answer': 'I implement threading to prevent GUI freezing during long operations like API calls. My applications use background threads for network requests while keeping the user interface responsive.',
                'technical_details': 'Threading module, daemon threads, GUI thread safety, and background processing'
            })
        
        # Add general questions based on the projects
        questions.extend([
            {
                'question': 'Tell me about a complex project you\'ve built.',
                'your_answer': 'I built a job application automation suite that includes web scraping, content generation, and GUI interfaces. It demonstrates full-stack development skills from data extraction to user interface design.',
                'technical_details': 'Multi-file architecture, modular design, error handling, and user experience considerations'
            },
            
            {
                'question': 'How do you approach learning new technologies?',
                'your_answer': 'I learn by building real projects that solve actual problems. My transition from Infrastructure to AI/Automation involved building practical tools while documenting the learning process publicly.',
                'technical_details': 'Project-based learning, documentation, iterative development, and continuous improvement'
            }
        ])
        
        return questions
    
    def generate_learning_path(self, analysis):
        """Suggest next learning steps"""
        current_skills = analysis['concepts_identified']
        
        learning_path = []
        
        # Beginner to Intermediate progression
        if 'gui_programming' in current_skills:
            learning_path.append({
                'topic': 'Advanced GUI Frameworks',
                'description': 'Learn PyQt or Kivy for more sophisticated desktop applications',
                'why_useful': 'Better for complex applications and mobile development',
                'next_project': 'Build a data visualization dashboard'
            })
        
        if 'api_integration' in current_skills:
            learning_path.append({
                'topic': 'API Development',
                'description': 'Learn Flask/FastAPI to build your own APIs',
                'why_useful': 'Complete the full-stack picture by creating backend services',
                'next_project': 'Build a REST API for your Memory Platform'
            })
        
        if 'web_scraping' in current_skills:
            learning_path.append({
                'topic': 'Advanced Scraping',
                'description': 'Learn Selenium for JavaScript-heavy sites and anti-bot measures',
                'why_useful': 'Handle more complex websites and automation scenarios',
                'next_project': 'Scrape dynamic job sites that load content with JavaScript'
            })
        
        # AI/ML progression
        learning_path.append({
            'topic': 'Machine Learning Basics',
            'description': 'Learn scikit-learn for basic ML models and data analysis',
            'why_useful': 'Direct step toward AI specialization goal',
            'next_project': 'Add intelligent job matching to your application bot'
        })
        
        learning_path.append({
            'topic': 'Database Integration',
            'description': 'Learn SQLAlchemy or direct database integration',
            'why_useful': 'Store and analyze your application data persistently',
            'next_project': 'Add database backend to track job application success rates'
        })
        
        return learning_path
    
    def generate_examples(self, analysis):
        """Generate practical code examples to study"""
        examples = []
        
        for pattern in analysis['complexity_patterns']:
            examples.append({
                'concept': pattern['concept'],
                'explanation': pattern['description'],
                'code_snippet': pattern['example'],
                'study_focus': f"Understand how {pattern['name']} works in your applications"
            })
        
        return examples

class LearningAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.assistant = LearningAssistant()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("Learning Assistant - Technical Knowledge Extractor")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1000x800+{x}+{y}")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Learning Assistant", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Analyze your code to understand what you've learned and prepare for interviews",
                                  font=('Arial', 10))
        subtitle_label.pack(anchor=tk.W)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.analyze_btn = ttk.Button(control_frame, text="Analyze My Code", 
                                     command=self.start_analysis,
                                     style='Accent.TButton')
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="Choose Directory", 
                  command=self.choose_directory).pack(side=tk.LEFT, padx=(0, 10))
        
        self.directory_var = tk.StringVar(value="Current Directory")
        ttk.Label(control_frame, textvariable=self.directory_var).pack(side=tk.LEFT)
        
        # Progress
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT)
        
        # Results notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Summary tab
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Learning Summary")
        
        self.summary_text = scrolledtext.ScrolledText(
            self.summary_frame, wrap=tk.WORD, font=('Arial', 10)
        )
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Concepts tab
        self.concepts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.concepts_frame, text="Concepts Learned")
        
        self.concepts_text = scrolledtext.ScrolledText(
            self.concepts_frame, wrap=tk.WORD, font=('Arial', 10)
        )
        self.concepts_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Technologies tab
        self.tech_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tech_frame, text="Technologies Mastered")
        
        self.tech_text = scrolledtext.ScrolledText(
            self.tech_frame, wrap=tk.WORD, font=('Arial', 10)
        )
        self.tech_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Interview prep tab
        self.interview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.interview_frame, text="Interview Preparation")
        
        self.interview_text = scrolledtext.ScrolledText(
            self.interview_frame, wrap=tk.WORD, font=('Arial', 10)
        )
        self.interview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Learning path tab
        self.learning_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.learning_frame, text="Next Learning Steps")
        
        self.learning_text = scrolledtext.ScrolledText(
            self.learning_frame, wrap=tk.WORD, font=('Arial', 10)
        )
        self.learning_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.save_btn = ttk.Button(button_frame, text="Save Learning Report", 
                                  command=self.save_report, state='disabled')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Export for Resume", 
                  command=self.export_for_resume, state='disabled').pack(side=tk.LEFT)
        
        self.current_analysis = None
        self.current_directory = "."
    
    def choose_directory(self):
        """Let user choose directory to analyze"""
        directory = filedialog.askdirectory(title="Choose directory to analyze")
        if directory:
            self.current_directory = directory
            self.directory_var.set(f"Directory: {Path(directory).name}")
    
    def start_analysis(self):
        """Start code analysis in background"""
        self.analyze_btn.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self.perform_analysis)
        thread.daemon = True
        thread.start()
    
    def perform_analysis(self):
        """Perform analysis in background thread"""
        try:
            # Analyze codebase
            analysis = self.assistant.analyze_codebase(self.current_directory)
            
            # Generate learning report
            report = self.assistant.generate_learning_report(analysis)
            
            # Update GUI
            self.root.after(0, lambda: self.display_results(analysis, report))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Analysis Error", str(e)))
        
        self.root.after(0, lambda: self.progress.stop())
        self.root.after(0, lambda: self.analyze_btn.config(state='normal'))
    
    def display_results(self, analysis, report):
        """Display analysis results"""
        self.current_analysis = {'analysis': analysis, 'report': report}
        
        # Clear all text areas
        for text_widget in [self.summary_text, self.concepts_text, self.tech_text, 
                           self.interview_text, self.learning_text]:
            text_widget.delete(1.0, tk.END)
        
        # Populate summary
        self.summary_text.insert(1.0, report['summary'])
        
        # Populate concepts
        concepts_content = "PROGRAMMING CONCEPTS YOU'VE MASTERED\n" + "="*50 + "\n\n"
        for concept, details in report['concepts_learned'].items():
            concepts_content += f"📚 {concept.replace('_', ' ').title()}\n"
            concepts_content += f"Definition: {details['definition']}\n"
            concepts_content += f"How you used it: {details['your_usage']}\n"
            concepts_content += f"Interview answer: {details['interview_answer']}\n\n"
        
        self.concepts_text.insert(1.0, concepts_content)
        
        # Populate technologies
        tech_content = "TECHNOLOGIES YOU'VE LEARNED\n" + "="*40 + "\n\n"
        for tech, details in report['technologies_mastered'].items():
            tech_content += f"⚙️ {tech.upper()}\n"
            tech_content += f"What it is: {details['what_it_is']}\n"
            tech_content += f"How you used it: {details['how_you_used_it']}\n"
            tech_content += f"Business value: {details['business_value']}\n"
            tech_content += f"Interview talking point: {details['interview_talking_point']}\n\n"
        
        self.tech_text.insert(1.0, tech_content)
        
        # Populate interview prep
        interview_content = "INTERVIEW PREPARATION\n" + "="*30 + "\n\n"
        for i, qa in enumerate(report['interview_preparation'], 1):
            interview_content += f"QUESTION {i}:\n"
            interview_content += f"❓ {qa['question']}\n\n"
            interview_content += f"YOUR ANSWER:\n"
            interview_content += f"✅ {qa['your_answer']}\n\n"
            interview_content += f"TECHNICAL DETAILS:\n"
            interview_content += f"🔧 {qa['technical_details']}\n\n"
            interview_content += "-" * 60 + "\n\n"
        
        self.interview_text.insert(1.0, interview_content)
        
        # Populate learning path
        learning_content = "YOUR NEXT LEARNING STEPS\n" + "="*35 + "\n\n"
        for i, step in enumerate(report['next_learning_steps'], 1):
            learning_content += f"{i}. {step['topic']}\n"
            learning_content += f"   Description: {step['description']}\n"
            learning_content += f"   Why useful: {step['why_useful']}\n"
            learning_content += f"   Next project: {step['next_project']}\n\n"
        
        self.learning_text.insert(1.0, learning_content)
        
        # Enable save button
        self.save_btn.config(state='normal')
        
        messagebox.showinfo("Analysis Complete", 
                           f"Analyzed {len(analysis['files_analyzed'])} files and identified "
                           f"{len(analysis['concepts_identified'])} programming concepts!")
    
    def save_report(self):
        """Save learning report to file"""
        if not self.current_analysis:
            return
        
        try:
            # Create learning reports folder
            reports_folder = Path("Learning_Reports")
            reports_folder.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save comprehensive report
            report_file = reports_folder / f"learning_analysis_{timestamp}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                report = self.current_analysis['report']
                
                f.write("TREY'S TECHNICAL LEARNING ANALYSIS\n")
                f.write("="*50 + "\n\n")
                
                f.write(report['summary'] + "\n\n")
                f.write("="*50 + "\n\n")
                
                f.write("CONCEPTS MASTERED:\n")
                f.write("-"*20 + "\n")
                for concept, details in report['concepts_learned'].items():
                    f.write(f"\n{concept.replace('_', ' ').title()}:\n")
                    f.write(f"- {details['definition']}\n")
                    f.write(f"- Your usage: {details['your_usage']}\n")
                
                f.write("\n" + "="*50 + "\n\n")
                f.write("TECHNOLOGIES LEARNED:\n")
                f.write("-"*20 + "\n")
                for tech, details in report['technologies_mastered'].items():
                    f.write(f"\n{tech.upper()}:\n")
                    f.write(f"- {details['what_it_is']}\n")
                    f.write(f"- Business value: {details['business_value']}\n")
                
                f.write("\n" + "="*50 + "\n\n")
                f.write("INTERVIEW PREPARATION:\n")
                f.write("-"*20 + "\n")
                for qa in report['interview_preparation']:
                    f.write(f"\nQ: {qa['question']}\n")
                    f.write(f"A: {qa['your_answer']}\n")
            
            messagebox.showinfo("Report Saved", f"Learning report saved to:\n{report_file}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save report: {e}")
    
    def export_for_resume(self):
        """Export skills summary for resume"""
        if not self.current_analysis:
            return
        
        try:
            skills_summary = "TECHNICAL SKILLS SUMMARY\n"
            skills_summary += "Based on actual project implementations:\n\n"
            
            analysis = self.current_analysis['analysis']
            
            skills_summary += "PROGRAMMING LANGUAGES:\n"
            skills_summary += "• Python (GUI development, API integration, web scraping)\n\n"
            
            skills_summary += "FRAMEWORKS & LIBRARIES:\n"
            for tech in sorted(analysis['imports_used']):
                if tech in ['tkinter', 'requests', 'bs4', 'threading', 'json']:
                    skills_summary += f"• {tech} - "
                    if tech == 'tkinter':
                        skills_summary += "Desktop GUI development\n"
                    elif tech == 'requests':
                        skills_summary += "HTTP API integration\n"
                    elif tech == 'bs4':
                        skills_summary += "Web scraping and HTML parsing\n"
                    elif tech == 'threading':
                        skills_summary += "Concurrent programming\n"
                    elif tech == 'json':
                        skills_summary += "Data serialization and API communication\n"
            
            skills_summary += "\nCORE COMPETENCIES:\n"
            for concept in analysis['concepts_identified']:
                concept_name = concept.replace('_', ' ').title()
                skills_summary += f"• {concept_name}\n"
            
            skills_summary += f"\nPROJECTS COMPLETED:\n"
            skills_summary += "• Job Application Automation Suite\n"
            skills_summary += "• GitHub Development Activity Logger\n"
            skills_summary += "• Learning Assistant & Code Analyzer\n"
            skills_summary += "• Multiple GUI and CLI interfaces\n"
            
            # Save to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(skills_summary)
            
            messagebox.showinfo("Skills Exported", 
                              "Technical skills summary copied to clipboard!\nPaste into your resume.")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export skills: {e}")

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Configure ttk styles
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    app = LearningAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()