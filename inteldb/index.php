<?php
require('fpdf.php');

/* =======================
   DATABASE CONNECTION
======================= */
$pdo = new PDO(
    "mysql:host=sql113.infinityfree.com;dbname=if0_41226934_gossipdb;charset=utf8",
    "if0_41226934",
    "bathrooM09"
);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$message = "";
$gossipData = "";

/* =======================
   PDF GENERATION
======================= */
if(isset($_GET['print'])) {

    $token = $_GET['print'];

    $stmt = $pdo->prepare("SELECT * FROM public_gossip_tokens WHERE token=?");
    $stmt->execute([$token]);
    $data = $stmt->fetch();

    if($data) {

        $pdf = new FPDF();
        $pdf->AddPage();
        $pdf->SetFont('Arial','B',16);
        $pdf->Cell(0,10,"Gossip Report",0,1);

        $pdf->SetFont('Arial','',12);
        $pdf->Cell(0,8,"Token: ".$data['token'],0,1);
        $pdf->Ln(5);
        $pdf->MultiCell(0,8,$data['gossip']);

        $pdf->Output();
        exit;

    } else {
        die("Invalid token.");
    }
}

/* =======================
   TOKEN SUBMISSION
======================= */
if(isset($_POST['token'])) {

    $token = trim($_POST['token']);

    $stmt = $pdo->prepare("SELECT * FROM public_gossip_tokens WHERE token=?");
    $stmt->execute([$token]);
    $data = $stmt->fetch();

    if($data) {
        $gossipData = $data['gossip'];
    } else {
        $message = "❌ Invalid token.";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Enter Your Token</title>
<style>
body { font-family: Arial; margin: 50px; text-align:center; }
.card { border:1px solid #ccc; padding:20px; width:500px; margin:auto; border-radius:10px; }
input { padding:10px; width:80%; margin-bottom:15px; }
button { padding:10px 20px; cursor:pointer; }
.gossip { margin-top:20px; text-align:left; white-space:pre-wrap; }
.error { color:red; }
</style>
</head>
<body>

<div class="card">
<h2>🔐 Enter Your Token</h2>

<form method="POST">
<input type="text" name="token" placeholder="Enter token here..." required>
<br>
<button type="submit">View Gossip</button>
</form>

<?php
if($message) {
    echo "<p class='error'>$message</p>";
}

if($gossipData) {
    echo "<div class='gossip'>";
    echo "<h3>Information Retrieved:</h3>";
    echo htmlspecialchars($gossipData);
    echo "</div>";

    echo "<br>";
    echo "<a href='?print=".urlencode($token)."'><button>📄 Print as PDF</button></a>";
}
?>

</div>

</body>
</html>