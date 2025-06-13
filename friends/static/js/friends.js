let requestsSection = document.getElementById('requests-section');
let recommendationsSection = document.getElementById('recommendations-section');
let allFriendsSection = document.getElementById('all-friends-section');
let allTabs = document.querySelectorAll('.left .tab-btn');
let mainTabElement = document.querySelector('.tab-btn:first-child');
let addButtons = document.querySelectorAll('.button-add');
let acceptButtons = document.querySelectorAll('.button-accept');

function showSection(sectionId) {
    requestsSection.style.display = 'none';
    recommendationsSection.style.display = 'none';
    allFriendsSection.style.display = 'none';
    
    allTabs.forEach(tab => {
        tab.classList.remove('active-tab');
    });
    
    if (sectionId === 'main') {
        requestsSection.style.display = 'block';
        recommendationsSection.style.display = 'block';
        allFriendsSection.style.display = 'block';
        mainTabElement.classList.add('active-tab');
    } else {
        let targetSection;
        if (sectionId === 'requests') targetSection = requestsSection;
        else if (sectionId === 'recommendations') targetSection = recommendationsSection;
        else if (sectionId === 'all-friends') targetSection = allFriendsSection;
        
        if (targetSection) {
            targetSection.style.display = 'block';
            const activeTab = document.querySelector(`.tab-btn[onclick="showSection('${sectionId}')"]`);
            if (activeTab) {
                activeTab.classList.add('active-tab');
            }
        }
    }
}

function getCSRFToken() {
    const csrfCookieMatch = document.cookie.match(/(^|;)\s*csrftoken\s*=\s*([^;]+)/);
    return csrfCookieMatch ? csrfCookieMatch.pop() : '';
}

function sendFriendRequest(userId) {
    fetch(`/friends/send_request/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    });
}

function acceptFriendRequest(requestId) {
    fetch(`/friends/accept_request/${requestId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const requestElement = document.querySelector(`.request-item[data-id="${requestId}"]`);
            if (requestElement) {
                requestElement.remove();
            }
            location.reload();
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    showSection('main');
    
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-user-id');
            if (userId) {
                sendFriendRequest(userId);
            }
        });
    });
    
    acceptButtons.forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            if (requestId) {
                acceptFriendRequest(requestId);
            }
        });
    });
});