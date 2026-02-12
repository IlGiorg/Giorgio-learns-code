<?php
$host = "127.0.0.1";
$port = 3307;
$user = "root";
$pass = ""; // change if needed
$db   = "cable_inventory";

$conn = new mysqli($host, $user, $pass, $db, $port);

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}
?>
