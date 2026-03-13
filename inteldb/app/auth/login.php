<?php
session_start();

/* =======================
   DATABASE CONNECTION
======================= */
$pdo = new PDO(
    "mysql:host=sql113.infinityfree.com;dbname=if0_41226934_gossipdb;charset=utf8",
    "if0_41226934",
    "bathrooM09"
);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$error = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && $password === $user['password']) {

        // Store session variables
        $_SESSION['username'] = $user['username'];
        $_SESSION['perms'] = (int)$user['perms'];

        header("Location: /app/fetcherwizard.php"); // redirect after login
        exit;

    } else {
        $error = "Invalid username or password.";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Login</title>
<style>
body { font-family: Arial; margin:40px; }
.card { border:1px solid #ccc; padding:20px; width:300px; border-radius:8px; }
.error { color:red; }
</style>
</head>
<body>

<h2>Login</h2>

<div class="card">
<form method="POST">
<input type="text" name="username" placeholder="Username" required><br><br>
<input type="password" name="password" placeholder="Password" required><br><br>
<button type="submit">Login</button>
</form>

<?php if($error) echo "<p class='error'>$error</p>"; ?>
</div>

</body>
</html>