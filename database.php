<?php
$host = "localhost";  // XAMPP default host
$username = "root";   // XAMPP default username
$password = "";       // No password for root user
$database = "to_do_task";  // Your database name

// Create connection
$conn = new mysqli($host, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
