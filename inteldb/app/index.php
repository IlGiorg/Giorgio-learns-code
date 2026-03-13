<?php
// Start session just in case
session_start();

// Redirect to login page
header("Location: /app/auth/login.php");
exit;
?>