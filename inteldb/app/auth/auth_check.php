<?php
session_start();

/* REQUIRED PERMISSION */
if (!isset($required_perm)) {
    die("Permission level not defined.");
}

/* CHECK LOGIN */
if (!isset($_SESSION['username']) || !isset($_SESSION['perms'])) {
    die("No results or insufficient permission level");
}

/* CHECK PERMISSION LEVEL */
if ($_SESSION['perms'] < $required_perm) {
    die("No results or insufficient permission level");
}
?>