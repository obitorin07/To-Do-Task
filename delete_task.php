<?php
include 'database.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST["clear_all"])) {
        // Clear all tasks
        $sql = "DELETE FROM task_logs";
        $stmt = $conn->prepare($sql);
        $stmt->execute();

        $sql = "DELETE FROM tasks";
        $stmt = $conn->prepare($sql);
        $stmt->execute();

        echo json_encode(["message" => "All tasks deleted successfully"]);
    } else {
        // Delete a single task
        $task_id = $_POST["task_id"];

        // Delete from task_logs
        $sql = "DELETE FROM task_logs WHERE task_id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("i", $task_id);
        $stmt->execute();

        // Delete from tasks if no more references in task_logs
        $sql = "DELETE FROM tasks WHERE task_id = ? AND NOT EXISTS (SELECT 1 FROM task_logs WHERE task_id = ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ii", $task_id, $task_id);
        $stmt->execute();

        echo json_encode(["message" => "Task deleted successfully"]);
    }
}
?>
