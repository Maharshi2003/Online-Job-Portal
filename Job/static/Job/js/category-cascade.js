(function () {
    var CATEGORY_DATA = {
        "Software Development": [
            "Junior Developer",
            "Senior Developer",
            "Python Developer",
            "Java Developer",
            "C++ Developer",
            ".NET Developer",
            "PHP Developer",
            "Mobile App Developer",
            "QA Engineer",
            "Software Architect"
        ],
        "Web Development": [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer",
            "React Developer",
            "Angular Developer",
            "Vue.js Developer",
            "WordPress Developer",
            "UI Engineer",
            "Web Designer",
            "Node.js Developer"
        ],
        "Data Science & AI": [
            "Data Analyst",
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "Deep Learning Intern",
            "NLP Engineer",
            "Business Intelligence Analyst",
            "Data Engineer",
            "Computer Vision Engineer",
            "ML Intern"
        ],
        "Cloud & DevOps": [
            "DevOps Engineer",
            "AWS Engineer",
            "Azure Engineer",
            "Cloud Architect",
            "Site Reliability Engineer",
            "Kubernetes Engineer",
            "CI/CD Engineer",
            "Linux Administrator",
            "Docker Specialist",
            "Cloud Intern"
        ],
        "Cybersecurity & IT Support": [
            "Cybersecurity Analyst",
            "Ethical Hacker",
            "Network Engineer",
            "System Administrator",
            "IT Support Executive",
            "SOC Analyst",
            "Information Security Officer",
            "Help Desk Technician",
            "Database Administrator",
            "IT Intern"
        ],
        "Fresher": [
            "Fresher Python Developer",
            "Fresher Java Developer",
            "Fresher Web Developer",
            "Fresher Frontend Developer",
            "Fresher Backend Developer",
            "Fresher Full Stack Developer",
            "Fresher Software Developer",
            "Fresher Data Analyst",
            "Fresher AI/ML Engineer",
            "Fresher Intern"
        ],
        "Human Resources": [
            "HR Executive",
            "Recruiter",
            "Talent Acquisition Specialist",
            "HR Manager",
            "Payroll Executive",
            "Training Coordinator",
            "Employee Relations Officer",
            "HR Intern",
            "Compensation Analyst",
            "Onboarding Specialist"
        ],
        "Marketing & Sales": [
            "Digital Marketing Executive",
            "Sales Executive",
            "Business Development Executive",
            "SEO Specialist",
            "Content Marketer",
            "Social Media Manager",
            "Brand Manager",
            "Market Research Analyst",
            "Inside Sales Representative",
            "Marketing Intern"
        ],
        "Finance & Accounting": [
            "Accountant",
            "Financial Analyst",
            "Auditor",
            "Tax Consultant",
            "Accounts Executive",
            "Investment Analyst",
            "Payroll Accountant",
            "Cost Accountant",
            "Finance Intern",
            "Bookkeeper"
        ],
        "Operations & Administration": [
            "Operations Executive",
            "Office Administrator",
            "Project Coordinator",
            "Supply Chain Executive",
            "Logistics Coordinator",
            "Customer Support Executive",
            "Operations Manager",
            "Admin Assistant",
            "Procurement Executive",
            "Operations Intern"
        ],
        "Design & Content": [
            "Graphic Designer",
            "UI/UX Designer",
            "Content Writer",
            "Copywriter",
            "Video Editor",
            "Product Designer",
            "Technical Writer",
            "Animator",
            "Creative Director",
            "Design Intern"
        ]
    };

    function fillTypes(select, types, enable, selected) {
        select.innerHTML = '';
        var first = document.createElement('option');
        first.value = '';
        first.textContent = 'Select your sub category';
        select.appendChild(first);
        var list = types ? types.slice() : [];
        if (selected && list.indexOf(selected) === -1) {
            list.unshift(selected);
        }
        list.forEach(function (name) {
            var opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            select.appendChild(opt);
        });
        select.disabled = !enable;
        select.value = (selected && enable) ? selected : '';
    }

    function initCategoryCascade() {
        var category = document.getElementById('seekerCategory') || document.getElementById('category');
        var type = document.getElementById('seekerCategoryType') || document.getElementById('category_type');
        if (!category || !type || category.dataset.cascadeBound === '1') return;
        category.dataset.cascadeBound = '1';

        var initialType = type.getAttribute('data-selected') || '';
        if (category.value) {
            fillTypes(type, CATEGORY_DATA[category.value] || [], true, initialType);
        } else {
            fillTypes(type, [], false);
        }

        category.addEventListener('change', function () {
            var types = CATEGORY_DATA[category.value] || [];
            fillTypes(type, types, !!category.value);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCategoryCascade);
    } else {
        initCategoryCascade();
    }
})();
