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