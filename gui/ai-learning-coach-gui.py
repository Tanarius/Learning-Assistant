#!/usr/bin/env python3
"""
AI Learning Coach GUI - Professional Interface
==============================================

Advanced GUI for the AI-powered learning coach that integrates with job data
from AI Job Hunt Commander to identify skill gaps and create personalized
learning paths.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font
import threading
import sys
import json
from pathlib import Path
from datetime import datetime
import webbrowser

# Add the src path for our AI Learning Coach
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from ai_learning_coach import AILearningCoach
    print("✅ AI Learning Coach imported successfully")
except ImportError as e:
    print(f"❌ Error importing AI Learning Coach: {e}")
    messagebox.showerror("Import Error", f"Could not import AI Learning Coach: {e}")
    sys.exit(1)

class AILearningCoachGUI:
    """Professional GUI for AI Learning Coach with job integration"""
    
    def __init__(self, root):
        self.root = root
        self.coach = AILearningCoach()
        self.current_analysis = None
        self.processing = False
        
        self.setup_window()
        self.setup_styles()
        self.create_interface()
        
        # Display initialization status
        self.add_status_message("🎓 AI Learning Coach initialized")
        if self.coach.ai_enabled:
            self.add_status_message("🤖 AI-POWERED MODE: OpenAI integration active")
        else:
            self.add_status_message("📋 TEMPLATE MODE: Add OpenAI API key for AI recommendations")
    
    def setup_window(self):
        """Configure main window with professional styling"""
        self.root.title("AI Learning Coach - Intelligent Skill Development")
        self.root.geometry("1400x1000")
        self.root.resizable(True, True)
        self.root.configure(bg='#f5f5f5')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (1000 // 2)
        self.root.geometry(f"1400x1000+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(1200, 800)
    
    def setup_styles(self):
        """Setup professional styling matching AI Commander"""
        self.style = ttk.Style()
        
        # Use modern theme
        try:
            self.style.theme_use('vista')
        except:
            try:
                self.style.theme_use('clam')
            except:
                pass
        
        # Configure custom styles
        self.style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 12))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Primary.TButton', font=('Arial', 11, 'bold'))
        self.style.configure('Success.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Warning.TButton', font=('Arial', 10))
    
    def create_interface(self):
        """Create the complete professional interface"""
        # Main container
        main_container = tk.Frame(self.root, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create header
        self.create_header(main_container)
        
        # Create main content area
        content_frame = tk.Frame(main_container, bg='#f5f5f5')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Left panel - Controls and status
        left_panel = tk.Frame(content_frame, bg='#f5f5f5', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        self.create_controls_panel(left_panel)
        
        # Right panel - Results
        right_panel = tk.Frame(content_frame, bg='#f5f5f5')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_results_panel(right_panel)
    
    def create_header(self, parent):
        """Create professional header section"""
        header_frame = tk.Frame(parent, bg='#f5f5f5')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Main title with icon
        title_frame = tk.Frame(header_frame, bg='#f5f5f5')
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame,
                              text="🎓 AI Learning Coach",
                              font=('Arial', 22, 'bold'),
                              bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.mode_indicator = tk.Label(title_frame,
                                      text="🤖 AI Mode" if self.coach.ai_enabled else "📋 Template Mode",
                                      font=('Arial', 10, 'bold'),
                                      bg='#f5f5f5', 
                                      fg='#27ae60' if self.coach.ai_enabled else '#f39c12')
        self.mode_indicator.pack(side=tk.RIGHT)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Intelligent Skill Gap Analysis • Job Integration • Personalized Learning Paths",
                                 font=('Arial', 12),
                                 bg='#f5f5f5', fg='#7f8c8d')
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Integration status
        jobs_count = len(self.coach.scan_ai_commander_jobs())
        integration_text = f"🔗 Found {jobs_count} job applications for analysis" if jobs_count > 0 else "⚠️ No job applications found - Generate some with AI Job Hunt Commander"
        integration_color = '#27ae60' if jobs_count > 0 else '#e74c3c'
        
        integration_label = tk.Label(header_frame,
                                    text=integration_text,
                                    font=('Arial', 10, 'bold'),
                                    bg='#f5f5f5', fg=integration_color)
        integration_label.pack(anchor=tk.W, pady=(5, 0))
    
    def create_controls_panel(self, parent):
        """Create the controls and configuration panel"""
        # Analysis Section
        analysis_frame = tk.LabelFrame(parent, text="🔍 Skill Gap Analysis", 
                                     font=('Arial', 12, 'bold'), padx=15, pady=15)
        analysis_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Directory selection
        dir_frame = tk.Frame(analysis_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(dir_frame, text="Codebase to analyze:",
                font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        dir_selection_frame = tk.Frame(dir_frame)
        dir_selection_frame.pack(fill=tk.X)
        
        self.directory_var = tk.StringVar(value="Current Directory")
        self.directory_label = tk.Label(dir_selection_frame, textvariable=self.directory_var,
                                       font=('Arial', 9), fg='#7f8c8d',
                                       relief='sunken', bd=1, padx=10, pady=5)
        self.directory_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(dir_selection_frame, text="📁 Browse",
                              command=self.browse_directory,
                              font=('Arial', 9),
                              bg='#95a5a6', fg='white',
                              activebackground='#7f8c8d',
                              relief='flat', bd=0, padx=12, pady=8,
                              cursor='hand2')
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Main action buttons
        buttons_frame = tk.Frame(analysis_frame)
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Analyze button
        self.analyze_btn = tk.Button(buttons_frame,
                                    text="🚀 Analyze Skills vs Jobs",
                                    command=self.start_analysis,
                                    font=('Arial', 12, 'bold'),
                                    bg='#3498db', fg='white',
                                    activebackground='#2980b9',
                                    relief='flat', bd=0, padx=20, pady=12,
                                    cursor='hand2')
        self.analyze_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Quick actions
        quick_frame = tk.Frame(buttons_frame)
        quick_frame.pack(fill=tk.X)
        
        refresh_btn = tk.Button(quick_frame, text="🔄 Refresh Jobs",
                               command=self.refresh_job_data,
                               font=('Arial', 10),
                               bg='#f39c12', fg='white',
                               activebackground='#e67e22',
                               relief='flat', bd=0, padx=15, pady=8,
                               cursor='hand2')
        refresh_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        help_btn = tk.Button(quick_frame, text="❓ Help",
                            command=self.show_help,
                            font=('Arial', 10),
                            bg='#95a5a6', fg='white',
                            activebackground='#7f8c8d',
                            relief='flat', bd=0, padx=15, pady=8,
                            cursor='hand2')
        help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Progress Section
        progress_frame = tk.LabelFrame(parent, text="📊 Analysis Progress",
                                     font=('Arial', 12, 'bold'), padx=15, pady=15)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(progress_frame,
                                                   height=6,
                                                   font=('Consolas', 9),
                                                   wrap=tk.WORD,
                                                   bg='#2c3e50', fg='#ecf0f1')
        self.status_text.pack(fill=tk.X)
        
        # Quick Stats Section
        stats_frame = tk.LabelFrame(parent, text="📈 Quick Stats",
                                   font=('Arial', 12, 'bold'), padx=15, pady=15)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.stats_label = tk.Label(stats_frame,
                                   text="Run analysis to see your skill development stats",
                                   font=('Arial', 10), fg='#7f8c8d',
                                   justify=tk.LEFT)
        self.stats_label.pack(anchor=tk.W)
        
        # Action Buttons
        actions_frame = tk.LabelFrame(parent, text="⚡ Actions",
                                    font=('Arial', 12, 'bold'), padx=15, pady=15)
        actions_frame.pack(fill=tk.X)
        
        # Export buttons
        self.export_btn = tk.Button(actions_frame, text="📄 Export Analysis",
                                   command=self.export_analysis,
                                   font=('Arial', 10),
                                   bg='#27ae60', fg='white',
                                   activebackground='#229954',
                                   relief='flat', bd=0, padx=15, pady=8,
                                   cursor='hand2', state='disabled')
        self.export_btn.pack(fill=tk.X, pady=(0, 8))
        
        self.learning_plan_btn = tk.Button(actions_frame, text="🎯 Create Learning Plan",
                                          command=self.create_learning_plan,
                                          font=('Arial', 10),
                                          bg='#8e44ad', fg='white',
                                          activebackground='#7d3c98',
                                          relief='flat', bd=0, padx=15, pady=8,
                                          cursor='hand2', state='disabled')
        self.learning_plan_btn.pack(fill=tk.X)
    
    def create_results_panel(self, parent):
        """Create the results display panel with tabs"""
        # Results header
        results_header = tk.Frame(parent, bg='#f5f5f5')
        results_header.pack(fill=tk.X, pady=(0, 15))
        
        results_title = tk.Label(results_header,
                                text="📋 Analysis Results",
                                font=('Arial', 16, 'bold'),
                                bg='#f5f5f5', fg='#2c3e50')
        results_title.pack(anchor=tk.W)
        
        # Create notebook for tabbed results
        self.results_notebook = ttk.Notebook(parent)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Skill Gaps
        self.create_skill_gaps_tab()
        
        # Tab 2: Learning Paths
        self.create_learning_paths_tab()
        
        # Tab 3: AI Recommendations
        self.create_ai_recommendations_tab()
        
        # Tab 4: Job Analysis
        self.create_job_analysis_tab()
        
        # Tab 5: Progress Tracking
        self.create_progress_tracking_tab()
    
    def create_skill_gaps_tab(self):
        """Create skill gaps analysis tab"""
        skill_gaps_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(skill_gaps_frame, text="🎯 Skill Gaps")
        
        # Header
        header_frame = tk.Frame(skill_gaps_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(header_frame, text="🔍 Skills You Need to Learn",
                font=('Arial', 14, 'bold')).pack(anchor=tk.W)
        
        tk.Label(header_frame,
                text="Based on job applications generated by AI Job Hunt Commander",
                font=('Arial', 10), fg='#7f8c8d').pack(anchor=tk.W, pady=(5, 0))
        
        # Skill gaps display
        self.skill_gaps_text = scrolledtext.ScrolledText(skill_gaps_frame,
                                                        font=('Arial', 11),
                                                        wrap=tk.WORD,
                                                        bg='white',
                                                        relief='solid', bd=1)
        self.skill_gaps_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_learning_paths_tab(self):
        """Create learning paths tab"""
        learning_paths_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(learning_paths_frame, text="🛤️ Learning Paths")
        
        # Header
        header_frame = tk.Frame(learning_paths_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(header_frame, text="📚 Structured Learning Paths",
                font=('Arial', 14, 'bold')).pack(anchor=tk.W)
        
        tk.Label(header_frame,
                text="Step-by-step paths to master the skills you need",
                font=('Arial', 10), fg='#7f8c8d').pack(anchor=tk.W, pady=(5, 0))
        
        # Learning paths display
        self.learning_paths_text = scrolledtext.ScrolledText(learning_paths_frame,
                                                           font=('Arial', 11),
                                                           wrap=tk.WORD,
                                                           bg='white',
                                                           relief='solid', bd=1)
        self.learning_paths_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_ai_recommendations_tab(self):
        """Create AI recommendations tab"""
        ai_rec_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(ai_rec_frame, text="🤖 AI Recommendations")
        
        # Header
        header_frame = tk.Frame(ai_rec_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(header_frame, text="🧠 Personalized AI Learning Advice",
                font=('Arial', 14, 'bold')).pack(anchor=tk.W)
        
        self.ai_mode_label = tk.Label(header_frame,
                                     text="",
                                     font=('Arial', 10), fg='#7f8c8d')
        self.ai_mode_label.pack(anchor=tk.W, pady=(5, 0))
        
        # AI recommendations display
        self.ai_recommendations_text = scrolledtext.ScrolledText(ai_rec_frame,
                                                               font=('Arial', 11),
                                                               wrap=tk.WORD,
                                                               bg='white',
                                                               relief='solid', bd=1)
        self.ai_recommendations_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_job_analysis_tab(self):
        """Create job analysis tab"""
        job_analysis_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(job_analysis_frame, text="💼 Job Analysis")
        
        # Header
        header_frame = tk.Frame(job_analysis_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(header_frame, text="📊 Job Requirements vs Your Skills",
                font=('Arial', 14, 'bold')).pack(anchor=tk.W)
        
        tk.Label(header_frame,
                text="Individual analysis of each job application",
                font=('Arial', 10), fg='#7f8c8d').pack(anchor=tk.W, pady=(5, 0))
        
        # Job analysis display
        self.job_analysis_text = scrolledtext.ScrolledText(job_analysis_frame,
                                                         font=('Arial', 11),
                                                         wrap=tk.WORD,
                                                         bg='white',
                                                         relief='solid', bd=1)
        self.job_analysis_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_progress_tracking_tab(self):
        """Create progress tracking tab"""
        progress_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(progress_frame, text="📈 Progress Tracking")
        
        # Header
        header_frame = tk.Frame(progress_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(header_frame, text="🎯 Your Learning Progress",
                font=('Arial', 14, 'bold')).pack(anchor=tk.W)
        
        tk.Label(header_frame,
                text="Track your skill development over time",
                font=('Arial', 10), fg='#7f8c8d').pack(anchor=tk.W, pady=(5, 0))
        
        # Progress display
        self.progress_tracking_text = scrolledtext.ScrolledText(progress_frame,
                                                              font=('Arial', 11),
                                                              wrap=tk.WORD,
                                                              bg='white',
                                                              relief='solid', bd=1)
        self.progress_tracking_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def browse_directory(self):
        """Let user select directory to analyze"""
        directory = filedialog.askdirectory(
            title="Select codebase directory to analyze",
            initialdir=str(Path.cwd())
        )
        if directory:
            self.current_directory = directory
            dir_name = Path(directory).name
            self.directory_var.set(f"{dir_name} ({len(list(Path(directory).glob('**/*.py')))} Python files)")
    
    def add_status_message(self, message):
        """Add message to status console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.status_text.insert(tk.END, formatted_message)
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def refresh_job_data(self):
        """Refresh job data from AI Commander"""
        jobs_count = len(self.coach.scan_ai_commander_jobs())
        if jobs_count > 0:
            self.add_status_message(f"🔄 Found {jobs_count} job applications for analysis")
            messagebox.showinfo("Job Data Refreshed", 
                              f"Found {jobs_count} job applications from AI Job Hunt Commander")
        else:
            self.add_status_message("⚠️ No job applications found")
            messagebox.showwarning("No Job Data", 
                                 "No job applications found. Generate some applications with AI Job Hunt Commander first.")
    
    def start_analysis(self):
        """Start the complete skill gap analysis"""
        if self.processing:
            return
        
        # Check for job data
        jobs_count = len(self.coach.scan_ai_commander_jobs())
        if jobs_count == 0:
            messagebox.showwarning("No Job Data",
                                 "No job applications found to analyze.\n\n"
                                 "Please use AI Job Hunt Commander to generate some job applications first, "
                                 "then run this analysis to identify skill gaps.")
            return
        
        self.processing = True
        self.analyze_btn.config(state='disabled', text="🔄 Analyzing...")
        self.progress.start()
        
        # Get directory
        directory = getattr(self, 'current_directory', '.')
        
        # Run in background thread
        analysis_thread = threading.Thread(
            target=self.perform_analysis,
            args=(directory,)
        )
        analysis_thread.daemon = True
        analysis_thread.start()
    
    def perform_analysis(self, directory):
        """Perform analysis in background thread"""
        try:
            self.root.after(0, lambda: self.add_status_message("🚀 Starting AI Learning Coach analysis..."))
            
            # Run complete analysis
            analysis = self.coach.analyze_job_skill_requirements(directory)
            
            if "error" in analysis:
                self.root.after(0, lambda: self.handle_analysis_error(analysis["error"]))
                return
            
            # Update GUI with results
            self.root.after(0, lambda: self.display_analysis_results(analysis))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.handle_analysis_error(error_msg))
    
    def display_analysis_results(self, analysis):
        """Display complete analysis results in GUI"""
        self.current_analysis = analysis
        
        # Stop progress
        self.progress.stop()
        self.analyze_btn.config(state='normal', text="🚀 Analyze Skills vs Jobs")
        self.processing = False
        
        # Enable action buttons
        self.export_btn.config(state='normal')
        self.learning_plan_btn.config(state='normal')
        
        # Update status
        jobs_count = analysis['jobs_analyzed_count']
        gaps_count = len(analysis['prioritized_skill_gaps'])
        readiness = analysis['overall_readiness']['status']
        
        self.add_status_message(f"✅ Analysis complete! {gaps_count} skill gaps identified from {jobs_count} jobs")
        self.add_status_message(f"📊 Overall readiness: {readiness}")
        
        # Update quick stats
        stats_text = f"""📊 Analysis Summary:
• Jobs Analyzed: {jobs_count}
• Skill Gaps Found: {gaps_count}
• Current Skills: {len(analysis['current_skills'])}
• Overall Readiness: {analysis['overall_readiness']['overall_score']:.1f}%
• Status: {readiness}"""
        self.stats_label.config(text=stats_text, justify=tk.LEFT)
        
        # Populate each tab
        self.populate_skill_gaps_tab(analysis)
        self.populate_learning_paths_tab(analysis)
        self.populate_ai_recommendations_tab(analysis)
        self.populate_job_analysis_tab(analysis)
        self.populate_progress_tracking_tab(analysis)
        
        # Switch to skill gaps tab
        self.results_notebook.select(0)
        
        # Show completion message
        messagebox.showinfo("Analysis Complete",
                           f"AI Learning Coach analysis completed!\n\n"
                           f"📊 Analyzed {jobs_count} job applications\n"
                           f"🎯 Identified {gaps_count} skill gaps\n"
                           f"📈 Overall readiness: {readiness}")
    
    def populate_skill_gaps_tab(self, analysis):
        """Populate the skill gaps tab with analysis results"""
        self.skill_gaps_text.delete(1.0, tk.END)
        
        content = "🎯 SKILL GAPS ANALYSIS\n"
        content += "=" * 60 + "\n\n"
        
        content += f"Based on analysis of {analysis['jobs_analyzed_count']} job applications:\n"
        for job in analysis['jobs_analyzed']:
            content += f"• {job['title']} at {job['company']} (Match: {job.get('application_score', 0):.1f}/10)\n"
        content += "\n"
        
        if not analysis['prioritized_skill_gaps']:
            content += "🎉 EXCELLENT! No critical skill gaps identified.\n"
            content += "You appear to have the skills needed for the jobs you're targeting.\n"
            content += "Focus on interview preparation and portfolio presentation."
        else:
            content += f"🔍 TOP {min(len(analysis['prioritized_skill_gaps']), 10)} SKILLS TO LEARN:\n\n"
            
            for i, gap in enumerate(analysis['prioritized_skill_gaps'][:10], 1):
                priority_stars = "⭐" * gap['learning_priority']
                urgency = "🔥 HIGH PRIORITY" if gap['learning_priority'] >= 4 else "📝 MODERATE" if gap['learning_priority'] >= 2 else "💡 LOW PRIORITY"
                
                content += f"{i}. {gap['skill_name'].replace('_', ' ').title()}\n"
                content += f"   Priority: {priority_stars} ({gap['learning_priority']}/5) - {urgency}\n"
                content += f"   Current Level: {gap['current_level'].title()}\n"
                content += f"   Target Level: {gap['required_level'].title()}\n"
                content += f"   Found in: {gap['job_frequency']} job(s)\n"
                content += f"   Learning Time: {gap['time_estimate']}\n"
                content += f"   Gap Severity: {gap['gap_severity']:.1f}/10\n\n"
        
        content += "\n" + "=" * 60 + "\n"
        content += "💡 READINESS ASSESSMENT:\n\n"
        
        readiness = analysis['overall_readiness']
        content += f"Overall Match Score: {readiness['overall_score']:.1f}%\n"
        content += f"Status: {readiness['status']}\n"
        content += f"Best Job Match: {readiness['best_match_score']:.1f}%\n"
        content += f"Most Challenging Job: {readiness['worst_match_score']:.1f}%\n\n"
        
        content += "📋 RECOMMENDATIONS:\n"
        for rec in readiness['recommendations']:
            content += f"• {rec}\n"
        
        self.skill_gaps_text.insert(1.0, content)
    
    def populate_learning_paths_tab(self, analysis):
        """Populate learning paths tab"""
        self.learning_paths_text.delete(1.0, tk.END)
        
        content = "🛤️ STRUCTURED LEARNING PATHS\n"
        content += "=" * 60 + "\n\n"
        
        if not analysis['learning_paths']:
            content += "🎉 Great! No specific learning paths needed.\n"
            content += "You already have the core skills for your target roles.\n"
            content += "Focus on polishing existing skills and interview prep."
        else:
            content += f"📚 {len(analysis['learning_paths'])} LEARNING PATH(S) CREATED:\n\n"
            
            for i, path in enumerate(analysis['learning_paths'], 1):
                content += f"{i}. {path['skill_area']}\n"
                content += f"   Current: {path['current_level'].title()} → Target: {path['target_level'].title()}\n"
                content += f"   Estimated Time: {path['total_time_estimate']}\n\n"
                
                content += "   📋 LEARNING STEPS:\n"
                for j, step in enumerate(path['steps'][:5], 1):  # Show top 5 steps
                    content += f"   {j}. {step['step']}\n"
                    content += f"      Duration: {step['duration']}\n"
                    content += f"      Deliverable: {step['deliverable']}\n\n"
                
                content += "   🎯 KEY PROJECTS:\n"
                for project in path['projects'][:3]:  # Show top 3 projects
                    content += f"   • {project}\n"
                content += "\n"
                
                content += "   🏆 MILESTONES:\n"
                for milestone in path['milestones'][:4]:  # Show top 4 milestones
                    content += f"   ✓ {milestone}\n"
                content += "\n"
                
                content += "   📊 SUCCESS METRICS:\n"
                for metric in path['success_metrics'][:3]:  # Show top 3 metrics
                    content += f"   • {metric}\n"
                content += "\n" + "-" * 50 + "\n\n"
        
        content += "\n💡 INTEGRATION TIPS:\n\n"
        content += "• Start with the highest priority skill group\n"
        content += "• Dedicate 1-2 hours daily to focused learning\n"
        content += "• Build portfolio projects that showcase multiple skills\n"
        content += "• Document your learning journey for personal branding\n"
        content += "• Apply new skills to existing projects (Memory Platform, automation bots)\n"
        content += "• Set weekly goals and track progress\n"
        
        self.learning_paths_text.insert(1.0, content)
    
    def populate_ai_recommendations_tab(self, analysis):
        """Populate AI recommendations tab"""
        self.ai_recommendations_text.delete(1.0, tk.END)
        
        ai_rec = analysis['ai_recommendations']
        
        if ai_rec['ai_generated']:
            self.ai_mode_label.config(text="🤖 Generated by OpenAI GPT-3.5-turbo", fg='#27ae60')
            content = "🤖 AI-POWERED LEARNING RECOMMENDATIONS\n"
            content += "=" * 60 + "\n\n"
            content += ai_rec['content']
            content += "\n\n" + "=" * 60 + "\n"
            content += f"Generated: {ai_rec['generated_at']}\n"
            content += f"Model: {ai_rec['model_used']}\n"
        else:
            self.ai_mode_label.config(text="📋 Template-based recommendations (Enable OpenAI for AI-powered advice)", fg='#f39c12')
            content = "📋 TEMPLATE-BASED LEARNING RECOMMENDATIONS\n"
            content += "=" * 60 + "\n\n"
            
            if 'recommendations' in ai_rec:
                for rec in ai_rec['recommendations']:
                    content += f"🎯 {rec['skill'].replace('_', ' ').title()}\n"
                    content += f"   Estimated Learning Time: {rec['time_estimate']}\n\n"
                    
                    content += "   📚 LEARNING RESOURCES:\n"
                    for resource in rec['resources']:
                        content += f"   • {resource}\n"
                    content += "\n"
                    
                    content += "   🔧 PROJECT IDEAS:\n"
                    for project in rec['projects']:
                        content += f"   • {project}\n"
                    content += "\n"
                    
                    content += "   ⚡ QUICK WINS:\n"
                    for win in rec['quick_wins']:
                        content += f"   • {win}\n"
                    content += "\n" + "-" * 50 + "\n\n"
            
            content += "\n💡 To get personalized AI recommendations:\n"
            content += "1. Add your OpenAI API key to the .env file\n"
            content += "2. Restart the AI Learning Coach\n"
            content += "3. Re-run the analysis for intelligent, customized advice\n"
        
        self.ai_recommendations_text.insert(1.0, content)
    
    def populate_job_analysis_tab(self, analysis):
        """Populate job analysis tab"""
        self.job_analysis_text.delete(1.0, tk.END)
        
        content = "💼 INDIVIDUAL JOB ANALYSIS\n"
        content += "=" * 60 + "\n\n"
        
        if not analysis['job_analyses']:
            content += "No job analyses available."
        else:
            for i, job_analysis in enumerate(analysis['job_analyses'], 1):
                content += f"{i}. {job_analysis['job_title']} at {job_analysis['company']}\n"
                content += f"   Overall Match Score: {job_analysis['overall_match_score']:.1f}%\n"
                content += f"   Readiness Timeline: {job_analysis['readiness_timeline']}\n\n"
                
                content += "   📋 REQUIRED SKILLS:\n"
                for skill in job_analysis['required_skills'][:8]:  # Show top 8
                    content += f"   • {skill.replace('_', ' ').title()}\n"
                content += "\n"
                
                if job_analysis['missing_skills']:
                    content += "   ❌ MISSING SKILLS:\n"
                    for skill in job_analysis['missing_skills'][:5]:  # Show top 5
                        content += f"   • {skill.replace('_', ' ').title()}\n"
                    content += "\n"
                
                if job_analysis['skill_gaps']:
                    content += "   🎯 SKILL GAPS TO ADDRESS:\n"
                    for gap in job_analysis['skill_gaps'][:3]:  # Show top 3
                        content += f"   • {gap['skill_name'].replace('_', ' ').title()}: {gap['current_level']} → {gap['required_level']} (Priority: {gap['learning_priority']}/5)\n"
                    content += "\n"
                
                content += "-" * 50 + "\n\n"
        
        content += "\n💡 APPLICATION STRATEGY:\n\n"
        content += "• Focus on jobs with 70%+ match scores for best success odds\n"
        content += "• For lower-scoring jobs, prioritize learning the most common missing skills\n"
        content += "• Use this analysis to tailor your resume and cover letters\n"
        content += "• Highlight skills you already have that match job requirements\n"
        
        self.job_analysis_text.insert(1.0, content)
    
    def populate_progress_tracking_tab(self, analysis):
        """Populate progress tracking tab"""
        self.progress_tracking_text.delete(1.0, tk.END)
        
        content = "📈 PROGRESS TRACKING & NEXT ACTIONS\n"
        content += "=" * 60 + "\n\n"
        
        # Current skills
        content += "✅ CURRENT SKILLS INVENTORY:\n\n"
        skill_categories = {
            "Infrastructure & Systems": ["infrastructure", "windows_server", "active_directory", "linux", "networking"],
            "Programming & Development": ["python", "automation", "api_integration", "python_gui"],
            "Data & Analysis": ["data_processing", "data_analysis", "scientific_computing"],
            "Web & APIs": ["web_scraping", "api_development", "web_development"],
            "Emerging Skills": ["machine_learning", "cloud_computing", "devops"]
        }
        
        for category, skills in skill_categories.items():
            category_skills = []
            for skill in skills:
                if skill in analysis['current_skills']:
                    level = analysis['current_skills'][skill]
                    category_skills.append(f"{skill.replace('_', ' ').title()}: {level.title()}")
            
            if category_skills:
                content += f"   {category}:\n"
                for skill in category_skills:
                    content += f"   • {skill}\n"
                content += "\n"
        
        # Next actions
        content += "\n🎯 IMMEDIATE NEXT ACTIONS:\n\n"
        for action in analysis['next_actions']:
            content += f"{action}\n"
        
        content += "\n\n📊 TRACKING RECOMMENDATIONS:\n\n"
        content += "• Re-run this analysis weekly to track skill development\n"
        content += "• Update your knowledge base as you learn new skills\n"
        content += "• Generate new job applications monthly to track market changes\n"
        content += "• Document learning milestones in your portfolio\n"
        content += "• Set SMART goals for each skill gap identified\n"
        content += "• Create a learning schedule and stick to it\n"
        content += "• Join communities related to your target skills\n"
        content += "• Practice skills through real projects, not just tutorials\n"
        
        content += "\n\n🎯 SUCCESS METRICS TO TRACK:\n\n"
        content += "• Time spent learning each week\n"
        content += "• Projects completed using new skills\n"
        content += "• Job application success rates\n"
        content += "• Interview callback rates\n"
        content += "• Portfolio project quality improvements\n"
        content += "• Community engagement (GitHub contributions, posts, etc.)\n"
        content += "• Skill assessment scores (if applicable)\n"
        content += "• Overall job market readiness percentage\n"
        
        self.progress_tracking_text.insert(1.0, content)
    
    def handle_analysis_error(self, error_msg):
        """Handle analysis errors"""
        self.progress.stop()
        self.analyze_btn.config(state='normal', text="🚀 Analyze Skills vs Jobs")
        self.processing = False
        
        self.add_status_message(f"❌ Analysis error: {error_msg}")
        messagebox.showerror("Analysis Error", 
                           f"Analysis failed: {error_msg}\n\n"
                           "Please check that:\n"
                           "• You have job applications from AI Job Hunt Commander\n"
                           "• The selected directory contains Python files\n"
                           "• You have proper file permissions")
    
    def export_analysis(self):
        """Export analysis results to file"""
        if not self.current_analysis:
            messagebox.showwarning("No Analysis", "No analysis results to export.")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"AI_Learning_Coach_Analysis_{timestamp}.txt"
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialname=filename
            )
            
            if not filepath:
                return
            
            # Create comprehensive export
            export_content = f"""AI LEARNING COACH - COMPLETE ANALYSIS REPORT
Generated: {self.current_analysis['analysis_timestamp']}
============================================================

EXECUTIVE SUMMARY:
• Jobs Analyzed: {self.current_analysis['jobs_analyzed_count']}
• Skill Gaps Identified: {len(self.current_analysis['prioritized_skill_gaps'])}
• Overall Readiness: {self.current_analysis['overall_readiness']['overall_score']:.1f}%
• Status: {self.current_analysis['overall_readiness']['status']}

JOBS ANALYZED:
"""
            for job in self.current_analysis['jobs_analyzed']:
                export_content += f"• {job['title']} at {job['company']} (Score: {job.get('application_score', 0):.1f}/10)\n"
            
            export_content += f"""
CURRENT SKILLS:
"""
            for skill, level in self.current_analysis['current_skills'].items():
                export_content += f"• {skill.replace('_', ' ').title()}: {level.title()}\n"
            
            export_content += f"""
TOP SKILL GAPS TO ADDRESS:
"""
            for i, gap in enumerate(self.current_analysis['prioritized_skill_gaps'][:10], 1):
                export_content += f"""
{i}. {gap['skill_name'].replace('_', ' ').title()}
   Current Level: {gap['current_level'].title()}
   Target Level: {gap['required_level'].title()}
   Priority: {gap['learning_priority']}/5
   Found in {gap['job_frequency']} job(s)
   Learning Time: {gap['time_estimate']}
"""
            
            export_content += f"""
AI RECOMMENDATIONS:
{self.current_analysis['ai_recommendations'].get('content', 'Template-based recommendations provided')}

NEXT ACTIONS:
"""
            for action in self.current_analysis['next_actions']:
                export_content += f"• {action}\n"
            
            export_content += f"""

LEARNING PATHS:
"""
            for path in self.current_analysis['learning_paths']:
                export_content += f"""
{path['skill_area']} ({path['total_time_estimate']}):
"""
                for step in path['steps'][:3]:
                    export_content += f"  • {step['step']} ({step['duration']})\n"
            
            export_content += f"""

Generated by AI Learning Coach - Infrastructure → AI Career Transition Toolkit
Portfolio: https://tanarius.github.io
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(export_content)
            
            messagebox.showinfo("Export Complete", 
                              f"Analysis exported successfully to:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export analysis: {e}")
    
    def create_learning_plan(self):
        """Create and export a focused learning plan"""
        if not self.current_analysis:
            messagebox.showwarning("No Analysis", "No analysis results available.")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Learning_Plan_{timestamp}.md"
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".md",
                filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")],
                initialname=filename
            )
            
            if not filepath:
                return
            
            # Create actionable learning plan
            plan_content = f"""# 🎓 AI Learning Coach - Personal Development Plan

**Generated:** {datetime.now().strftime('%B %d, %Y')}  
**Career Goal:** Infrastructure Engineer → AI/Automation Specialist  
**Timeline:** 30-day job search sprint  

## 📊 Current Status

- **Overall Readiness:** {self.current_analysis['overall_readiness']['overall_score']:.1f}%
- **Status:** {self.current_analysis['overall_readiness']['status']}
- **Jobs Analyzed:** {self.current_analysis['jobs_analyzed_count']}
- **Skill Gaps:** {len(self.current_analysis['prioritized_skill_gaps'])}

## 🎯 Top 5 Priority Skills

"""
            for i, gap in enumerate(self.current_analysis['prioritized_skill_gaps'][:5], 1):
                plan_content += f"""### {i}. {gap['skill_name'].replace('_', ' ').title()}

- **Current Level:** {gap['current_level'].title()}
- **Target Level:** {gap['required_level'].title()}  
- **Priority:** {gap['learning_priority']}/5 ({'🔥 HIGH' if gap['learning_priority'] >= 4 else '📝 MEDIUM' if gap['learning_priority'] >= 2 else '💡 LOW'})
- **Learning Time:** {gap['time_estimate']}
- **Found in:** {gap['job_frequency']} job posting(s)

**Learning Actions:**
- [ ] Complete foundational tutorial/course
- [ ] Build practice project
- [ ] Integrate into existing automation projects
- [ ] Create portfolio demonstration
- [ ] Document learning journey

"""
            
            plan_content += f"""## 📅 Weekly Learning Schedule

### Week 1-2: Foundation Building
- Focus on highest priority skill: **{self.current_analysis['prioritized_skill_gaps'][0]['skill_name'].replace('_', ' ').title()}**
- Daily commitment: 1-2 hours
- Goal: Complete basic tutorial and build first project

### Week 3-4: Integration & Practice  
- Integrate new skills into Memory Platform or automation bots
- Start second priority skill
- Document progress for portfolio

### Week 5-8: Advanced Application
- Build comprehensive projects showcasing multiple skills
- Continue with remaining priority skills
- Prepare for job applications

## 🔗 Integration Opportunities

**Memory Platform Enhancements:**
- Add new skills to enhance AI capabilities
- Document technical decisions and learning process
- Use as portfolio showcase project

**Automation Bot Improvements:**
- Integrate new technologies into existing bots
- Add advanced features demonstrating new skills
- Create new bots showcasing specific skills

## 📈 Progress Tracking

**Weekly Check-ins:**
- [ ] Hours spent learning
- [ ] Skills practiced
- [ ] Projects completed
- [ ] Portfolio updates made

**Monthly Assessment:**
- [ ] Re-run AI Learning Coach analysis
- [ ] Update resume with new skills
- [ ] Generate new job applications to test market readiness
- [ ] Adjust learning plan based on results

## 🎯 Success Metrics

- **Technical:** Demonstrate proficiency through working projects
- **Professional:** Update LinkedIn and resume with new skills
- **Practical:** Apply skills to real automation challenges
- **Career:** Improve job application success rates

## 💡 Learning Resources

**Primary Focus Areas:**
"""
            
            # Add specific resources based on top skills
            top_skills = [gap['skill_name'] for gap in self.current_analysis['prioritized_skill_gaps'][:5]]
            
            resource_mapping = {
                'machine_learning': '- [Andrew Ng\'s ML Course](https://coursera.org/learn/machine-learning)\n- [Hands-On Machine Learning Book](https://github.com/ageron/handson-ml2)\n- [Scikit-learn Documentation](https://scikit-learn.org/)',
                'python': '- [Python Crash Course Book](https://nostarch.com/pythoncrashcourse2e)\n- [Automate the Boring Stuff](https://automatetheboringstuff.com/)\n- [Real Python Tutorials](https://realpython.com/)',
                'aws': '- [AWS Cloud Practitioner](https://aws.amazon.com/certification/certified-cloud-practitioner/)\n- [A Cloud Guru Courses](https://acloudguru.com/)\n- [AWS Free Tier Practice](https://aws.amazon.com/free/)',
                'docker': '- [Docker Official Tutorial](https://docs.docker.com/get-started/)\n- [Docker Mastery Course](https://www.udemy.com/course/docker-mastery/)\n- [Play with Docker](https://labs.play-with-docker.com/)'
            }
            
            for skill in top_skills:
                if skill in resource_mapping:
                    plan_content += f"\n**{skill.replace('_', ' ').title()}:**\n{resource_mapping[skill]}\n"
            
            plan_content += f"""

## 🚀 Next Actions (This Week)

"""
            for action in self.current_analysis['next_actions'][:8]:
                if action.startswith('•'):
                    plan_content += f"- [ ] {action[2:]}\n"
                elif action.startswith('🎯') or action.startswith('📚'):
                    plan_content += f"\n### {action}\n"
                else:
                    plan_content += f"- [ ] {action}\n"
            
            plan_content += f"""

---

**Generated by AI Learning Coach**  
**Part of Infrastructure → AI Career Transition Toolkit**  
**Portfolio:** https://tanarius.github.io
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(plan_content)
            
            messagebox.showinfo("Learning Plan Created", 
                              f"Personalized learning plan created:\n{filepath}\n\n"
                              "This plan includes:\n"
                              "• Priority skill rankings\n"
                              "• Weekly learning schedule\n" 
                              "• Progress tracking checklist\n"
                              "• Integration opportunities\n"
                              "• Specific learning resources")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not create learning plan: {e}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """🎓 AI Learning Coach - Help Guide

WHAT IT DOES:
• Analyzes job applications from AI Job Hunt Commander
• Identifies skills you need to learn for target roles  
• Creates personalized learning paths and recommendations
• Tracks your progress over time

HOW TO USE:
1. First, generate job applications with AI Job Hunt Commander
2. Select your codebase directory (optional)
3. Click "Analyze Skills vs Jobs"
4. Review results in the tabs
5. Export analysis or create learning plan

FEATURES:
🎯 Skill Gaps - Shows exactly what you need to learn
🛤️ Learning Paths - Step-by-step skill development plans
🤖 AI Recommendations - Personalized advice (with OpenAI)
💼 Job Analysis - Individual job requirement analysis  
📈 Progress Tracking - Monitor your learning journey

INTEGRATION:
• Automatically reads job data from AI Job Hunt Commander
• Analyzes your actual code to determine current skills
• Creates learning plans that integrate with your existing projects

TIPS FOR BEST RESULTS:
• Generate diverse job applications first
• Keep your codebase up to date
• Run analysis monthly to track progress
• Focus on high-priority skills first
• Document your learning journey

For more help: https://tanarius.github.io"""

        messagebox.showinfo("AI Learning Coach Help", help_text)


def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Configure ttk styles for modern appearance
    style = ttk.Style()
    try:
        style.theme_use('vista')  # Modern Windows theme
    except:
        try:
            style.theme_use('clam')  # Cross-platform modern theme
        except:
            pass  # Use default theme
    
    app = AILearningCoachGUI(root)
    
    # Handle window closing
    def on_closing():
        if app.processing:
            if messagebox.askokcancel("Processing", 
                                    "AI Learning Coach is still analyzing. Close anyway?"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()