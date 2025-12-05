from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, send_file
import secrets
import os

# ==========================================
# CONFIGURATION & DATA
# ==========================================

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secret key for session management

# Data Source - Mapped from Mohd Faaiz Resume
PROFILE_DATA = {
    "hero": {
        "title": "Mohd Faaiz",
        "subtitle": "SRE Engineer with 4 years of exp",
        "description": "Results-focused Site Reliability Engineer with nearly 4 years of experience designing and operating high-availability cloud systems. I specialize in bridging the gap between development and operations.",
        "tags": ["High Availability", "Automation", "Cloud Architecture"],
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1950&q=80"
    },
    "rows": [
        {
            "title": "Projects",
            "content": [
                {
                    "id": "p1",
                    # PROJECT SPECIFIC FIELDS
                    "project_name": "Automated AWS Infra",
                    "tech_stack": "Terraform & VPC Architecture",
                    "details": """
                        <ul class="list-disc pl-5 space-y-2 text-sm md:text-base text-gray-300">
                            <li>Designed and implemented custom AWS VPC architecture with multiple public subnets across availability zones for high availability.</li>
                            <li>Configured Internet Gateway and Route Tables to enable outbound internet access for VPC resources.</li>
                            <li>Developed security groups allowing inbound HTTP (port 80) and SSH (port 22) traffic with appropriate ingress and unrestricted egress rules.</li>
                            <li>Provisioned and launched multiple EC2 instances with custom user data scripts in separate subnets to ensure fault tolerance.</li>
                            <li>Set up a scalable Application Load Balancer with target groups and listeners to distribute incoming traffic across EC2 instances.</li>
                            <li>Created and configured an S3 bucket with ownership controls and public access settings tailored for project requirements.</li>
                            <li>Applied Infrastructure as Code (IaC) principles using Terraform to automate resource provisioning, improving repeatability and reducing manual errors.</li>
                            <li>Enabled modularity and reuse by parameterizing core network CIDR blocks, AMI images, and other critical infrastructure variables.</li>
                        </ul>
                    """,
                    "repo_link": "https://github.com/Faaiz26/Teraform-Aws-Project.git",
                    "project_img": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=500&q=60",
                    
                    # Common Meta Data
                    
                    "duration": "2024",
                    "tags": ["IaC", "AWS", "Security"],
                    "tools": ["Terraform", "AWS VPC", "S3", "EC2", "ALB"]
                },
                {
                    "id": "p2",
                    # PROJECT SPECIFIC FIELDS
                    "project_name": "SRE Monitoring Agent",
                    "tech_stack": "Real-Time Dashboard & Python",
                    "details": """
                        <ul class="list-disc pl-5 space-y-2 text-sm md:text-base text-gray-300">
                            <li>Designed and implemented a custom Python-based monitoring agent to collect key system metrics (CPU, memory, disk usage, and error counts from log files) at regular intervals.</li>
                            <li>Persisted collected metrics in an SQLite database for historical data analysis and reliability.</li>
                            <li>Developed a Prometheus-compatible /metrics endpoint for integration with external monitoring and alerting systems.</li>
                            <li>Created a responsive web dashboard using Flask and Plotly to visualize real-time and historical metrics with auto-refresh, supporting interactive trend analysis for CPU, memory, disk, and log error rates.</li>
                            <li>Engineered a background thread scheduler to automate continuous metric collection and storage, ensuring up-to-date health signal tracking.</li>
                        </ul>
                    """,
                    "repo_link": "https://github.com/Faaiz26/Monitoring-agent-with-real-time-dashboard",
                    "project_img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=500&q=60",
                    
                    # Common Meta Data
                    
                    "duration": "2023",
                    "tags": ["Observability", "Python", "Flask"],
                    "tools": ["Python", "Flask", "Plotly", "Prometheus", "SQLite"]
                }
            ]
        },
        {
            "title": "Experience Episodes",
            "content": [
                {
                    "id": "e1",
                    # EXPERIENCE SPECIFIC FIELDS
                    "company_name": "Diksha Technologies",
                    "role": "Client: Airtel Africa",
                    "key_achievements": """
                        <ul class="list-disc pl-5 space-y-2 text-sm md:text-base text-gray-300">
                            <li>Architected and maintained scalable microservices serving millions across 14 countries.</li>
                            <li>Automated release pipelines with GitOps, reducing deployment time by 60%.</li>
                            <li>Increased uptime and reliability by designing robust failover and leading root cause analysis.</li>
                            <li>Implemented canary deployments ensuring safer and resilient feature rollouts.</li>
                        </ul>
                    """,
                    "company_img": "https://media.glassdoor.com/sqll/442462/diksha-technologies-squarelogo.png",
                    
                    # Common Meta Data
                    "match": "Current Organization",
                    "tenure": "Aug 2024 - Present",
                    "core_competencies": ["SRE", "Operations"],
                    "tools": ["Loki", "Grafana", "Rancher", "GitOps", "MongoDB"]
                },
                {
                    "id": "e2",
                    # EXPERIENCE SPECIFIC FIELDS
                    "company_name": "Tech Mahindra",
                    "role": "Software Engineer",
                    "key_achievements": """
                        <ul class="list-disc pl-5 space-y-2 text-sm md:text-base text-gray-300">
                            <li>Enhanced vRAN automation orchestrator for Rakuten using production log analysis and data-driven optimization.</li>
                            <li>Built automated data pipelines and dashboards enabling real-time monitoring of key metrics.</li>
                            <li>Automated workflows and deployments (Python, Salesforce Flows), boosting stability and reducing manual intervention.</li>
                            <li>Developed fault-tolerant email automation for reliable business communication integrated with Salesforce.</li>
                        </ul>
                    """,
                    "company_img": "https://download.logo.wine/logo/Tech_Mahindra/Tech_Mahindra-Logo.wine.png",
                    
                    # Common Meta Data
                    "match": "Completed",
                    "tenure": "Oct 2021 - Aug 2024",
                    "core_competencies": ["Automation", "VRAN", "Analytics"],
                    "tools": ["Kibana", "Loki", "Python", "Salesforce Flows", "Linux"]
                }
            ]
        },
        {
            "title": "Technical Arsenal (Skills)",
            "content": [
                # SKILL SPECIFIC FIELDS - CONSOLIDATED INTO ONE CARD
                { 
                    "id": "s1", 
                    "skill_name": "Technical Stack", 
                    "category": "All Technical Skills", 
                    "skill_img": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=500&q=60", # Abstract Tech Image
                    "details": """
                        <ul class="list-disc pl-5 space-y-2 text-sm md:text-base">
                            <li><strong class="text-white">Programming/Automation:</strong> Python (NumPy, Pandas, ML libs, TensorFlow), JavaScript</li>
                            <li><strong class="text-white">DevOps Tools:</strong> AWS, Rancher, ArgoCD, Terraform, Jenkins, GitOps</li>
                            <li><strong class="text-white">Cloud & Infrastructure:</strong> Kubernetes (via Rancher), Microservices, Linux</li>
                            <li><strong class="text-white">Monitoring & Observability:</strong> Grafana, Kibana, Loki</li>
                            <li><strong class="text-white">Databases:</strong> SQL, MongoDB</li>
                            <li><strong class="text-white">Salesforce Ecosystem:</strong> Salesforce Flows, LWC, App Builder, Apex</li>
                            <li><strong class="text-white">Others:</strong> Tableau, Google Apps Script, Google CSE</li>
                        </ul>
                    """,
                    "match": "GitOps, Kubernetes",
                    "tools": ["Python", "AWS", "Kubernetes", "Grafana", "SQL", "Salesforce"]
                }
            ]
        }
    ]
}

# ==========================================
# TEMPLATES (HTML/CSS/JS)
# ==========================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mohd Faaiz | SRE Portfolio</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background-color: #141414; color: white; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; overflow-x: hidden; }
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .fade-in { animation: fadeIn 0.5s ease-in; }
        .scale-up { animation: scaleUp 0.3s ease-out; }
        html { scroll-behavior: smooth; } /* Enable smooth scrolling for anchors */
        
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes scaleUp { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        
        .row-poster:hover { transform: scale(1.05); z-index: 10; }
        .netflix-btn { transition: all 0.2s; }
        .netflix-btn:hover { transform: scale(1.05); }
    </style>
</head>
<body>

    {% if not session.get('profile') %}
    <!-- PROFILE GATE SCREEN -->
    <div class="min-h-screen flex flex-col items-center justify-center fade-in">
        <h1 class="text-3xl md:text-5xl font-medium mb-12 tracking-wide">Who's watching?</h1>
        <div class="flex flex-wrap justify-center gap-8 px-4">
            {% for profile in profiles %}
            <a href="{{ url_for('select_profile', name=profile.name) }}" class="group flex flex-col items-center cursor-pointer transition-transform hover:scale-105">
                <div class="w-24 h-24 md:w-32 md:h-32 rounded-md {{ profile.color }} mb-4 flex items-center justify-center shadow-lg group-hover:ring-4 ring-white transition-all overflow-hidden">
                    <span class="text-4xl font-bold opacity-80 uppercase">{{ profile.name[0] }}</span>
                </div>
                <span class="text-gray-400 text-lg group-hover:text-white transition-colors">{{ profile.name }}</span>
            </a>
            {% endfor %}
        </div>
        <button class="mt-20 border border-gray-500 px-6 py-2 text-gray-400 hover:text-white hover:border-white tracking-widest uppercase text-sm transition-colors">
            Manage Profiles
        </button>
    </div>
    
    {% else %}
    
    <!-- MAIN APP SCREEN -->
    <div id="app">
        
        <!-- Navbar -->
        <nav id="navbar" class="fixed w-full z-40 transition-all duration-500 px-4 md:px-12 py-4 flex items-center justify-between bg-gradient-to-b from-black/80 to-transparent">
            <div class="flex items-center gap-8">
                <a href="#" class="text-red-600 text-3xl md:text-4xl font-bold tracking-tighter cursor-pointer no-underline hover:text-red-700">FAAIZ.</a>
                <ul class="hidden md:flex gap-6 text-sm text-gray-200">
                    <li><a href="#" class="font-medium cursor-pointer hover:text-gray-400 transition-colors">Home</a></li>
                    <li><a href="#blockbuster-projects" class="cursor-pointer hover:text-gray-400 transition-colors">Projects</a></li>
                    <li><a href="#experience-episodes" class="cursor-pointer hover:text-gray-400 transition-colors">Experience</a></li>
                </ul>
            </div>
            <div class="flex items-center gap-6">
                <div class="hidden md:flex gap-4 text-white">
                    <a href="https://github.com/Faaiz26" target="_blank"><i class="fab fa-github text-xl hover:text-gray-300"></i></a>
                    <a href="https://www.linkedin.com/in/mohdfaaiz786/" target="_blank"><i class="fab fa-linkedin text-xl hover:text-gray-300"></i></a>
                </div>
                <div class="flex items-center gap-2 cursor-pointer group relative">
                    <div class="w-8 h-8 bg-blue-600 rounded flex items-center justify-center font-bold text-white uppercase text-xs">
                        {{ session.get('profile')[0] }}
                    </div>
                    <i class="fas fa-caret-down text-white"></i>
                    <!-- Dropdown -->
                    <div class="absolute top-full right-0 mt-2 w-32 bg-black border border-gray-700 rounded shadow-xl hidden group-hover:block p-2">
                        <a href="{{ url_for('logout') }}" class="text-white text-sm hover:underline w-full text-left block">Sign out</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Hero Banner -->
        <div class="relative h-[85vh] w-full">
            <div class="absolute inset-0">
                <img src="{{ data.hero.image }}" class="w-full h-full object-cover">
                <div class="absolute inset-0 bg-gradient-to-r from-black via-black/40 to-transparent"></div>
                <div class="absolute inset-0 bg-gradient-to-t from-[#141414] via-transparent to-transparent"></div>
            </div>
            
            <div class="absolute top-[20%] left-4 md:left-12 max-w-2xl space-y-5 p-4 fade-in">
                <div class="flex items-center gap-3 mb-2">
                    <span class="text-red-600 font-black tracking-widest text-4xl md:text-6xl uppercase drop-shadow-lg">S R E</span>
                </div>
                <h1 class="text-4xl md:text-6xl font-bold text-white leading-tight drop-shadow-lg">{{ data.hero.title }}</h1>
                <div class="flex items-center gap-4 text-white font-semibold text-lg drop-shadow-md flex-wrap">
                    <span class="text-green-400">4 years of Exp</span>
                    <span class="border border-gray-400 px-2 text-sm rounded">7869368832</span>
                    <span class="text-sm bg-red-600 px-1 rounded text-white">mohdfaaiz65@gmail.com</span>
                </div>
                <p class="text-white/90 text-lg md:text-xl drop-shadow-md line-clamp-3">{{ data.hero.description }}</p>
                <div class="flex items-center gap-4 pt-4">
                    <!-- RESUME BUTTON -->
                    <a href="https://drive.google.com/file/d/1KAPAJJyL5O_TKc6wJMYOvYVrQh2l4GiM/view?usp=sharing" target="_blank" class="netflix-btn flex items-center gap-2 bg-white text-black px-8 py-3 rounded font-bold text-lg hover:bg-gray-200 transition-colors">
                        <i class="fas fa-play"></i> Download Resume
                    </a>
                    
                    <button onclick="openAboutModal()" class="netflix-btn flex items-center gap-2 bg-gray-500/70 text-white px-8 py-3 rounded font-bold text-lg backdrop-blur-sm">
                        <i class="fas fa-info-circle"></i> More Info
                    </button>
                </div>
            </div>
        </div>

        <!-- Content Rows -->
        <div class="relative z-10 space-y-8 pb-20 mt-8">
            {% for row in data.rows %}
            <div id="{{ row.title|lower|replace(' ', '-')|replace('(', '')|replace(')', '') }}" class="group/row relative scroll-mt-24">
                <h3 class="text-white/90 text-lg md:text-xl font-semibold mb-3 px-4 md:px-12 group-hover/row:text-white transition-colors">{{ row.title }}</h3>
                
                <div class="relative px-4 md:px-12 group">
                    <!-- Scroll Left Btn -->
                    <button onclick="scrollRow('row-{{ loop.index }}', 'left')" class="absolute left-0 top-0 bottom-0 z-40 bg-black/50 w-12 hover:bg-black/70 hidden md:flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-white">
                        <i class="fas fa-chevron-left text-2xl"></i>
                    </button>
                    
                    <!-- Scroll Container -->
                    <div id="row-{{ loop.index }}" class="flex overflow-x-scroll hide-scrollbar space-x-4 pb-4 scroll-smooth">
                        {% for item in row.content %} 
                        <div onclick='openModal({{ item|tojson }})' class="row-poster flex-none w-[200px] md:w-[280px] aspect-video relative rounded-md overflow-hidden cursor-pointer bg-[#202020] transition-all duration-300">
                            <!-- Image Selection Logic -->
                            <img src="{{ item.project_img or item.company_img or item.skill_img or item.image }}" class="w-full h-full object-cover">
                            <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                                <!-- Title Selection Logic -->
                                <h4 class="text-white font-bold text-sm md:text-base drop-shadow-md">{{ item.project_name or item.company_name or item.skill_name }}</h4>
                                <div class="flex gap-2 mt-2 items-center">
                                    <div class="bg-white rounded-full p-1 w-6 h-6 flex items-center justify-center"><i class="fas fa-play text-black text-xs"></i></div>
                                    <div class="border border-gray-400 rounded-full p-1 w-6 h-6 flex items-center justify-center"><i class="fas fa-check text-white text-xs"></i></div>
                                </div>
                                <div class="flex items-center gap-2 mt-2 text-[10px] md:text-xs text-green-400 font-semibold">
                                    <span>{{ item.match or "98% Match" }}</span>
                                    <span class="border border-gray-500 px-1 text-gray-300 rounded-sm">HD</span>
                                </div>
                                <div class="flex flex-wrap gap-1 mt-1">
                                    <!-- Tag Selection Logic -->
                                    {% set tags = item.tags or item.core_competencies or item.genre %}
                                    {% if tags %}
                                        {% for g in tags[:2] %}
                                        <span class="text-[10px] text-white">● {{ g }}</span>
                                        {% endfor %}
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>

                    <!-- Scroll Right Btn -->
                    <button onclick="scrollRow('row-{{ loop.index }}', 'right')" class="absolute right-0 top-0 bottom-0 z-40 bg-black/50 w-12 hover:bg-black/70 hidden md:flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-white">
                        <i class="fas fa-chevron-right text-2xl"></i>
                    </button>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Footer -->
        <footer class="px-4 md:px-12 py-20 text-gray-500 text-sm max-w-5xl mx-auto border-t border-gray-800 mt-10">
            <div class="flex gap-4 mb-4 text-white">
                <i class="fab fa-github text-2xl hover:text-gray-400 cursor-pointer"></i>
                <i class="fab fa-linkedin text-2xl hover:text-gray-400 cursor-pointer"></i>
            </div>
            <p class="mb-4">© 2025 Mohd Faaiz Portfolio Inc.</p>
            <p>Built with Python (Flask) & Tailwind CSS</p>
        </footer>
    </div>

    <!-- MODAL POPUP (Hidden by default) -->
    <div id="infoModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm hidden fade-in" onclick="closeModal()">
        <div class="bg-[#181818] w-full max-w-4xl rounded-lg shadow-2xl overflow-hidden relative scale-up max-h-[90vh] overflow-y-auto" onclick="event.stopPropagation()">
            <button onclick="closeModal()" class="absolute top-4 right-4 z-20 bg-[#181818] rounded-full p-2 hover:bg-white/20 text-white w-10 h-10 flex items-center justify-center">
                <i class="fas fa-times text-xl"></i>
            </button>

            <!-- Modal Hero -->
            <div class="relative h-64 md:h-96">
                <div class="absolute inset-0 bg-gradient-to-t from-[#181818] via-transparent to-transparent z-[1]"></div>
                <img id="modalImg" src="" class="w-full h-full object-cover">
                <div class="absolute bottom-0 left-0 p-8 z-10 w-full">
                    <h2 id="modalTitle" class="text-3xl md:text-5xl font-bold text-white mb-2"></h2>
                    <p id="modalSubtitle" class="text-xl text-gray-300"></p>
                </div>
            </div>

            <!-- Modal Content -->
            <div class="p-8 grid md:grid-cols-3 gap-8 text-white">
                <div class="md:col-span-2 space-y-6">
                    <div class="flex items-center space-x-4 text-sm font-semibold">
                        <span class="text-green-400" id="modalMatch">98% Match</span>
                        <span class="text-gray-400" id="modalDuration">2024</span>
                        <div id="modalGenres" class="flex gap-2"></div>
                    </div>
                    <!-- Updated to use innerHTML to support HTML bullets -->
                    <div id="modalDesc" class="text-lg leading-relaxed text-gray-300"></div>
                    
                    <div class="flex gap-4 pt-4">
                        <a id="modalLink" href="#" target="_blank" class="hidden flex items-center gap-2 bg-white text-black px-6 py-2 rounded font-bold hover:bg-gray-200 transition-colors">
                            <i class="fab fa-github"></i> View Code
                        </a>
                    </div>
                </div>
                <div class="md:col-span-1 border-l border-gray-700 pl-4">
                    <div class="text-gray-400 text-sm mb-2">Tech Stack :</div>
                    <div id="modalTools" class="flex flex-wrap gap-2 text-sm text-white"></div>
                    
                </div>
            </div>
        </div>
    </div>
    
    <!-- JAVASCRIPT LOGIC -->
    <script>
        // Navbar Scroll Effect
        window.addEventListener('scroll', () => {
            const nav = document.getElementById('navbar');
            if(nav) {
                if (window.scrollY > 50) {
                    nav.classList.remove('bg-transparent', 'bg-gradient-to-b');
                    nav.classList.add('bg-[#141414]');
                } else {
                    nav.classList.add('bg-gradient-to-b');
                    nav.classList.remove('bg-[#141414]');
                }
            }
        });

        // Horizontal Scroll
        function scrollRow(elementId, direction) {
            const container = document.getElementById(elementId);
            const scrollAmount = window.innerWidth / 1.5;
            if (direction === 'left') {
                container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            } else {
                container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            }
        }

        // Modal Logic
        const modal = document.getElementById('infoModal');
        
        function openModal(item) {
            // MAPPING LOGIC for DISTINCT FIELDS
            const title = item.project_name || item.company_name || item.skill_name || item.title;
            const subtitle = item.tech_stack || item.role || item.category || item.subtitle;
            const img = item.project_img || item.company_img || item.skill_img || item.image;
            const desc = item.details || item.key_achievements || item.description || "No description provided.";
            const duration = item.duration || item.tenure || "2024";
            const tags = item.tags || item.core_competencies || item.genre || [];
            const link = item.repo_link || item.link;

            document.getElementById('modalTitle').innerText = title;
            document.getElementById('modalSubtitle').innerText = subtitle || '';
            document.getElementById('modalImg').src = img;
            
            // CHANGED: Use innerHTML to allow bullet points to render
            document.getElementById('modalDesc').innerHTML = desc;
            
            document.getElementById('modalMatch').innerText = item.match || "98% Match";
            document.getElementById('modalDuration').innerText = duration;
            
            // Genres/Tags
            const genreContainer = document.getElementById('modalGenres');
            genreContainer.innerHTML = '';
            if (tags && tags.length > 0) {
                tags.forEach(g => {
                     const span = document.createElement('span');
                     span.className = "border border-gray-600 rounded px-2 py-0.5 text-xs text-gray-300";
                     span.innerText = g;
                     genreContainer.appendChild(span);
                });
            }

            // Tools
            const toolsContainer = document.getElementById('modalTools');
            toolsContainer.innerHTML = '';
            if (item.tools) {
                item.tools.forEach(t => {
                    const span = document.createElement('span');
                    span.className = "text-white hover:underline cursor-pointer mr-2";
                    span.innerText = t + ",";
                    toolsContainer.appendChild(span);
                });
            }

            // Link
            const linkBtn = document.getElementById('modalLink');
            if (link) {
                linkBtn.href = link;
                linkBtn.classList.remove('hidden');
            } else {
                linkBtn.classList.add('hidden');
            }

            modal.classList.remove('hidden');
        }

        function closeModal() {
            modal.classList.add('hidden');
        }

        // Helpers for Hero Buttons
        
        function openAboutModal() {
             const aboutData = {
                title: "About Mohd Faaiz",
                subtitle: "SRE",
                image: "{{ data.hero.image }}",
                description: `
                    <p class="mb-4">Results-focused Site Reliability Engineer with 3.9 years of experience designing and 
operating high-availability cloud systems. Adept at automation, reducing deployment times, 
uptime improvement, and incident response within large-scale environments. Skilled at 
bridging development and operations for efficient continuous delivery, with a track record of 
building resilient, scalable solutions powering millions of users. </p>
                    <div class="mt-4 border-t border-gray-700 pt-4 text-sm text-gray-300">
                        <div class="flex flex-col gap-2">
                            <div class="flex items-center gap-2">
                                <i class="fas fa-envelope text-red-600 w-5"></i>
                                <a href="mailto:mohdfaaiz65@gmail.com" class="hover:text-white transition-colors">mohdfaaiz65@gmail.com</a>
                            </div>
                            <div class="flex items-center gap-2">
                                <i class="fas fa-phone text-red-600 w-5"></i>
                                <span class="hover:text-white transition-colors">7869368832</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <i class="fab fa-linkedin text-red-600 w-5"></i>
                                <a href="https://www.linkedin.com/in/mohdfaaiz786/" target="_blank" class="hover:text-white transition-colors">linkedin.com/in/mohdfaaiz786/</a>
                            </div>
                            <div class="flex items-center gap-2">
                                <i class="fab fa-github text-red-600 w-5"></i>
                                <a href="https://github.com/Faaiz26" target="_blank" class="hover:text-white transition-colors">github.com/Faaiz26</a>
                            </div>
                        </div>
                    </div>
                `,
                tools: ["Problem Solving", "Incident Response", "Automation"],
                
            };
            openModal(aboutData);
        }
    </script>
    {% endif %}
</body>
</html>
"""

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def index():
    # If already logged in, go to browse
    if 'profile' in session:
        return redirect(url_for('browse'))
    
    # Profile selection data
    profiles = [
        {"name": "Recruiter", "color": "bg-blue-600"}
    ]
    return render_template_string(HTML_TEMPLATE, profiles=profiles, data=None)

@app.route('/select_profile/<name>')
def select_profile(name):
    session['profile'] = name
    return redirect(url_for('browse'))

@app.route('/browse')
def browse():
    if 'profile' not in session:
        return redirect(url_for('index'))
    
    return render_template_string(HTML_TEMPLATE, data=PROFILE_DATA)

@app.route('/download_resume')
def download_resume():
    return redirect("https://drive.google.com/file/d/1KAPAJJyL5O_TKc6wJMYOvYVrQh2l4GiM/view?usp=sharing")

@app.route('/logout')
def logout():
    session.pop('profile', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starting Netflix-Style Portfolio...")
    print("Go to http://127.0.0.1:5000 in your browser")
    app.run(debug=True)