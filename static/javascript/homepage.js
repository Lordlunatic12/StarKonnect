// render job card
const renderCard = (data, index) => {
    return `<div class="job-${index} job-card ${data.featured ? 'featured' : ''}">
        <div class="job-card-item">
            <div class="job-logo">
                <img src="${data.logo}" alt="${data.company}"/>
            </div>
            <div class="job-info">
                <div class="job-company">
                    <span class="company">${data.company}</span>
                    ${data.new ? '<span class="tag tag-rounded tag-green">New!</span>' : ''}
                    ${data.featured? '<span class="tag tag-rounded tag-black">Featured</span>' : ''}
                </div>
                <div class="job-post">${data.position}</div>
                <div class="job-others">
                    <div class="days-ago">${data.postedAt}</div>
                    <div class="job-type">${data.contract}</div>
                    <div class="job-location">${data.location}</div>
                </div>
            </div>
        </div>
        <div class="job-tags">
            ${renderTags(data.role, data.level, !("languages" in data) ? [] : data.languages, !("tools" in data) ? [] : data.tools, 0)}
        </div>
        <div>
        <form action="http://localhost:5000/applyjob/${data.company}" method="POST" id="applyform">
    			<button class="apply-btn" onclick="document.getElementById('applyform').submit();">Apply</button>
          </form>
    		</div>
    </div>`;
}

// render tag in job cards
const renderTags = (role, level, languages = [], tools = [], isSearch = false) => {
    return [role, level, ...languages, ...tools].map(v => {
        return `<span class="tag tag-lg tag-light-green">${v} ${isSearch ? ' <img src="../static/images/icon-remove.svg" class="remove-icon" alt="remove" /> ' : ''}</span>`;
    });
};

const renderSearchTags = (data, isSearch = true) => {
    console.log(data);
    return data.map(v => {
        return `<span class="tag tag-lg tag-light-green">${v} ${isSearch ? ' <img src="../static/images/icon-remove.svg" class="remove-icon" alt="remove" /> ' : ''}</span>`;
    });
}

// define data
let data = [
    {
      "id": 1,
      "company": "Photosnap",
      "logo": "../static/images/photosnap.svg",
      "new": true,
      "featured": true,
      "position": "Senior Frontend Developer",
      "role": "Frontend",
      "level": "Senior",
      "postedAt": "1d ago",
      "contract": "Full Time",
      "location": "USA Only",
      "languages": ["HTML", "CSS", "JavaScript"],
      "tools": ["React"]
    },
    {
      "id": 2,
      "company": "Manage",
      "logo": "../static/images/manage.svg",
      "new": true,
      "featured": true,
      "position": "Fullstack Developer",
      "role": "Fullstack",
      "level": "Midweight",
      "postedAt": "1d ago",
      "contract": "Part Time",
      "location": "Remote",
      "languages": ["Python"],
      "tools": ["React"]
    },
    {
      "id": 3,
      "company": "Account",
      "logo": "../static/images/account.svg",
      "new": true,
      "featured": false,
      "position": "Junior Frontend Developer",
      "role": "Frontend",
      "level": "Junior",
      "postedAt": "2d ago",
      "contract": "Part Time",
      "location": "USA Only",
      "languages": ["JavaScript"],
      "tools": ["React", "Sass"]
    },
    {
      "id": 4,
      "company": "MyHome",
      "logo": "../static/images/myhome.svg",
      "new": false,
      "featured": false,
      "position": "Junior Frontend Developer",
      "role": "Frontend",
      "level": "Junior",
      "postedAt": "5d ago",
      "contract": "Part Time",
      "location": "USA Only",
      "languages": ["CSS", "JavaScript"],
      "tools": ["React"]
    },
    {
      "id": 5,
      "company": "Loop Studios",
      "logo": "../static/images/loop-studios.svg",
      "new": false,
      "featured": false,
      "position": "Software Engineer",
      "role": "FullStack",
      "level": "Midweight",
      "postedAt": "1w ago",
      "contract": "Full Time",
      "location": "Worldwide",
      "languages": ["JavaScript"],
      "tools": ["Ruby", "Sass"]
    },
    {
      "id": 6,
      "company": "FaceIt",
      "logo": "../static/images/faceit.svg",
      "new": false,
      "featured": false,
      "position": "Junior Backend Developer",
      "role": "Backend",
      "level": "Junior",
      "postedAt": "2w ago",
      "contract": "Full Time",
      "location": "UK Only",
      "languages": ["R"],
      "tools": ["RoR"]
    },
    {
      "id": 7,
      "company": "Shortly",
      "logo": "../static/images/shortly.svg",
      "new": false,
      "featured": false,
      "position": "Junior Developer",
      "role": "Frontend",
      "level": "Junior",
      "postedAt": "2w ago",
      "contract": "Full Time",
      "location": "Worldwide",
      "languages": ["HTML", "JavaScript"],
      "tools": ["Sass"]
    },
    {
      "id": 8,
      "company": "Insure",
      "logo": "../static/images/insure.svg",
      "new": false,
      "featured": false,
      "position": "Junior Frontend Developer",
      "role": "Frontend",
      "level": "Junior",
      "postedAt": "2w ago",
      "contract": "Full Time",
      "location": "USA Only",
      "languages": ["JavaScript"],
      "tools": ["Vue, Sass"]
    },
    {
      "id": 9,
      "company": "Eyecam Co",
      "logo": "../static/images/eyecam-co.svg",
      "new": false,
      "featured": false,
      "position": "Full Stack Engineer",
      "role": "Fullstack",
      "level": "Midweight",
      "postedAt": "3w ago",
      "contract": "Full Time",
      "location": "Worldwide",
      "languages": ["JavaScript", "Python"],
      "tools": ["Django"]
    },
    {
      "id": 10,
      "company": "The Air Filter Company",
      "logo": "../static/images/the-air-filter-company.svg",
      "new": false,
      "featured": false,
      "position": "Front-end Dev",
      "role": "Frontend",
      "level": "Junior",
      "postedAt": "1w ago",
      "contract": "Part Time",
      "location": "Worldwide",
      "languages": ["JavaScript"],
      "tools": ["React", "Sass"]
    }
];

// define elements
const jobListing = document.querySelector('.job-listing');
const jobListingSearchWraper = document.querySelector('.job-listing-search');
const jobListingSearch = document.querySelector('.job-search-tags');
const jobListingClear = document.querySelector('.job-search-clear');
let searchItems = [];
let originalData = data;

const filterJobList = (job, item) => {
    if("languages" in job && job.languages.includes(item))
        return job.languages.includes(item);
    else if("tools" in job && job.tools.includes(item))
        return job.tools.includes(item);
    else
        return job.role === item || job.level === item;
}

jobListingClear.addEventListener('click', e => {
    e.preventDefault();
    searchItems = [];
    loadJobPosts(originalData);
});

const loadJobPosts = async (data) => {
    jobListing.innerHTML = '';
    jobListingSearch.innerHTML = '';
    jobListingSearchWraper.classList.remove('active');
    await data.map((job, index) => { jobListing.innerHTML += renderCard(job, index); });
    const jobTags = document.querySelectorAll('.job-tags .tag');
    await jobTags.forEach(jobTag => {
        jobTag.addEventListener('click', async (e) => {
            e.preventDefault();
            let item = e.target.innerText;
            searchItems = searchItems.includes(item) ? searchItems : [ ...searchItems, item ];
            let filteredData = data.filter(job => filterJobList(job, item));
            loadJobPosts(filteredData);
        });
    });
    if(searchItems.length > 0){
        jobListingSearchWraper.classList.add('active');
        jobListingSearch.innerHTML = renderSearchTags(searchItems);
        const jobSearchTags = document.querySelectorAll('.job-search-tags .tag');
        await jobSearchTags.forEach(jobSearchTag => {
            jobSearchTag.addEventListener('click', async (e) => {
                e.preventDefault();
                let item = e.target.parentNode.innerText;
                searchItems = searchItems.filter(searchItem => searchItem !== item);
                let filteredData = [];
                if(searchItems.length > 0)
                    filteredData = await searchItems.map(searchItem => originalData.filter(job => filterJobList(job, searchItem)));
                loadJobPosts((filteredData.length > 0 && filteredData[0].length > 0) ? filteredData[0] : originalData);
            });
        })
    }
}

loadJobPosts(data);
