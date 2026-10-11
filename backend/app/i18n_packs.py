"""Translations over the Persian source of truth. Missing keys stay Persian."""

_PRODUCT_DETAILS = {
    "en": {
        "enterprise-ai-platform": {
            "tagline": "A private platform to build, deploy, and run enterprise AI",
            "features": [
                {"title": "Central AI platform", "text": "One place for every model, project, and compute resource."},
                {"title": "Multi-team workspace", "text": "Teams work on shared or separate projects at the same time."},
                {"title": "Role-based access", "text": "Precise roles for people, teams, and resources."},
                {"title": "GPU management", "text": "Schedule, allocate, and watch GPU capacity."},
                {"title": "Model serving", "text": "Publish models as stable, scalable services."},
                {"title": "Vector database", "text": "Store and search embeddings for LLM and semantic search."},
                {"title": "Enterprise security", "text": "Layers that protect data, models, and access."},
                {"title": "Private deployment", "text": "On-premises or cloud, with data staying under your control."},
            ],
            "benefits": [
                {"title": "One control plane", "text": "Build and run every AI project from a single platform."},
                {"title": "Faster release", "text": "Shorten the path from research to production."},
                {"title": "Data ownership", "text": "Models and data remain inside the organization."},
                {"title": "Lower GPU cost", "text": "Smarter scheduling reduces infrastructure spend."},
            ],
            "audiences": ["Large enterprises", "Public agencies", "Data-driven companies", "Research teams"],
            "steps": [
                {"title": "Data", "text": "Load, version, and prepare datasets."},
                {"title": "Train", "text": "Train in notebooks and automated pipelines."},
                {"title": "Serve", "text": "Publish the model as a stable service."},
                {"title": "Watch", "text": "Monitor quality and keep improving."},
            ],
            "faqs": [
                {"q": "Can this run inside our network?", "a": "Yes. It deploys privately, on-premises or in the cloud, so data stays in your control."},
                {"q": "Can several teams use it?", "a": "Yes. Separate workspaces and role-based access support many teams."},
                {"q": "How are GPUs managed?", "a": "Capacity is allocated, scheduled, and monitored across users."},
                {"q": "Can models connect to current systems?", "a": "Yes. Standard APIs connect models to existing software."},
            ],
        },
        "ai-assistant": {
            "tagline": "An agent that completes business tasks, not only a chatbot",
            "features": [
                {"title": "Understands conversation", "text": "Reads natural language and the user's intent."},
                {"title": "Keeps context", "text": "Remembers the thread so answers stay coherent."},
                {"title": "Does the work", "text": "Carries out real tasks instead of only replying."},
                {"title": "Connects to systems", "text": "Works with the software and APIs you already use."},
                {"title": "Automates processes", "text": "Runs repetitive workflows."},
                {"title": "Multi-step actions", "text": "Chains steps toward a larger goal."},
                {"title": "Company knowledge", "text": "Answers from internal documents."},
                {"title": "Digital colleague", "text": "Available across departments."},
            ],
            "benefits": [
                {"title": "More than chat", "text": "It acts on the user's behalf."},
                {"title": "Higher output", "text": "Repetitive work no longer fills the day."},
                {"title": "Hands-off flows", "text": "Multi-step work runs without manual handoffs."},
                {"title": "Whole company", "text": "Useful from HR and finance to sales and support."},
            ],
            "audiences": ["Human resources", "Finance", "Customer support", "Sales", "IT", "Management"],
            "steps": [
                {"title": "Understand", "text": "The assistant reads the request and the context."},
                {"title": "Plan", "text": "It chooses the steps required."},
                {"title": "Act", "text": "It calls internal systems and completes the work."},
                {"title": "Report", "text": "It returns a clear result."},
            ],
            "faqs": [
                {"q": "How is this different from a chatbot?", "a": "A chatbot replies. This assistant performs real actions for the user."},
                {"q": "Does it connect to internal systems?", "a": "Yes, through APIs and integrations with existing software."},
                {"q": "Which teams can use it?", "a": "HR, finance, support, sales, IT, and management."},
                {"q": "Does it remember the conversation?", "a": "Yes. History is kept so later answers stay consistent."},
            ],
        },
        "intelligent-bi": {
            "tagline": "Ask in plain language and get tables, charts, and an explanation",
            "features": [
                {"title": "Natural-language questions", "text": "Ask in Persian or English with no technical background."},
                {"title": "Understands the schema", "text": "Finds tables, relations, and structure on its own."},
                {"title": "Many databases", "text": "Query several sources together."},
                {"title": "Writes SQL", "text": "Builds the query that matches the question."},
                {"title": "Safe execution", "text": "Runs queries under control."},
                {"title": "Tables and charts", "text": "Shows results that are easy to read."},
                {"title": "Trends", "text": "Surfaces patterns in company data."},
                {"title": "Plain explanation", "text": "Describes the result for non-technical readers."},
            ],
            "benefits": [
                {"title": "No SQL required", "text": "Business users analyze data themselves."},
                {"title": "Fast answers", "text": "Seconds instead of hours of manual work."},
                {"title": "Two languages", "text": "Questions in Persian and English."},
                {"title": "Decisions from data", "text": "Managers reach insight quickly."},
            ],
            "audiences": ["Business managers", "Analysts", "Sales", "Finance"],
            "steps": [
                {"title": "Ask", "text": "The user asks in Persian or English."},
                {"title": "Build the query", "text": "The platform understands the schema and writes SQL."},
                {"title": "Run safely", "text": "The query runs against the databases."},
                {"title": "Explain", "text": "A table, a chart, and a written explanation come back."},
            ],
            "faqs": [
                {"q": "Do I need to know SQL?", "a": "No. Ask in Persian or English."},
                {"q": "Can it use more than one database?", "a": "Yes. Several sources and engines are supported."},
                {"q": "How are results shown?", "a": "As a table, a chart, and a plain-language explanation."},
                {"q": "Is query execution safe?", "a": "Yes. Queries run under controlled permissions."},
            ],
        },
        "api-gateway": {
            "tagline": "An enterprise API gateway with a visual setup and built-in billing",
            "features": [
                {"title": "Authentication", "text": "Standard identity for API consumers."},
                {"title": "Access control", "text": "Permissions per service and consumer."},
                {"title": "Rate limits", "text": "Protect services from overload."},
                {"title": "Routing and load balancing", "text": "Send traffic to the right service."},
                {"title": "Monitoring", "text": "Live health and performance."},
                {"title": "Versions", "text": "Run several API versions together."},
                {"title": "Plugins", "text": "Add behavior with modular extensions."},
                {"title": "Billing engine", "text": "Calculate usage and customer cost automatically."},
            ],
            "benefits": [
                {"title": "Billing included", "text": "No separate billing product."},
                {"title": "No lost revenue", "text": "Usage is recorded so API income is not missed."},
                {"title": "Visual and instant", "text": "Change settings in a UI. No YAML and no delay."},
                {"title": "Built-in analytics", "text": "Requests, traffic, and errors in one dashboard."},
            ],
            "audiences": ["API businesses", "Large enterprises", "Banks and fintech", "Technology companies"],
            "steps": [
                {"title": "Receive", "text": "API calls enter the gateway."},
                {"title": "Check", "text": "Identity, access, and rate limits are applied."},
                {"title": "Route", "text": "The call is sent to the target service."},
                {"title": "Bill", "text": "Usage is stored and cost is calculated."},
            ],
            "faqs": [
                {"q": "Do I need YAML?", "a": "No. Everything is configured in the visual interface and applies immediately."},
                {"q": "What does the billing engine do?", "a": "It calculates API usage and customer charges automatically."},
                {"q": "Can we add custom plugins?", "a": "Yes. The plugin architecture accepts custom capabilities."},
                {"q": "What analytics are included?", "a": "Request dashboards, performance, traffic, and errors."},
            ],
        },
        "online-queue-system": {
            "tagline": "Online booking and queue management for hospitals, clinics, banks, and offices",
            "features": [
                {"title": "Online booking", "text": "Appointments for any service."},
                {"title": "Live queue", "text": "Current queue status on a digital display."},
                {"title": "SMS updates", "text": "Confirmation, reminders, and status messages."},
                {"title": "Staff dashboard", "text": "Operator desk and management views."},
                {"title": "Many branches", "text": "Run every branch from one system."},
                {"title": "Hours and holidays", "text": "Capacity, calendar, and waiting list."},
                {"title": "Reports", "text": "Visits, service performance, and history."},
                {"title": "Access control", "text": "Roles for staff who use the system."},
            ],
            "benefits": [
                {"title": "Fully digital flow", "text": "Booking and queues live in one system."},
                {"title": "Shorter waits", "text": "A managed queue reduces time in line."},
                {"title": "Better visits", "text": "Online booking and SMS improve the experience."},
                {"title": "Multi-branch", "text": "Services and branches share one console."},
            ],
            "audiences": ["Hospitals", "Clinics", "Banks", "Public agencies", "Universities", "Municipalities"],
            "steps": [
                {"title": "Book", "text": "The visitor reserves a time online."},
                {"title": "Notify", "text": "Confirmation and reminder SMS are sent."},
                {"title": "Queue", "text": "The live queue is shown on displays."},
                {"title": "Call and report", "text": "The turn is called and the visit is recorded."},
            ],
            "faqs": [
                {"q": "Who is this for?", "a": "Hospitals, clinics, banks, public agencies, universities, municipalities, and large organizations."},
                {"q": "Can it cover several branches?", "a": "Yes. All branches are managed from one system."},
                {"q": "Are visitors told about their turn?", "a": "Yes. SMS and a digital display show the status."},
                {"q": "Which reports are included?", "a": "Visit counts, service performance, history, and management reports."},
            ],
        },
        "FaraProject": {
            "tagline": "From strategic portfolio control to precise project and task execution",
            "features": [
                {"title": "Portfolio management", "text": "Prioritize projects and align them with strategic goals."},
                {"title": "Work breakdown", "text": "Define WBS, activities, and dependencies clearly."},
                {"title": "Project scheduling", "text": "Plan timelines and track schedule variance."},
                {"title": "Task management", "text": "Assign ownership, follow status, and finish daily work."},
                {"title": "Resource management", "text": "Allocate people and capacity across projects."},
                {"title": "Progress monitoring", "text": "See live progress, risks, and bottlenecks."},
                {"title": "Management reports", "text": "Dashboards for executives, PMO, and project managers."},
                {"title": "One workspace", "text": "Portfolio, projects, and tasks live in a single system."},
            ],
            "benefits": [
                {"title": "Clear performance", "text": "Project and team status is visible for decisions."},
                {"title": "Organizational alignment", "text": "Strategy connects to plans and daily tasks."},
                {"title": "Fewer deviations", "text": "Time and delivery gaps are found earlier."},
                {"title": "Higher productivity", "text": "Central tracking cuts waste and rework."},
            ],
            "audiences": ["Executives", "Project managers", "PMO offices", "Delivery teams", "Project-driven organizations"],
            "steps": [
                {"title": "Define the portfolio", "text": "Projects are prioritized against company goals."},
                {"title": "Plan", "text": "WBS, schedule, and resources are set."},
                {"title": "Execute and track", "text": "Tasks are assigned and progress is recorded."},
                {"title": "Report and improve", "text": "Management reports guide corrective action."},
            ],
            "faqs": [
                {"q": "Who is FaraProject for?", "a": "Organizations that run several projects at once, from software teams to PMO offices and executives."},
                {"q": "Is it only a task tracker?", "a": "No. It covers portfolio and project management as well as daily tasks."},
                {"q": "Which reports are included?", "a": "Progress, resources, schedule variance, and management dashboards for different roles."},
                {"q": "Who uses the system?", "a": "Executives, project managers, PMO specialists, and delivery team members."},
            ],
        },
    },
}

_SERVICE_DETAILS = {
    "en": {
        "devops": {
            "kicker": "Fara Kherad services",
            "lead": "We help teams make software delivery faster, steadier, and safer.",
            "intro_title": "A full software delivery cycle",
            "intro": [
                "We design the whole path from source control and development to test, release, and monitoring.",
                "No two organizations are alike. The DevOps setup follows your team size, architecture, and goals.",
                "From a small team to a large enterprise, the result scales and fits how you already work.",
            ],
            "offerings_title": "What we deliver",
            "offerings_lead": "Specialized work for your infrastructure",
            "offerings": [
                {"title": "DevOps architecture"},
                {"title": "CI/CD pipelines"},
                {"title": "GitLab and GitLab CI"},
                {"title": "Build and deployment automation"},
                {"title": "Kubernetes and a container platform"},
                {"title": "Docker and runtime environments"},
                {"title": "Infrastructure automation"},
                {"title": "Monitoring and logging"},
                {"title": "A smoother release process"},
            ],
            "why_title": "Why Fara Kherad",
            "why_lead": "We build a path that fits the business, not only a toolchain",
            "why": [
                {"title": "Designed for you", "text": "Processes follow your architecture and constraints."},
                {"title": "Experienced team", "text": "We have shipped DevOps in complex enterprise environments."},
                {"title": "Beside your team", "text": "Design, knowledge transfer, training, and operations support."},
                {"title": "Safe and ready to grow", "text": "A platform you can monitor and scale with confidence."},
            ],
            "cta_lead": "We stay with your team while you build delivery that is automated and reliable.",
            "cta_text": "If you want releases that are faster and safer, talk to us.",
        },
        "mlops": {
            "kicker": "Fara Kherad services",
            "lead": "Start the AI path with infrastructure that matches industrial practice.",
            "intro_title": "From idea to production AI",
            "intro": [
                "We take AI work from an idea to a real production system.",
                "The design follows your models, data volume, compute needs, and business goals.",
                "Whether you are starting or scaling models you already have, the path is practical.",
            ],
            "offerings_title": "What we deliver",
            "offerings_lead": "Specialized work for your AI infrastructure",
            "offerings": [
                {"title": "AI infrastructure design"},
                {"title": "Model-serving platforms"},
                {"title": "Running and managing LLMs"},
                {"title": "Large language model setup"},
                {"title": "GPU infrastructure"},
                {"title": "Compute cost control"},
                {"title": "AI lifecycle design"},
                {"title": "Model and version management"},
                {"title": "MLOps pipelines"},
                {"title": "AI development environments"},
                {"title": "Help building AI products"},
            ],
            "why_title": "Why Fara Kherad",
            "why_lead": "AI infrastructure shaped around the organization's real needs",
            "why": [
                {"title": "Fits the business", "text": "Architecture follows budget and priorities."},
                {"title": "AI practitioners", "text": "Hands-on work with LLMs, GPUs, and production models."},
                {"title": "Cost and performance", "text": "Use compute carefully without wasting spend."},
                {"title": "Through to a product", "text": "We stay for build, test, and launch."},
            ],
            "cta_lead": "We provide what you need to develop, test, and run AI products.",
            "cta_text": "If you want a careful start, contact us.",
        },
    },
}


PACKS = {
    "en": {
        "settings": {
            "company_name": "Fara Kherad",
            "tagline": "Enterprise artificial intelligence",
            "about_title": "About Fara Kherad",
            "about_text": (
                "Fara Kherad is an information technology company focused on enterprise software and artificial intelligence. "
                "We build software, AI products, and infrastructure for large organizations. "
                "A specialist team helps businesses raise performance through AI and digital change."
            ),
            "cta_kicker": "Why Fara Kherad?",
            "cta_title": "Ready to change how the business works?",
            "cta_text": "Talk to the team and get a free consultation on AI and enterprise software.",
            "footer_text": "Enterprise software, artificial intelligence, and infrastructure products",
            "address": "Tehran, Iran",
        },
        "features": {
            "1": {"title": "Automation", "description": "Automate repetitive work and cut human error with AI"},
            "2": {"title": "Higher output", "description": "Finish work faster and free people for strategic tasks"},
            "3": {"title": "Smarter decisions", "description": "Turn data into practical insight for managers"},
            "4": {"title": "Lower cost", "description": "Use resources more carefully and reduce operating cost"},
            "5": {"title": "Data analysis", "description": "Find useful patterns in large volumes of company data"},
        },
        "stats": {
            "1": {"title": "Specialist team", "description": "Experience in enterprise software and AI"},
            "2": {"title": "Modern technology", "description": "Current tools and sound engineering practice"},
            "3": {"title": "Strong security", "description": "Enterprise security standards"},
            "4": {"title": "Room to grow", "description": "Infrastructure that expands with you"},
        },
        "slides": {
            "1": {
                "title": "Enterprise AI, built to run",
                "subtitle": "Artificial intelligence for the next stage of your business",
                "description": "Fara Kherad builds enterprise software, AI products, and the infrastructure behind digital change.",
                "cta_primary_text": "See products",
                "cta_secondary_text": "Contact us",
            },
            "2": {
                "title": "Fara Kherad",
                "subtitle": "Enterprise software and artificial intelligence",
                "description": "We focus on large organizations and build software, AI solutions, and infrastructure products for them.",
                "cta_primary_text": "About us",
                "cta_secondary_text": "Our services",
            },
        },
        "products": {
            "enterprise-ai-platform": {
                "title": "Fara Kherad enterprise AI platform",
                "summary": "Private AI infrastructure: GPU cluster, model serving, vector database, APIs, and enterprise deployment",
                "description": (
                    "A private platform for running AI at organizational scale. "
                    "What you need to build, deploy, and manage AI sits in one place.\n\n"
                    "It covers multi-user workspaces, model lifecycle, GPU capacity, experiment tracking, and pipelines, "
                    "with security, monitoring, role-based access, and on-premises or cloud deployment.\n\n"
                    "Teams build, ship, and operate their AI projects from a single platform, from data and training to serving."
                ),
                "details": _PRODUCT_DETAILS["en"]["enterprise-ai-platform"],
            },
            "ai-assistant": {
                "title": "Fara Kherad AI assistant",
                "summary": "An enterprise assistant based on large language models",
                "description": (
                    "More than a chatbot. An agent that completes business tasks and works beside the team like a digital colleague.\n\n"
                    "It understands conversation, keeps context, connects to company systems, automates processes, and carries out multi-step work.\n\n"
                    "With access to internal knowledge and APIs, it supports many departments and raises output."
                ),
                "details": _PRODUCT_DETAILS["en"]["ai-assistant"],
            },
            "intelligent-bi": {
                "title": "Fara Kherad interactive BI",
                "summary": "AI business intelligence for analysis and decisions",
                "description": (
                    "Ask in Persian or English and receive an answer, a table, and a chart without writing SQL.\n\n"
                    "The platform reads the database structure, connects to several sources, writes and runs SQL safely, "
                    "and explains the result in plain language."
                ),
                "details": _PRODUCT_DETAILS["en"]["intelligent-bi"],
            },
            "api-gateway": {
                "title": "API Gateway",
                "summary": "An enterprise API gateway with authentication, routing, rate limits, monitoring, and security",
                "description": (
                    "A modern gateway with a fully visual setup and a built-in billing engine, so API revenue is not lost.\n\n"
                    "Configuration happens in an interface, not in YAML or on the command line. Changes apply immediately.\n\n"
                    "The billing engine records consumption and calculates what each customer owes."
                ),
                "details": _PRODUCT_DETAILS["en"]["api-gateway"],
            },
            "online-queue-system": {
                "title": "Online appointment and queue system",
                "summary": "Online booking and queue management for hospitals, clinics, banks, and organizations",
                "description": (
                    "A complete platform that digitizes booking and queue management.\n\n"
                    "Organizations offer online appointments, live queues, SMS updates, management dashboards, and a counter desk.\n\n"
                    "Multiple branches, service catalogs, and reports make it suitable for hospitals, clinics, banks, and public agencies."
                ),
                "details": _PRODUCT_DETAILS["en"]["online-queue-system"],
            },
            "FaraProject": {
                "title": "FaraProject, integrated software project management",
                "summary": "An integrated portfolio, project, and task system for planning, progress tracking, resource control, and management reports",
                "description": (
                    "FaraProject is an integrated portfolio, project, and task platform for planning, organizing, running, and controlling organizational work.\n\n"
                    "It connects strategic goals to portfolios, delivery plans, and daily tasks so managers see project status, progress, resources, and team performance in one place.\n\n"
                    "With portfolio control, work breakdown, scheduling, ownership, task tracking, and management reports, project delivery becomes clearer and decisions rest on shared information."
                ),
                "details": _PRODUCT_DETAILS["en"]["FaraProject"],
            },
        },
        "services": {
            "devops": {
                "title": "DevOps services",
                "description": "Design and run the full software path, from code to release and operations.",
                "details": _SERVICE_DETAILS["en"]["devops"],
            },
            "mlops": {
                "title": "MLOps services",
                "description": "AI infrastructure, large language models, GPUs, and the lifecycle of AI projects.",
                "details": _SERVICE_DETAILS["en"]["mlops"],
            },
        },
        "articles": {
            "ai-benefits-for-business": {
                "title": "What AI changes in a business",
                "excerpt": "AI changes how organizations work and opens room for growth.",
                "content": (
                    "Organizations that automate repetitive work reduce human error, raise output, and free people for strategic tasks.\n\n"
                    "Analysis gives managers something they can act on. Models find patterns that static reports miss, and customer service becomes faster and more specific.\n\n"
                    "Private deployment keeps data governance intact. The organization can run AI at scale without depending on public services.\n\n"
                    "Fara Kherad supports that path with an enterprise AI platform, an agent assistant, interactive BI, and DevOps and MLOps services."
                ),
            },
            "devops-services": {
                "title": "Fara Kherad DevOps services",
                "excerpt": "A full delivery cycle, from source control to test, release, and monitoring.",
                "content": (
                    "No two organizations need the same setup. We design DevOps around team size, product architecture, and business goals.\n\n"
                    "The work includes architecture, CI/CD, GitLab, Kubernetes, Docker, infrastructure automation, monitoring, and a cleaner release process.\n\n"
                    "Standard environments shorten release time and reduce manual error. Teams stay on the product while infrastructure is managed as code.\n\n"
                    "We stay from design through rollout so delivery becomes measurable and repeatable."
                ),
            },
            "mlops-services": {
                "title": "Fara Kherad MLOps services",
                "excerpt": "Start AI with suitable infrastructure and industrial practice.",
                "content": (
                    "We help organizations take AI from an idea to production. Infrastructure follows the model, the data, the compute, and the business goal.\n\n"
                    "That includes large language models, GPU capacity, data and model versions, training and serving pipelines, and production monitoring.\n\n"
                    "MLOps closes the gap between data teams and operations: repeatable training, controlled release, and access control over data and models.\n\n"
                    "The result is a stable organizational service, with security and operations considered from the start."
                ),
            },
        },
        "ui": {
            "محصولات نرم‌افزاری": "Software products",
            "خدمات تخصصی زیرساخت و هوش مصنوعی": "Infrastructure and AI services",
            "مقالات": "Articles",
            "تماس با ما": "Contact",
            "نتایج جستجو": "Search results",
            "صفحه پیدا نشد": "Page not found",
        },
    },
}

from app.i18n_extra import EXTRA

PACKS.update(EXTRA)
