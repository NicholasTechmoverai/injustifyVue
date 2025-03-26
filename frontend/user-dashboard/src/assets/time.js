// Get the current time (9:56 AM in this case)
const now = new Date();
now.setHours(9, 56, 0, 0); // Set time to 9:56 AM

// Set 1:00 PM today
const onePM = new Date();
onePM.setHours(13, 0, 0, 0); // 13:00 is 1:00 PM

// Calculate the difference in milliseconds
const diffMs = onePM - now;

// Convert milliseconds to hours and minutes
const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

console.log(`Time difference: ${diffHours} hours and ${diffMinutes} minutes`);