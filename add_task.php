<?php
include 'database.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $task_description = trim($_POST["task_description"]);
    
    if (!empty($task_description)) {
        // Check if task already exists
        $check_sql = "SELECT task_id FROM tasks WHERE task_description = ?";
        $stmt = $conn->prepare($check_sql);
        $stmt->bind_param("s", $task_description);
        $stmt->execute();
        $stmt->store_result();
        
        if ($stmt->num_rows == 0) {
            // Insert new task into `tasks` table
            $insert_task_sql = "INSERT INTO tasks (task_description) VALUES (?)";
            $stmt = $conn->prepare($insert_task_sql);
            $stmt->bind_param("s", $task_description);
            $stmt->execute();
            $task_id = $stmt->insert_id;
        } else {
            $stmt->bind_result($task_id);
            $stmt->fetch();
        }
        
        // Insert into `task_logs` with default values
        $insert_log_sql = "INSERT INTO task_logs (task_id, week_number, is_completed) 
                           VALUES (?, 'Week 1', 0)";
        $stmt = $conn->prepare($insert_log_sql);
        $stmt->bind_param("i", $task_id);
        $stmt->execute();
        
        echo json_encode(["message" => "Task added successfully"]);
    } else {
        echo json_encode(["error" => "Task description cannot be empty"]);
    }
}
?>
