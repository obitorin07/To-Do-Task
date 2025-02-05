<?php
include 'database.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if task_id and is_completed are provided
    if (isset($_POST["task_id"]) && isset($_POST["is_completed"])) {
        $task_id = $_POST["task_id"];
        $status = $_POST["is_completed"];

        // Log the received data for debugging
        error_log("Received task_id: " . $task_id);
        error_log("Received is_completed: " . $status);

        // Check if the task already exists in task_logs for today (prevents duplication)
        $check_sql = "SELECT * FROM task_logs WHERE task_id = ? AND task_date = CURDATE()";
        $stmt = $conn->prepare($check_sql);
        $stmt->bind_param("i", $task_id);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows == 0) {
            // Insert the new task log into task_logs table if not already logged today
            $sql = "INSERT INTO task_logs (task_id, is_completed, task_date, task_time) 
                    VALUES (?, ?, CURDATE(), CURRENT_TIME())";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param("ii", $task_id, $status);

            if ($stmt->execute()) {
                // Success: Return a success message
                echo json_encode(["message" => "Task status inserted successfully"]);
            } else {
                // Failure: Return an error message
                echo json_encode(["message" => "Failed to insert task status"]);
            }
        } else {
            // Task already logged today
            echo json_encode(["message" => "Task already logged today"]);
        }
    } else {
        echo json_encode(["message" => "Missing task_id or is_completed"]);
    }
} else {
    echo json_encode(["message" => "Invalid request method"]);
}
?>
