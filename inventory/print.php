<?php
include "db.php";

$where = [];
$params = [];

if (!empty($_GET['bucket'])) {
    $where[] = "cablebucket = ?";
    $params[] = $_GET['bucket'];
}

$sql = "SELECT * FROM cables";
if ($where) $sql .= " WHERE " . implode(" AND ", $where);

$stmt = $conn->prepare($sql);
if ($params) $stmt->bind_param("s", ...$params);

$stmt->execute();
$result = $stmt->get_result();
?>

<!DOCTYPE html>
<html>
<head>
<title>Print With Barcodes</title>
<style>
body { font-family: Arial, sans-serif; }
.card {
    border: 1px solid #000;
    padding: 12mm;
    margin-bottom: 10mm;
    page-break-inside: avoid;
}
.barcode {
    display: block;
    width: 70mm;
    height: auto;
    margin-top: 6mm;
}
@media print {
    body { margin: 10mm; }
}
</style>
</head>
<body onload="window.print()">

<h2>Cable Inventory (With Barcodes)</h2>

<?php while ($row = $result->fetch_assoc()): ?>
<div class="card">
    <strong>ID:</strong> <?= htmlspecialchars($row['cableid']) ?><br>
    <strong>Bucket:</strong> <?= htmlspecialchars($row['cablebucket']) ?><br>
    <strong>Status:</strong> <?= htmlspecialchars($row['cablestatus']) ?><br>
    <?= htmlspecialchars($row['cabledesc']) ?><br>
    <img class="barcode" src="barcode.php?id=<?= urlencode($row['cableid']) ?>" alt="Barcode <?= htmlspecialchars($row['cableid']) ?>">
</div>
<?php endwhile; ?>

</body>
</html>
