#!/usr/bin/env python3
"""
AI Learning Coach - Advanced Technical Skill Development Engine
==============================================================

Integrates with AI Job Hunt Commander to identify skill gaps and create
personalized learning paths. Uses OpenAI to provide intelligent learning
recommendations based on job requirements vs current capabilities.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
"""

import os
import json
import openai
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re
import ast
from dataclasses import dataclass, asdict

# Set up OpenAI API
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent.parent / "applying-assistant" / ".env")
    openai.api_key = os.getenv("OPENAI_API_KEY")
except ImportError:
    openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class SkillGap:
    """Represents a skill gap identified from job requirements"""
    skill_name: str
    required_level: str  # "beginner", "intermediate", "advanced"
    current_level: str
    gap_severity: float  # 0-10, how critical this gap is
    job_frequency: int   # How often this appears in job postings
    learning_priority: int  # 1-5, priority for learning
    resources: List[str]
    time_estimate: str   # "1-2 weeks", "1-3 months", etc.

@dataclass 
class LearningPath:
    """Represents a complete learning path for skill development"""
    skill_area: str
    current_level: str
    target_level: str
    total_time_estimate: str
    steps: List[Dict[str, Any]]
    projects: List[str]
    milestones: List[str]
    success_metrics: List[str]

@dataclass
class JobSkillAnalysis:
    """Analysis of skills required for a specific job"""
    job_title: str
    company: str
    required_skills: List[str]
    preferred_skills: List[str]
    missing_skills: List[str]
    skill_gaps: List[SkillGap]
    overall_match_score: float
    readiness_timeline: str

class AILearningCoach:
    """AI-powered learning coach that creates personalized skill development plans"""
    
    def __init__(self):
        self.ai_enabled = bool(openai.api_key)
        
        # Paths for integration with other systems - Initialize first
        self.ai_commander_path = Path(__file__).parent.parent.parent / "05-AI-JOB-HUNT-COMMANDER" / "gui" / "Generated_Applications"
        self.learning_data_path = Path(__file__).parent.parent / "Learning_Data"
        self.learning_data_path.mkdir(exist_ok=True)
        
        # Load data after paths are set
        self.knowledge_base = self.load_knowledge_base()
        self.learning_history = self.load_learning_history()
        self.skill_database = self.build_skill_database()
        
        print(f"AI Learning Coach initialized - AI Mode: {'ENABLED' if self.ai_enabled else 'DISABLED'}")
    
    def load_knowledge_base(self) -> Dict[str, Any]:
        """Load existing knowledge base or create new one"""
        kb_path = Path(__file__).parent.parent / "Learning_Data" / "knowledge_base.json"
        if kb_path.exists():
            try:
                with open(kb_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "skills_learned": {},
            "concepts_mastered": {},
            "projects_completed": {},
            "learning_velocity": {},
            "areas_of_interest": [],
            "career_goals": {
                "current_role": "Infrastructure Engineer", 
                "target_role": "AI/Automation Specialist",
                "timeline": "30 days for job transition"
            }
        }
    
    def load_learning_history(self) -> List[Dict[str, Any]]:
        """Load historical learning progress"""
        history_path = self.learning_data_path / "learning_history.json"
        if history_path.exists():
            try:
                with open(history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def build_skill_database(self) -> Dict[str, Dict[str, Any]]:
        """Comprehensive skill database for analysis"""
        return {
            # Programming Languages
            "python": {
                "category": "programming_language",
                "learning_curve": "moderate", 
                "time_to_proficiency": "3-6 months",
                "prerequisites": [],
                "related_skills": ["automation", "data_analysis", "machine_learning"],
                "job_market_demand": "very_high"
            },
            "javascript": {
                "category": "programming_language",
                "learning_curve": "moderate",
                "time_to_proficiency": "2-4 months", 
                "prerequisites": ["html", "css"],
                "related_skills": ["web_development", "node_js", "react"],
                "job_market_demand": "very_high"
            },
            "sql": {
                "category": "programming_language",
                "learning_curve": "easy",
                "time_to_proficiency": "1-3 months",
                "prerequisites": [],
                "related_skills": ["database_management", "data_analysis"],
                "job_market_demand": "high"
            },
            
            # AI/ML Technologies
            "machine_learning": {
                "category": "ai_technology",
                "learning_curve": "steep",
                "time_to_proficiency": "6-12 months",
                "prerequisites": ["python", "statistics", "linear_algebra"],
                "related_skills": ["data_science", "deep_learning", "scikit_learn"],
                "job_market_demand": "very_high"
            },
            "tensorflow": {
                "category": "ai_framework",
                "learning_curve": "steep", 
                "time_to_proficiency": "4-8 months",
                "prerequisites": ["python", "machine_learning", "numpy"],
                "related_skills": ["deep_learning", "neural_networks"],
                "job_market_demand": "high"
            },
            "pytorch": {
                "category": "ai_framework",
                "learning_curve": "steep",
                "time_to_proficiency": "4-8 months", 
                "prerequisites": ["python", "machine_learning", "numpy"],
                "related_skills": ["deep_learning", "neural_networks"],
                "job_market_demand": "high"
            },
            
            # Cloud & Infrastructure
            "aws": {
                "category": "cloud_platform",
                "learning_curve": "moderate",
                "time_to_proficiency": "3-6 months",
                "prerequisites": [],
                "related_skills": ["cloud_computing", "devops", "infrastructure"],
                "job_market_demand": "very_high"
            },
            "docker": {
                "category": "devops_tool",
                "learning_curve": "moderate",
                "time_to_proficiency": "1-3 months",
                "prerequisites": ["linux"],
                "related_skills": ["kubernetes", "containerization", "devops"],
                "job_market_demand": "high"
            },
            "kubernetes": {
                "category": "devops_tool", 
                "learning_curve": "steep",
                "time_to_proficiency": "3-8 months",
                "prerequisites": ["docker", "linux", "networking"],
                "related_skills": ["container_orchestration", "devops"],
                "job_market_demand": "high"
            },
            
            # Data Technologies
            "pandas": {
                "category": "data_library",
                "learning_curve": "moderate",
                "time_to_proficiency": "1-3 months",
                "prerequisites": ["python"],
                "related_skills": ["data_analysis", "numpy"],
                "job_market_demand": "high"
            },
            "numpy": {
                "category": "data_library",
                "learning_curve": "moderate",
                "time_to_proficiency": "1-2 months",
                "prerequisites": ["python"],
                "related_skills": ["data_analysis", "scientific_computing"],
                "job_market_demand": "high"
            }
        }
    
    def scan_ai_commander_jobs(self) -> List[Dict[str, Any]]:
        """Scan AI Commander generated applications for job data"""
        jobs_analyzed = []
        
        if not self.ai_commander_path.exists():
            return jobs_analyzed
        
        # Find all application directories
        for app_dir in self.ai_commander_path.iterdir():
            if app_dir.is_dir():
                summary_file = app_dir / f"application_summary_{app_dir.name}.json"
                if summary_file.exists():
                    try:
                        with open(summary_file, 'r', encoding='utf-8') as f:
                            job_data = json.load(f)
                            jobs_analyzed.append(job_data)
                    except Exception as e:
                        print(f"Error reading job data from {summary_file}: {e}")
        
        print(f"Found {len(jobs_analyzed)} job applications to analyze")
        return jobs_analyzed
    
    def extract_skills_from_job(self, job_data: Dict[str, Any]) -> List[str]:
        """Extract required skills from job data using multiple sources"""
        skills = set()
        
        # From job title
        title = job_data.get('job_information', {}).get('title', '').lower()
        skills.update(self.extract_skills_from_text(title))
        
        # From company tech stack
        tech_stack = job_data.get('company_intelligence', {}).get('tech_stack', [])
        for tech in tech_stack:
            skills.add(tech.lower().strip())
        
        # From emphasized skills in resume customization
        emphasized = job_data.get('resume_customization', {}).get('emphasized_skills', [])
        for skill in emphasized:
            skills.update(self.extract_skills_from_text(skill))
        
        # From application recommendations
        recommendations = job_data.get('company_intelligence', {}).get('application_recommendations', [])
        for rec in recommendations:
            skills.update(self.extract_skills_from_text(rec))
        
        return list(skills)
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from text using pattern matching"""
        if not text:
            return []
        
        text = text.lower()
        found_skills = []
        
        # Check against our skill database
        for skill in self.skill_database.keys():
            if skill in text or skill.replace('_', ' ') in text:
                found_skills.append(skill)
        
        # Pattern-based extraction for common variations
        patterns = {
            r'\bapi\b': 'api_development',
            r'\brest\b': 'rest_api',
            r'\bmachine\s+learning\b': 'machine_learning',
            r'\bdeep\s+learning\b': 'deep_learning',
            r'\bdata\s+science\b': 'data_science',
            r'\bweb\s+development\b': 'web_development',
            r'\bcloud\s+computing\b': 'cloud_computing',
            r'\bdevops\b': 'devops',
            r'\bautomation\b': 'automation',
            r'\binfrastructure\b': 'infrastructure'
        }
        
        for pattern, skill in patterns.items():
            if re.search(pattern, text):
                found_skills.append(skill)
        
        return found_skills
    
    def analyze_current_skills(self, codebase_path: str = None) -> Dict[str, str]:
        """Analyze current skills from codebase and knowledge base"""
        current_skills = {}
        
        # From knowledge base
        kb_skills = self.knowledge_base.get('skills_learned', {})
        current_skills.update(kb_skills)
        
        # From codebase analysis (existing Learning Assistant functionality)
        if codebase_path:
            code_skills = self.analyze_codebase_skills(codebase_path)
            current_skills.update(code_skills)
        
        # Default skills based on background
        default_skills = {
            "infrastructure": "advanced",
            "windows_server": "advanced", 
            "active_directory": "advanced",
            "linux": "intermediate",
            "networking": "intermediate",
            "python": "intermediate",
            "automation": "intermediate",
            "api_integration": "beginner"
        }
        
        # Merge, preferring detected skills over defaults
        for skill, level in default_skills.items():
            if skill not in current_skills:
                current_skills[skill] = level
        
        return current_skills
    
    def analyze_codebase_skills(self, codebase_path: str) -> Dict[str, str]:
        """Analyze skills demonstrated in codebase"""
        skills = {}
        
        try:
            path = Path(codebase_path)
            python_files = list(path.glob("**/*.py"))
            
            imports_found = set()
            patterns_found = set()
            
            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract imports
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports_found.add(alias.name.lower())
                            elif isinstance(node, ast.ImportFrom) and node.module:
                                imports_found.add(node.module.lower())
                    except:
                        pass  # Continue with text analysis
                    
                    # Pattern analysis
                    if 'tkinter' in content.lower():
                        patterns_found.add('gui_development')
                    if 'requests.' in content:
                        patterns_found.add('api_integration')
                    if 'threading' in content.lower():
                        patterns_found.add('concurrent_programming')
                    if 'beautifulsoup' in content.lower():
                        patterns_found.add('web_scraping')
                
                except:
                    continue
            
            # Map imports and patterns to skill levels
            skill_mapping = {
                'tkinter': ('python_gui', 'intermediate'),
                'requests': ('api_integration', 'intermediate'),
                'beautifulsoup4': ('web_scraping', 'intermediate'),
                'bs4': ('web_scraping', 'intermediate'),
                'threading': ('concurrent_programming', 'beginner'),
                'json': ('data_processing', 'intermediate'),
                'pandas': ('data_analysis', 'intermediate'),
                'numpy': ('scientific_computing', 'intermediate'),
                'gui_development': ('python_gui', 'intermediate'),
                'api_integration': ('api_development', 'intermediate'),
                'concurrent_programming': ('multithreading', 'beginner'),
                'web_scraping': ('web_scraping', 'intermediate')
            }
            
            for item in imports_found.union(patterns_found):
                if item in skill_mapping:
                    skill, level = skill_mapping[item]
                    skills[skill] = level
            
            # Estimate Python level based on complexity
            if len(skills) > 3:
                skills['python'] = 'intermediate'
            elif len(skills) > 0:
                skills['python'] = 'beginner'
        
        except Exception as e:
            print(f"Error analyzing codebase: {e}")
        
        return skills
    
    def identify_skill_gaps(self, job_data: Dict[str, Any], current_skills: Dict[str, str]) -> JobSkillAnalysis:
        """Identify skill gaps between current abilities and job requirements"""
        
        # Extract required skills from job
        required_skills = self.extract_skills_from_job(job_data)
        
        # Determine what's missing
        missing_skills = []
        skill_gaps = []
        
        for required_skill in required_skills:
            current_level = current_skills.get(required_skill, "none")
            
            if current_level == "none":
                missing_skills.append(required_skill)
                
                # Create skill gap analysis
                gap = SkillGap(
                    skill_name=required_skill,
                    required_level="intermediate",  # Assume intermediate for job requirements
                    current_level="none",
                    gap_severity=8.0,  # High severity for completely missing skills
                    job_frequency=1,   # Will be updated when we analyze multiple jobs
                    learning_priority=5 if required_skill in ['python', 'machine_learning', 'aws'] else 3,
                    resources=[],      # Will be filled by AI recommendations
                    time_estimate=self.estimate_learning_time(required_skill, "none", "intermediate")
                )
                skill_gaps.append(gap)
            
            elif self.skill_level_to_number(current_level) < self.skill_level_to_number("intermediate"):
                # Existing skill but needs improvement
                gap = SkillGap(
                    skill_name=required_skill,
                    required_level="intermediate", 
                    current_level=current_level,
                    gap_severity=5.0,  # Medium severity for skills that need improvement
                    job_frequency=1,
                    learning_priority=4 if required_skill in ['python', 'machine_learning', 'aws'] else 2,
                    resources=[],
                    time_estimate=self.estimate_learning_time(required_skill, current_level, "intermediate")
                )
                skill_gaps.append(gap)
        
        # Calculate overall match score
        total_required = len(required_skills) if required_skills else 1
        matched_skills = len([s for s in required_skills if s in current_skills and current_skills[s] != "none"])
        overall_match_score = (matched_skills / total_required) * 100
        
        # Determine readiness timeline
        if overall_match_score >= 80:
            readiness_timeline = "Ready now - apply immediately"
        elif overall_match_score >= 60:
            readiness_timeline = "1-2 months with focused learning"
        elif overall_match_score >= 40:
            readiness_timeline = "3-6 months with dedicated study"
        else:
            readiness_timeline = "6+ months - significant skill development needed"
        
        return JobSkillAnalysis(
            job_title=job_data.get('job_information', {}).get('title', 'Unknown'),
            company=job_data.get('job_information', {}).get('company', 'Unknown'),
            required_skills=required_skills,
            preferred_skills=[],  # Could be enhanced to distinguish required vs preferred
            missing_skills=missing_skills,
            skill_gaps=skill_gaps,
            overall_match_score=overall_match_score,
            readiness_timeline=readiness_timeline
        )
    
    def skill_level_to_number(self, level: str) -> int:
        """Convert skill level string to number for comparison"""
        mapping = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
        return mapping.get(level.lower(), 0)
    
    def estimate_learning_time(self, skill: str, current_level: str, target_level: str) -> str:
        """Estimate learning time based on skill difficulty and level gap"""
        if skill in self.skill_database:
            base_time = self.skill_database[skill]['time_to_proficiency']
            learning_curve = self.skill_database[skill]['learning_curve']
            
            # Adjust based on current level
            current_num = self.skill_level_to_number(current_level)
            target_num = self.skill_level_to_number(target_level)
            level_gap = target_num - current_num
            
            if level_gap <= 0:
                return "Already proficient"
            elif level_gap == 1:
                if learning_curve == "easy":
                    return "2-4 weeks"
                elif learning_curve == "moderate": 
                    return "1-2 months"
                else:
                    return "2-4 months"
            else:  # level_gap >= 2
                return base_time
        
        # Default estimates
        if current_level == "none":
            return "2-4 months"
        else:
            return "1-2 months"
    
    def generate_ai_learning_recommendations(self, skill_gaps: List[SkillGap], job_context: str) -> Dict[str, Any]:
        """Use OpenAI to generate personalized learning recommendations"""
        if not self.ai_enabled:
            return self.generate_template_recommendations(skill_gaps)
        
        try:
            # Create context for AI
            gaps_summary = []
            for gap in skill_gaps:
                gaps_summary.append(f"- {gap.skill_name}: Need to go from {gap.current_level} to {gap.required_level} (Priority: {gap.learning_priority}/5)")
            
            prompt = f"""You are an AI learning coach helping an Infrastructure Engineer transition to AI/Automation roles.

BACKGROUND:
- Current role: Infrastructure Engineer with 4+ years experience
- Career goal: AI/Automation Specialist
- Timeline: 30-day job search sprint
- Strengths: Infrastructure reliability (99.8% uptime), Python automation, system administration
- Current projects: Memory Platform (AI family connections), GitHub automation bots

JOB CONTEXT: {job_context}

SKILL GAPS IDENTIFIED:
{chr(10).join(gaps_summary)}

Please provide a comprehensive learning plan with:

1. **Priority Ranking**: Order these skills by learning priority for the job market and this specific role
2. **Learning Strategy**: For each skill, provide:
   - Specific learning resources (courses, books, tutorials)
   - Hands-on project suggestions that build portfolio value
   - Time estimates and milestones
   - How to demonstrate this skill to employers
3. **Integration Opportunities**: Ways to incorporate new skills into existing projects (Memory Platform, automation bots)
4. **Quick Wins**: Skills that can be learned rapidly to boost job applications immediately
5. **Portfolio Projects**: Specific projects that would showcase multiple skills simultaneously

Focus on practical, portfolio-building learning that directly supports the Infrastructure → AI career transition narrative.
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            
            ai_content = response.choices[0].message.content.strip()
            
            return {
                "ai_generated": True,
                "content": ai_content,
                "generated_at": datetime.now().isoformat(),
                "model_used": "gpt-3.5-turbo"
            }
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self.generate_template_recommendations(skill_gaps)
    
    def generate_template_recommendations(self, skill_gaps: List[SkillGap]) -> Dict[str, Any]:
        """Generate template-based learning recommendations when AI is not available"""
        recommendations = []
        
        for gap in skill_gaps:
            skill = gap.skill_name
            
            # Template recommendations based on skill
            if skill == "machine_learning":
                recommendations.append({
                    "skill": skill,
                    "resources": [
                        "Andrew Ng's Machine Learning Course (Coursera)",
                        "Hands-On Machine Learning with Scikit-Learn and TensorFlow",
                        "Kaggle Learn: Machine Learning"
                    ],
                    "projects": [
                        "Add intelligent job matching to your application bot",
                        "Create ML model to predict application success rates",
                        "Build recommendation engine for Memory Platform"
                    ],
                    "time_estimate": gap.time_estimate,
                    "quick_wins": [
                        "Complete Kaggle's Intro to Machine Learning course (4 hours)",
                        "Build a simple classification model with scikit-learn"
                    ]
                })
            elif skill == "python":
                recommendations.append({
                    "skill": skill,
                    "resources": [
                        "Python Crash Course by Eric Matthes",
                        "Automate the Boring Stuff with Python",
                        "Real Python tutorials"
                    ],
                    "projects": [
                        "Enhance existing automation bots with advanced features",
                        "Create data analysis dashboard for job applications",
                        "Build web scraping tool for job market research"
                    ],
                    "time_estimate": gap.time_estimate,
                    "quick_wins": [
                        "Add error handling to existing bots",
                        "Implement logging and monitoring"
                    ]
                })
            elif skill in ["aws", "cloud_computing"]:
                recommendations.append({
                    "skill": skill,
                    "resources": [
                        "AWS Cloud Practitioner certification path",
                        "A Cloud Guru courses",
                        "AWS free tier hands-on practice"
                    ],
                    "projects": [
                        "Deploy Memory Platform to AWS",
                        "Set up automated deployment pipeline",
                        "Create cloud infrastructure monitoring"
                    ],
                    "time_estimate": gap.time_estimate,
                    "quick_wins": [
                        "Deploy a simple web app to AWS EC2",
                        "Set up S3 bucket for project files"
                    ]
                })
            else:
                # Generic recommendation
                recommendations.append({
                    "skill": skill,
                    "resources": [
                        f"Official {skill} documentation",
                        f"YouTube tutorials for {skill}",
                        f"Practice projects with {skill}"
                    ],
                    "projects": [
                        f"Integrate {skill} into existing automation projects",
                        f"Create demo project showcasing {skill}"
                    ],
                    "time_estimate": gap.time_estimate,
                    "quick_wins": [
                        f"Complete basic {skill} tutorial",
                        f"Add {skill} to a simple project"
                    ]
                })
        
        return {
            "ai_generated": False,
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat(),
            "note": "Template-based recommendations. Enable OpenAI for personalized learning paths."
        }
    
    def create_learning_path(self, skill_gaps: List[SkillGap], ai_recommendations: Dict[str, Any]) -> List[LearningPath]:
        """Create structured learning paths for skill development"""
        learning_paths = []
        
        # Group related skills
        skill_groups = self.group_related_skills(skill_gaps)
        
        for group_name, group_skills in skill_groups.items():
            # Create learning path for each group
            path_steps = []
            projects = []
            milestones = []
            success_metrics = []
            total_time = "2-4 months"  # Default
            
            for gap in group_skills:
                # Add learning steps
                path_steps.extend([
                    {
                        "step": f"Foundation: Learn {gap.skill_name} basics",
                        "duration": "1-2 weeks",
                        "resources": [f"Official {gap.skill_name} documentation", "Beginner tutorials"],
                        "deliverable": f"Basic {gap.skill_name} demo project"
                    },
                    {
                        "step": f"Practice: Build {gap.skill_name} project",
                        "duration": "2-3 weeks", 
                        "resources": [f"Hands-on {gap.skill_name} projects", "Community forums"],
                        "deliverable": f"Portfolio-worthy {gap.skill_name} application"
                    },
                    {
                        "step": f"Integration: Add {gap.skill_name} to existing projects",
                        "duration": "1-2 weeks",
                        "resources": ["Existing codebase", "Integration tutorials"],
                        "deliverable": f"Enhanced automation bot with {gap.skill_name}"
                    }
                ])
                
                # Add projects
                projects.extend([
                    f"Build {gap.skill_name} demonstration project",
                    f"Integrate {gap.skill_name} into Memory Platform",
                    f"Create {gap.skill_name} automation tool"
                ])
                
                # Add milestones
                milestones.extend([
                    f"Complete basic {gap.skill_name} tutorial",
                    f"Build first {gap.skill_name} project", 
                    f"Deploy {gap.skill_name} in production"
                ])
                
                # Add success metrics
                success_metrics.extend([
                    f"Can explain {gap.skill_name} concepts clearly",
                    f"Has working {gap.skill_name} project in portfolio",
                    f"Can implement {gap.skill_name} solutions independently"
                ])
            
            learning_path = LearningPath(
                skill_area=group_name,
                current_level="beginner",
                target_level="intermediate",
                total_time_estimate=total_time,
                steps=path_steps[:6],  # Limit to 6 steps to avoid overwhelm
                projects=projects[:3],  # Top 3 projects
                milestones=milestones[:5],  # Top 5 milestones
                success_metrics=success_metrics[:4]  # Top 4 metrics
            )
            
            learning_paths.append(learning_path)
        
        return learning_paths
    
    def group_related_skills(self, skill_gaps: List[SkillGap]) -> Dict[str, List[SkillGap]]:
        """Group related skills together for efficient learning"""
        groups = {
            "AI/Machine Learning": [],
            "Cloud & Infrastructure": [],
            "Data Processing": [],
            "Web Development": [],
            "DevOps & Automation": []
        }
        
        # Categorize skills
        for gap in skill_gaps:
            skill = gap.skill_name.lower()
            
            if any(term in skill for term in ['machine', 'learning', 'ai', 'tensorflow', 'pytorch', 'neural']):
                groups["AI/Machine Learning"].append(gap)
            elif any(term in skill for term in ['aws', 'cloud', 'azure', 'gcp', 'infrastructure']):
                groups["Cloud & Infrastructure"].append(gap)
            elif any(term in skill for term in ['data', 'pandas', 'numpy', 'sql', 'analytics']):
                groups["Data Processing"].append(gap)
            elif any(term in skill for term in ['web', 'javascript', 'html', 'css', 'react', 'node']):
                groups["Web Development"].append(gap)
            elif any(term in skill for term in ['docker', 'kubernetes', 'devops', 'automation', 'ci/cd']):
                groups["DevOps & Automation"].append(gap)
            else:
                # Default to most relevant group
                groups["DevOps & Automation"].append(gap)
        
        # Remove empty groups
        return {name: skills for name, skills in groups.items() if skills}
    
    def save_analysis(self, analysis: Dict[str, Any]) -> str:
        """Save complete analysis to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"learning_analysis_{timestamp}.json"
        filepath = self.learning_data_path / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
            return str(filepath)
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return ""
    
    def update_knowledge_base(self, new_skills: Dict[str, str], analysis_results: Dict[str, Any]):
        """Update knowledge base with new insights"""
        # Update skills learned
        for skill, level in new_skills.items():
            self.knowledge_base["skills_learned"][skill] = level
        
        # Update learning history
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "analysis_type": "job_skill_gap_analysis",
            "skills_analyzed": list(new_skills.keys()),
            "job_count": analysis_results.get("jobs_analyzed_count", 0),
            "recommendations_generated": analysis_results.get("ai_recommendations", {}).get("ai_generated", False)
        }
        self.learning_history.append(history_entry)
        
        # Save updated knowledge base
        kb_path = self.learning_data_path / "knowledge_base.json"
        try:
            with open(kb_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error updating knowledge base: {e}")
        
        # Save learning history
        history_path = self.learning_data_path / "learning_history.json"
        try:
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(self.learning_history, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Error updating learning history: {e}")
    
    def analyze_job_skill_requirements(self, codebase_path: str = ".") -> Dict[str, Any]:
        """Main method: Complete analysis of job requirements vs current skills"""
        print("Starting AI Learning Coach Analysis...")
        
        # Step 1: Scan AI Commander job data
        jobs_data = self.scan_ai_commander_jobs()
        if not jobs_data:
            print("No job applications found. Generate some applications with AI Job Hunt Commander first!")
            return {"error": "No job applications found to analyze"}
        
        # Step 2: Analyze current skills
        print("Analyzing current technical skills...")
        current_skills = self.analyze_current_skills(codebase_path)
        
        # Step 3: Analyze each job for skill gaps
        job_analyses = []
        all_skill_gaps = []
        
        for job_data in jobs_data:
            job_analysis = self.identify_skill_gaps(job_data, current_skills)
            job_analyses.append(job_analysis)
            all_skill_gaps.extend(job_analysis.skill_gaps)
        
        # Step 4: Prioritize skill gaps across all jobs
        prioritized_gaps = self.prioritize_skill_gaps(all_skill_gaps)
        
        # Step 5: Generate AI recommendations
        print("Generating personalized learning recommendations...")
        job_context = f"Analyzing {len(jobs_data)} job applications including roles at: " + ", ".join([job.get('job_information', {}).get('company', 'Unknown') for job in jobs_data])
        ai_recommendations = self.generate_ai_learning_recommendations(prioritized_gaps, job_context)
        
        # Step 6: Create structured learning paths
        print("Creating structured learning paths...")
        learning_paths = self.create_learning_path(prioritized_gaps, ai_recommendations)
        
        # Step 7: Compile complete analysis
        complete_analysis = {
            "analysis_timestamp": datetime.now().isoformat(),
            "jobs_analyzed_count": len(jobs_data),
            "jobs_analyzed": [
                {
                    "title": job.get('job_information', {}).get('title'),
                    "company": job.get('job_information', {}).get('company'),
                    "application_score": job.get('application_score')
                } for job in jobs_data
            ],
            "current_skills": current_skills,
            "job_analyses": [asdict(analysis) for analysis in job_analyses],
            "prioritized_skill_gaps": [asdict(gap) for gap in prioritized_gaps],
            "ai_recommendations": ai_recommendations,
            "learning_paths": [asdict(path) for path in learning_paths],
            "overall_readiness": self.calculate_overall_readiness(job_analyses),
            "next_actions": self.generate_next_actions(prioritized_gaps, ai_recommendations)
        }
        
        # Step 8: Save analysis and update knowledge base
        saved_path = self.save_analysis(complete_analysis)
        self.update_knowledge_base(current_skills, complete_analysis)
        
        print("Analysis complete!")
        print(f"Saved to: {saved_path}")
        
        return complete_analysis
    
    def prioritize_skill_gaps(self, all_gaps: List[SkillGap]) -> List[SkillGap]:
        """Prioritize skill gaps by frequency across jobs and learning priority"""
        
        # Count frequency of each skill across jobs
        skill_frequency = {}
        for gap in all_gaps:
            skill_name = gap.skill_name
            if skill_name in skill_frequency:
                skill_frequency[skill_name].append(gap)
            else:
                skill_frequency[skill_name] = [gap]
        
        # Create prioritized list with updated frequencies
        prioritized = []
        for skill_name, gap_instances in skill_frequency.items():
            # Take the first instance but update its frequency and priority
            primary_gap = gap_instances[0]
            primary_gap.job_frequency = len(gap_instances)
            
            # Increase priority based on frequency
            if primary_gap.job_frequency >= 3:
                primary_gap.learning_priority = min(5, primary_gap.learning_priority + 2)
            elif primary_gap.job_frequency >= 2:
                primary_gap.learning_priority = min(5, primary_gap.learning_priority + 1)
            
            prioritized.append(primary_gap)
        
        # Sort by learning priority (descending) then by job frequency (descending)
        prioritized.sort(key=lambda x: (x.learning_priority, x.job_frequency), reverse=True)
        
        return prioritized
    
    def calculate_overall_readiness(self, job_analyses: List[JobSkillAnalysis]) -> Dict[str, Any]:
        """Calculate overall job market readiness"""
        if not job_analyses:
            return {"overall_score": 0, "status": "No data"}
        
        scores = [analysis.overall_match_score for analysis in job_analyses]
        avg_score = sum(scores) / len(scores)
        
        # Determine readiness status
        if avg_score >= 80:
            status = "Ready - Start applying now"
            recommendations = ["Begin aggressive job application campaign", "Focus on interview preparation"]
        elif avg_score >= 60:
            status = "Nearly Ready - 1-2 months focused learning"
            recommendations = ["Focus on top 3 skill gaps", "Continue building portfolio projects"]
        elif avg_score >= 40:
            status = "Development Phase - 3-6 months needed"
            recommendations = ["Systematic skill building required", "Consider bootcamp or intensive training"]
        else:
            status = "Foundation Phase - 6+ months development needed"
            recommendations = ["Build fundamental skills first", "Consider formal education or certification"]
        
        return {
            "overall_score": round(avg_score, 1),
            "status": status,
            "individual_scores": scores,
            "best_match_score": max(scores),
            "worst_match_score": min(scores),
            "recommendations": recommendations
        }
    
    def generate_next_actions(self, prioritized_gaps: List[SkillGap], ai_recommendations: Dict[str, Any]) -> List[str]:
        """Generate specific next actions to take"""
        actions = []
        
        if not prioritized_gaps:
            actions.append("Great! No critical skill gaps identified. Focus on interview preparation.")
            return actions
        
        # Top 3 skills to focus on
        top_skills = prioritized_gaps[:3]
        
        actions.append("🎯 IMMEDIATE PRIORITIES (Next 2 weeks):")
        for i, gap in enumerate(top_skills, 1):
            actions.append(f"{i}. Start learning {gap.skill_name} - Priority {gap.learning_priority}/5")
        
        actions.append("")
        actions.append("📚 LEARNING ACTIONS:")
        actions.append("• Choose one primary skill from the top 3 to focus on first")
        actions.append("• Dedicate 1-2 hours daily to structured learning")
        actions.append("• Build a portfolio project incorporating the new skill")
        
        actions.append("")
        actions.append("🔧 INTEGRATION ACTIONS:")
        actions.append("• Add new skills to existing automation projects")
        actions.append("• Update resume and portfolio to reflect learning progress")
        actions.append("• Document learning journey for personal brand building")
        
        actions.append("")
        actions.append("📈 TRACKING ACTIONS:")
        actions.append("• Set weekly learning goals and milestones")
        actions.append("• Re-run this analysis monthly to track progress")
        actions.append("• Apply to 1-2 jobs while learning to get market feedback")
        
        return actions


def main():
    """Test the AI Learning Coach"""
    coach = AILearningCoach()
    
    print("AI Learning Coach - Test Mode")
    print("=" * 50)
    
    # Run complete analysis
    analysis = coach.analyze_job_skill_requirements(".")
    
    if "error" in analysis:
        print(f"ERROR: {analysis['error']}")
        print("\nTo test the learning coach:")
        print("1. Generate some job applications with AI Job Hunt Commander first")
        print("2. Then run this analysis to identify skill gaps")
    else:
        print("\nAnalysis completed successfully!")
        print(f"Analyzed {analysis['jobs_analyzed_count']} job applications")
        print(f"Identified {len(analysis['prioritized_skill_gaps'])} skill gaps")
        print(f"Overall readiness: {analysis['overall_readiness']['status']}")
        
        # Show top 3 skill gaps
        if analysis['prioritized_skill_gaps']:
            print("\nTOP SKILL GAPS TO ADDRESS:")
            for i, gap in enumerate(analysis['prioritized_skill_gaps'][:3], 1):
                print(f"{i}. {gap['skill_name']} - Priority {gap['learning_priority']}/5 (appears in {gap['job_frequency']} jobs)")


if __name__ == "__main__":
    main()