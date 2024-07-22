import axios from 'axios';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000';
const APPLICATIONS_ENDPOINT = `${API_BASE_URL}/applications`;
const STATUS_UPDATE_ENDPOINT = `${API_BASE_URL}/applications/status`;

async function fetchApplications() {
    try {
        const response = await axios.get(APPLICATIONS_ENDPOINT);
        displayApplications(response.data);
    } catch (error) {
        console.error('Error fetching applications:', error);
    }
}

function displayApplications(applications) {
    const applicationsContainer = document.getElementById('applicationsContainer');
    applicationsContainer.innerHTML = '';

    applications.forEach(application => {
        const applicationElement = document.createElement('div');
        applicationElement.innerHTML = `
            <h2>${application.position}</h2>
            <p>${application.company}</p>
            <p>${application.location}</p>
            <button onclick="updateStatus(${application.id}, 'Approved')">Approve</button>
            <button onclick="updateStatus(${application.id}, 'Rejected')">Reject</button>
        `;
        applicationsContainer.appendChild(applicationElement);
    });
}

async function submitApplication(applicationData) {
    try {
        await axios.post(APPLICATIONS_ENDPOINT, applicationData);
        fetchApplications();
    } catch (error) {
        console.error('Error submitting application:', error);
    }
}

async function updateStatus(applicationId, newStatus) {
    try {
        await axios.patch(`${STATUS_UPDATE_ENDPOINT}/${applicationGovId}`, { status: newStatus });
        fetchApplications();
    } catch (error) {
        console.error('Error updating application status:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchApplications();

    const applicationForm = document.getElementById('applicationForm');
    applicationForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(applicationForm);
        const applicationData = {};
        for (let [key, value] of formData.entries()) {
            applicationData[key] = value;
        }
        submitApplication(applicationData);
    });
});