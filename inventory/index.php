<?php
include "db.php";

$where = [];
$params = [];

if (!empty($_GET['bucket'])) {
    $where[] = "cablebucket = ?";
    $params[] = $_GET['bucket'];
}

if (!empty($_GET['id'])) {
    $where[] = "cableid = ?";
    $params[] = $_GET['id'];
}

if (!empty($_GET['desc'])) {
    $where[] = "cabledesc LIKE ?";
    $params[] = "%" . $_GET['desc'] . "%";
}

$sql = "SELECT * FROM cables";
if ($where) {
    $sql .= " WHERE " . implode(" AND ", $where);
}

$stmt = $conn->prepare($sql);

if ($params) {
    $types = str_repeat("s", count($params));
    $stmt->bind_param($types, ...$params);
}

$stmt->execute();
$result = $stmt->get_result();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Cable Inventory</title>
    <style>
        body { font-family: Arial; background:#f4f4f4; }
        table { border-collapse: collapse; width:100%; background:white; }
        th, td { border:1px solid #ccc; padding:8px; text-align:left; }
        th { background:#222; color:white; }
        a { text-decoration:none; }
        .box { background:white; padding:15px; margin-bottom:15px; }
    </style>
</head>
<body>

<h1>Cable Inventory</h1>

<div class="box">
    <a href="create.php">➕ Add New Cable</a>
</div>

<div class="box">
    <form method="get">
        <strong>Search</strong><br><br>
        Cable ID:
        <input type="number" name="id">

        Description:
        <input type="text" name="desc">

        Bucket:
        <select name="bucket">
            <option value="">-- all --</option>
            <option>audio</option>
            <option>usb</option>
            <option>power</option>
            <option>gear</option>
            <option>circuits</option>
        </select>

        <button type="submit">Search</button>
        <a href="index.php">Reset</a>
    </form>
</div>

<table>
<tr>
    <th>ID</th>
    <th>Type</th>
    <th>Bucket</th>
    <th>Description</th>
    <th>Status</th>
    <th>Action</th>


</tr>
<a href="print_all.php?<?= http_build_query($_GET) ?>" target="_blank">🖨 Print All</a>
|
<a href="print.php?<?= http_build_query($_GET) ?>" target="_blank">
📄 Print All With Barcodes
</a>

<?php while ($row = $result->fetch_assoc()): ?>
<tr>
    <td><?= $row['cableid'] ?></td>
    <td><?= $row['cabletype'] ?></td>
    <td><?= $row['cablebucket'] ?></td>
    <td><?= htmlspecialchars($row['cabledesc']) ?></td>
    <td><?= $row['cablestatus'] ?></td>
    <td><a href="edit.php?id=<?= $row['cableid'] ?>">✏️ Edit</a></td>
</tr>
<?php endwhile; ?>

</table>

</body>
</html>
