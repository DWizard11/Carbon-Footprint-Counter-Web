const dialog = document.getElementById('summarisedDialog');
const openButton = document.getElementById('openDialog');
const closeButton = document.getElementById('closeDialog');

// Event listener to open the dialog
openButton.addEventListener('click', function() {
  dialog.showModal();
});

// Event listener to close the dialog
closeButton.addEventListener('click', function() {
  dialog.close();
});

// Logout after inactivity 
var timeoutDuration = 5 * 60 * 1000; // 30 minutes
var timeout;

function resetTimeout() {
    clearTimeout(timeout);
    timeout = setTimeout(logout, timeoutDuration);
}

function logout() {
    window.location.href = "/logout";
}

window.onload = function() {
    resetTimeout();
    document.onmousemove = resetTimeout;
    document.onkeypress = resetTimeout;
    document.ontouchstart = resetTimeout;
};