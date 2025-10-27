document.querySelectorAll('.predict-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    alert('Prediction feature coming soon!');
  });
});
document.querySelectorAll('.ngo-actions button').forEach(btn => {
  btn.addEventListener('click', function () {
    alert('NGO and Payment feature coming soon!');
  });
});

// page2

// Predict buttons feedback
document.querySelectorAll('.predict-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    alert('Prediction feature coming soon!');
  });
});

// Pay & NGO button feedback (if on page 1)
document.querySelectorAll('.ngo-actions button').forEach(btn => {
  btn.addEventListener('click', function () {
    alert('NGO and Payment feature coming soon!');
  });
});

// Search button on Page 2
const searchBtn = document.querySelector('.search-btn');
if (searchBtn) {
  searchBtn.addEventListener('click', () => {
    alert('Water Check Search feature coming soon!');
  });
}

// Feedback for buttons and navigation
document.querySelectorAll('.predict-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    alert('Prediction feature coming soon!');
  });
});
document.querySelectorAll('.ngo-actions button').forEach(btn => {
  btn.addEventListener('click', function () {
    alert('NGO and Payment feature coming soon!');
  });
});
const searchBtn = document.querySelector('.search-btn');
if (searchBtn) {
  searchBtn.addEventListener('click', () => {
    alert('Water Check Search feature coming soon!');
  });
}
// Profile exit button
const exitBtn = document.querySelector('.profile-overlay-btn');
if (exitBtn) {
  exitBtn.addEventListener('click', function () {
    alert('Exit Profile feature coming soon!');
  });
}

// Prevent form actual submission (demo)
const profileForm = document.querySelector('.profile-info-form');
if (profileForm) {
  profileForm.addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Profile saved (demo only)!');
  });
}
