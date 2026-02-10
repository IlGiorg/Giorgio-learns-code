<?php
include "db.php";

$where = [];
$params = [];

if (!empty($_GET['bucket'])) {
    $where[] = "cablebucket = ?";
    $params[] = $_GET['bucket'];
}

$sql = "SELECT * FROM cables";
if ($where) {
    $sql .= " WHERE " . implode(" AND ", $where);
}

$stmt = $conn->prepare($sql);
if ($params) {
    $stmt->bind_param("s", ...$params);
}
$stmt->execute();
$result = $stmt->get_result();
?>

<!DOCTYPE html>
<html>
<head>
<title>Print Cables</title>
<style>
body { font-family: Arial; }
.item { margin-bottom: 20px; }
</style>
</head>

<body onload="window.print()">

<h2>Cable Inventory</h2>

<?php while ($row = $result->fetch_assoc()): ?>
<div class="item">
    <strong>ID:</strong> <?= $row['cableid'] ?><br>
    <strong>Bucket:</strong> <?= $row['cablebucket'] ?><br>
    <strong>Status:</strong> <?= $row['cablestatus'] ?><br>
    <?= htmlspecialchars($row['cabledesc']) ?>
</div>
<hr>
<?php endwhile; ?>

</body>
</html>
