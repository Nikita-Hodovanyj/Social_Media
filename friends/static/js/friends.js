let requestsSection = document.getElementById('requests-section');
let recommendationsSection = document.getElementById('recommendations-section');
let allFriendsSection = document.getElementById('all-friends-section');
let tabElements = document.querySelectorAll('.left .tab-btn');
let mainTab = document.querySelector('.tab-btn:first-child');

function showSection(sectionId) {
    requestsSection.style.display = 'none';
    recommendationsSection.style.display = 'none';
    allFriendsSection.style.display = 'none';
    
    tabElements.forEach(tab => {
        tab.classList.remove('active-tab');
    });
    
    if (sectionId === 'main') {
        requestsSection.style.display = 'block';
        recommendationsSection.style.display = 'block';
        allFriendsSection.style.display = 'block';
        mainTab.classList.add('active-tab');
    } else {
        const targetSection = document.getElementById(`${sectionId}-section`);
        if (targetSection) {
            targetSection.style.display = 'block';
            document.querySelector(`.tab-btn[onclick="showSection('${sectionId}')"]`)
                .classList.add('active-tab');
        }
    }
}

window.addEventListener('DOMContentLoaded', () => {
    showSection('main');
});