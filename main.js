import axios from 'axios';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000';
const APPLICATIONS_API = `${API_BASE_URL}/applications`;
const STATUS_UPDATE_API = `${API_BASE_URL}/applications/status`;

async function retrieveApplications(filterStatus = '') {
    try {
        const response = await axios.get(APPLICATIONS_API);
        const applications = filterStatus ? response.data.filter(app => app.status === filterStatus) : response.data;
        renderApplications(applications);
    } catch (error) {
        console.error('Error retrieving applications:', error);
    }
}

function renderApplications(applications) {
    const applicationsListElement = document.getElementById('applicationsContainer');
    applicationsListElement.innerHTML = '';

    applications.forEach(app => {
        const applicationDiv = document.createElement('div');
        applicationDiv.innerHTML = `
            <h2>${app.position}</h2>
            <p>${app.company}</p>
            <p>${app.location}</p>
            <p>Status: ${app.status}</p>
            <button onclick="changeApplicationStatus(${app.id}, 'Approved')">Approve</button>
            <button onclick="changeApplicationStatus(${app.id}, 'Rejected')">Reject</button>
        `;
        applicationsListElement.appendChild(applicationDiv);
    });
}

async function sendApplication(applicationInfo) {
    try {
        await axios.post(APPLICATIONS_API, applicationInfo);
        retrieveApplications();
    } catch (error) {
        console.error('Error sending application:', error);
    }
}

async function changeApplicationStatus(appId, newStatus) {
    try {
        await axios.patch(`${STATUS_UPDATE_API}/${appId}`, { status: newStatus });
        retrieveApplications();
    } catch (error) {
        console.error('Error changing application status:', error);
    }
}

function setupFilter() {
    const filterElement = document.getElementById('statusFilter');
    filterElement.addEventListener('change', () => {
        retrieveApplications(filterElement.value);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    retrieveApplications();
    setupFilter();

    const applicationFormElement = document.getElementById('applicationForm');
    applicationFormElement.addEventListener('submit', (e) => {
        e.preventDefault();
        const formInputData = new FormData(applicationFormElement);
        const applicationData = {};
        for (let [key, value] of formInputData.entries()) {
            applicationData[key] = value;
        }
        sendApplication(applicationData);
    });
});