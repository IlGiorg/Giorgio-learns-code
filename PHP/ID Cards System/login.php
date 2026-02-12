<?php
session_start();

$correct_user = "admin";
$correct_pass = "password123";

$username = $_POST['userinput'] ?? '';
$password = $_POST['passinput'] ?? '';

if ($username === $correct_user && $password === $correct_pass) {
    $_SESSION['loggedin'] = true;
    $_SESSION['username'] = $username;
    header("Location: ops.php");
    exit();
} else {
    header("Location: index.html?error=1");
    exit();
}
?>
