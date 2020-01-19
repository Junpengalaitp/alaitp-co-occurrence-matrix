pl = "PROGRAMMING_LANGUAGE"  # programming language,  e.g. Java, Python
ol = "OTHER_LANGUAGE"  # non-programming language, e.g. 'CSS', 'HTML'
lb = "LIBRARY"  # library, e.g. React, Bootstrap
fw = "FRAMEWORK"  # framework e.g. Spring, Django
cs = "COMPUTER_SCIENCE"  # computer science, low level knowledge
ai = "AI"  # Machine Learning, Deep Learning
pt = "PROTOCOL"  # e.g 'HTTP', 'CORS'
ds = "DATA_STORAGE"  # databases, MySQL, MongoDB
dt = "DATA_TRANSMISSION"  # JSON, RabbitMQ, Kafka
dv = "DIVISION"  # software development division at high level e.g. Front end, Data, Security, Network
ps = "POSITION"  # specific job position, personal
we = "WORK_EXPERIENCE"  # years of work experience
os_ = "OS"  # operating system
sv = "SERVER"  # Nginx, Tomcat, Node,js
ap = "APPROACH"  # software development approach e.g. TDD, AGILE
se = "SOFTWARE_ENGINEERING"  # software engineering process e.g development, testing, optimization
pf = "PLATFORM"  # platforms for software development e.g AWS, Github
ge = "GENERAL"  # individual non-specific skills. e.g 'technical best practises', 'cloud services'
sf = "SOFT_SKILL"  # e.g. skills of interacting with other people 'active communicator', 'technical leadership'
tl = "TOOL"  # tools for software development work e.g. IDEs
at = "ARCHITECT"  # software development architect. e.g. 'REST API'
pd = "SOFTWARE_PRODUCT"  # product to build
ql = "QUALITY"  # code/software quality e.g. easy-to-understand, testable
of = "OFFER"  # salary, benefits
tm = "TEAM"  # team description/culture
cp = "COMPANY"  # company type e.g. startup, FinTech

category_map = {pl: "pl", ol: "ol", lb: "lb", fw: "fw", cs: "cs", ai: "ai", pt: "pt", ds: "ds", dt: "dt", dv: "dv",
                ps: "ps", we: "we", os_: "os", sv: "sv", ap: "ap", se: "se", pf: "pf", ge: "ge", sf: "sf", tl: "tl",
                at: "at", pd: "pd", ql: "ql", of: "of", tm: "tm", cp: "cp"}

category_dict = {category_map[key]: key for key in category_map}
