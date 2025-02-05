document.addEventListener("DOMContentLoaded", () => {
    const taskListEl = document.getElementById("task-list");
    const taskInputEl = document.getElementById("task-input");
    const addTaskButton = document.getElementById("add-task");
    const clearTasksButton = document.getElementById("clear-tasks");

    // Fetch tasks from the database
    function fetchTasks() {
        fetch("fetch_tasks.php")
            .then(response => response.json())
            .then(tasks => {
                taskListEl.innerHTML = "";
                tasks.forEach(task => {
                    const li = document.createElement("li");
                    li.innerHTML = `
                        <span>${task.task_description}</span>
                        <select onchange="updateTaskStatus(${task.task_id}, this.value)" id="task-status-${task.task_id}">
                            <option value="0" ${task.is_completed === "0" ? "selected" : ""}>Not Completed</option>
                            <option value="1" ${task.is_completed === "1" ? "selected" : ""}>Completed</option>
                        </select>
                        <button onclick="deleteTask(${task.task_id})">Delete</button>
                        <button onclick="saveTaskStatus(${task.task_id})">Save</button>
                    `;
                    taskListEl.appendChild(li);
                });
            });
    }

    // Add new task
    addTaskButton.addEventListener("click", () => {
        const taskDescription = taskInputEl.value.trim();
        if (taskDescription === "") return;

        fetch("add_task.php", {
            method: "POST",
            body: new URLSearchParams({ task_description: taskDescription }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        }).then(() => {
            taskInputEl.value = "";
            fetchTasks();
        });
    });

    // Update task status (Completed/Not Completed)
    window.updateTaskStatus = (taskId, status) => {
        const statusDropdown = document.getElementById(`task-status-${taskId}`);
        statusDropdown.value = status;
    };

    // Save task status (Completed/Not Completed) and insert into task_logs
    window.saveTaskStatus = (taskId) => {
        const statusDropdown = document.getElementById(`task-status-${taskId}`);
        const status = statusDropdown.value;

        console.log("Saving task ID:", taskId, "Status:", status);  // Log to see if the data is correct

        // Send the data to insert the task log into the database
        fetch("update_task.php", {
            method: "POST",
            body: new URLSearchParams({ task_id: taskId, is_completed: status }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response from update_task.php:", data); // Log the response from the server
            // After saving, update the task list with the latest data
            fetchTasks();  // Refresh the task list with updated task status
        })
        .catch(error => console.log("Error inserting task:", error));  // Log if there is an error
    };

    // Delete task
    window.deleteTask = (taskId) => {
        fetch("delete_task.php", {
            method: "POST",
            body: new URLSearchParams({ task_id: taskId }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        }).then(() => fetchTasks());
    };

    // Clear all tasks
    clearTasksButton.addEventListener("click", () => {
        fetch("delete_task.php", {
            method: "POST",
            body: new URLSearchParams({ clear_all: true }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        }).then(() => fetchTasks());
    });

    // Initial fetch and display of tasks
    fetchTasks();
});
