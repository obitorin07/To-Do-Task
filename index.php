<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Daily Task Tracker</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h1>Daily Task Tracker 📅</h1>
    <div class="stats">
      <p>Date: <span id="current-date"></span></p>
      <p>Day: <span id="current-day"></span></p>
      <p>Total Tasks: <span id="total-tasks">0</span></p>
      <p>Completed: <span id="completed-tasks">0</span></p>
    </div>
    
    <div class="input-section">
      <input type="text" id="task-input" placeholder="Enter new task">
      <button id="add-task">➕ Add Task</button>
    </div>
    
    <ul id="task-list"></ul>
    
    <div class="controls">
      <button id="clear-tasks">🗑️ Clear All</button>
    </div>
  </div>
  
  <script src="script.js"></script>
</body>
</html>
