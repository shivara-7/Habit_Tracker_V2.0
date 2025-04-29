// Select the "Add Habits" button
const addButton = document.querySelector('.add-button');
// Add click event to "Add Habits" button
addButton.addEventListener('click', function() {
    const habitName = prompt("Enter a new habit:");

    if (habitName && habitName.trim() !== "") {
        const li = document.createElement("li");
        li.textContent = habitName;
        document.getElementById('habitList').appendChild(li);
    } else {
        alert("Please enter a valid habit.");
    }
});
// (Optional) Make ➕ icon clickable too
const plusIcon = document.querySelector('.add-habit-icon');
plusIcon.addEventListener('click', function() {
    const habitName = prompt("Enter a new habit:");

    if (habitName && habitName.trim() !== "") {
        const li = document.createElement("li");
        li.textContent = habitName;
        document.getElementById('habitList').appendChild(li);
    } else {
        alert("Please enter a valid habit.");
    }
});
