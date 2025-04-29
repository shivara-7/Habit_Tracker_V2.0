document.addEventListener('DOMContentLoaded', function() {
    const addHabitForm = document.getElementById('addHabitForm');
    const markDoneForm = document.getElementById('markDoneForm');
    const habitsListElement = document.getElementById('habitsList') ? document.getElementById('habitsList').querySelector('ul') : null;

    function fetchHabits() {
        if (!habitsListElement) return;
        fetch('/get_habits')
            .then(response => response.json())
            .then(habits => {
                habitsListElement.innerHTML = '';
                habits.forEach(habit => {
                    const li = document.createElement('li');
                    li.textContent = `${habit.name} (Goal: ${habit.goal || 'N/A'}, ID: ${habit.id})`;
                    habitsListElement.appendChild(li);
                });
            });
    }

    if (addHabitForm) {
        addHabitForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const habitName = document.getElementById('habitName').value;
            const habitGoal = document.getElementById('habitGoal').value;
            fetch('/add_habit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ habitName: habitName, habitGoal: habitGoal }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    fetchHabits();
                    addHabitForm.reset();
                } else if (data.error) {
                    alert(data.error);
                }
            });
        });
    }

    if (markDoneForm) {
        markDoneForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const habitId = document.getElementById('habitId').value;
            const date = document.getElementById('date').value;
            fetch('/mark_habit_done', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ habitId: parseInt(habitId), date: date }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || data.error || 'Status updated');
                markDoneForm.reset();
            });
        });
    }

    if (habitsListElement) {
      fetchHabits();
    }
});