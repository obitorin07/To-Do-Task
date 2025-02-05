<?php
include 'database.php';

$sql = "SELECT t.task_id, t.task_description, 
               COALESCE(l.is_completed, 0) AS is_completed 
        FROM tasks t 
        LEFT JOIN task_logs l ON t.task_id = l.task_id";

$result = $conn->query($sql);

$tasks = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $tasks[] = $row;
    }
}

// Convert to JSON format
header('Content-Type: application/json');
echo json_encode($tasks);
?>
