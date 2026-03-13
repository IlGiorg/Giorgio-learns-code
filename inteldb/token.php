<?php
$pdo = new PDO(
    "mysql:host=sql113.infinityfree.com;dbname=if0_41226934_gossipdb;charset=utf8",
    "if0_41226934",
    "bathrooM09"
);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$createdToken = "";
$message = "";

if(isset($_POST['create_token'])){
    $token = trim($_POST['token']);
    $gossip = trim($_POST['gossip']);

    if(empty($token)){
        $message = "❌ Please enter a token.";
    } else {
        // Check if token already exists
        $stmt = $pdo->prepare("SELECT * FROM public_gossip_tokens WHERE token=?");
        $stmt->execute([$token]);
        if($stmt->rowCount() > 0){
            $message = "❌ Token already exists, choose another.";
        } else {
            $stmt = $pdo->prepare("INSERT INTO public_gossip_tokens (token, gossip) VALUES (?, ?)");
            $stmt->execute([$token, $gossip]);
            $createdToken = $token;
            $message = "✅ Token created successfully.";
        }
    }
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Create Public Token</title>
<style>
body { font-family: Arial; margin:40px; }
input, textarea { width:100%; padding:8px; margin-bottom:15px; }
button { padding:8px 15px; }
.token-box { background:#f0f0f0; padding:15px; margin-top:20px; }
.success { color:green; font-weight:bold; }
.error { color:red; font-weight:bold; }
</style>
</head>
<body>

<h1>🔐 Create Public Gossip Token</h1>

<?php if($message): ?>
<p class="<?php echo $createdToken ? 'success' : 'error'; ?>"><?php echo $message; ?></p>
<?php endif; ?>

<form method="POST">
<label>Custom Token:</label>
<input type="text" name="token" placeholder="Enter your token here..." required>

<label>Gossip Content:</label>
<textarea name="gossip" placeholder="Enter gossip content..." required></textarea>

<button name="create_token">Save Token</button>
</form>

<?php if($createdToken): ?>
<div class="token-box">
<strong>Token Created:</strong><br>
<?php echo htmlspecialchars($createdToken); ?><br><br>
Share link:<br>
<a href="token.php?token=<?php echo urlencode($createdToken); ?>">token.php?token=<?php echo urlencode($createdToken); ?></a>
</div>
<?php endif; ?>

</body>
</html>