<?php
$pdo = new PDO(
    "mysql:host=sql113.infinityfree.com;dbname=if0_41226934_gossipdb;charset=utf8",
    "if0_41226934",
    "bathrooM09"
);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$message = "";

/* =======================
   AJAX PERSON SEARCH
======================= */
if(isset($_GET['ajax_search'])){
    $search = "%".$_GET['ajax_search']."%";
    $stmt = $pdo->prepare("SELECT personid, name, surname FROM people WHERE name LIKE ? OR surname LIKE ? LIMIT 10");
    $stmt->execute([$search,$search]);
    echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
    exit;
}

/* =======================
   ADD PERSON
======================= */
if(isset($_POST['add_person'])){
    $stmt = $pdo->prepare("INSERT INTO people (name, surname, dob, address, history) VALUES (?, ?, ?, ?, ?)");
    $stmt->execute([
        $_POST['name'],
        $_POST['surname'],
        $_POST['dob'],
        $_POST['address'],
        $_POST['history']
    ]);
    $message = "✅ Person added successfully.";
}

/* =======================
   ADD RELATIONSHIP
======================= */
if(isset($_POST['add_relationship'])){
    if($_POST['person1'] == $_POST['person2']){
        $message = "❌ Cannot relate a person to themselves.";
    } else {
        $stmt = $pdo->prepare("
            INSERT INTO relationships
            (person1, person2, start_date, end_date, relstage, relquicknotes, relhistory, relknown)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ");
        $stmt->execute([
            $_POST['person1'],
            $_POST['person2'],
            $_POST['start_date'],
            $_POST['end_date'],
            $_POST['relstage'],
            $_POST['relquicknotes'],
            $_POST['relhistory'],
            isset($_POST['relknown']) ? 1 : 0
        ]);
        $message = "✅ Relationship added.";
    }
}

/* =======================
   ADD GOSSIP
======================= */
if(isset($_POST['add_gossip'])){
    $stmt = $pdo->prepare("
        INSERT INTO gossip_entries (personid, title, content, gossip_date, visibility)
        VALUES (?, ?, ?, ?, ?)
    ");
    $stmt->execute([
        $_POST['gossip_personid'],
        $_POST['title'],
        $_POST['content'],
        $_POST['gossip_date'],
        $_POST['visibility']
    ]);
    $message = "✅ Intel added.";
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Add New Intel</title>
<style>
body { font-family: Arial; margin:40px; }
.card { border:1px solid #ccc; padding:20px; margin-bottom:30px; border-radius:8px; }
input, textarea { width:100%; padding:8px; margin:5px 0 15px 0; }
button { padding:8px 15px; }
.results { border:1px solid #ddd; max-height:150px; overflow:auto; }
.result-item { padding:5px; cursor:pointer; }
.result-item:hover { background:#eee; }
.success { color:green; font-weight:bold; }
</style>

<script>
function searchPerson(inputId, hiddenId, resultsId){
    let query = document.getElementById(inputId).value;
    if(query.length < 2) return;

    fetch("?ajax_search=" + encodeURIComponent(query))
    .then(res => res.json())
    .then(data => {
        let results = document.getElementById(resultsId);
        results.innerHTML = "";
        data.forEach(person => {
            let div = document.createElement("div");
            div.className = "result-item";
            div.innerText = person.name + " " + person.surname;
            div.onclick = function(){
                document.getElementById(inputId).value = person.name + " " + person.surname;
                document.getElementById(hiddenId).value = person.personid;
                results.innerHTML = "";
            };
            results.appendChild(div);
        });
    });
}
</script>
</head>
<body>

<h1>🛠 Insider Panel</h1>
<?php if($message) echo "<p class='success'>$message</p>"; ?>

<div class="card">
<h2>Add Person</h2>
<form method="POST">
<input type="text" name="name" placeholder="Name" required>
<input type="text" name="surname" placeholder="Surname" required>
<input type="date" name="dob" placeholder="Date of Birth">
<input type="text" name="address" placeholder="Address">
<textarea name="history" maxlength="511" placeholder="History"></textarea>
<button name="add_person">Add Person</button>
</form>
</div>

<div class="card">
<h2>Add Relationship</h2>
<form method="POST">

<label>Person 1</label>
<input type="text" id="person1_search" onkeyup="searchPerson('person1_search','person1_id','results1')" placeholder="Search person...">
<input type="hidden" name="person1" id="person1_id">
<div id="results1" class="results"></div>

<label>Person 2</label>
<input type="text" id="person2_search" onkeyup="searchPerson('person2_search','person2_id','results2')" placeholder="Search person...">
<input type="hidden" name="person2" id="person2_id">
<div id="results2" class="results"></div>

<input type="date" name="start_date" >
<input type="date" name="end_date">
<input type="text" name="relstage" placeholder="Relationship Stage">
<input type="text" name="relquicknotes" placeholder="Quick Notes">
<textarea name="relhistory" placeholder="Relationship History"></textarea>

<label><input type="checkbox" name="relknown" checked> Publicly Known</label>
<button name="add_relationship">Add Relationship</button>
</form>
</div>

<div class="card">
<h2>Add Intel Entry</h2>
<form method="POST">

<label>Person</label>
<input type="text" id="gossip_search" onkeyup="searchPerson('gossip_search','gossip_id','results3')" placeholder="Search person...">
<input type="hidden" name="gossip_personid" id="gossip_id">
<div id="results3" class="results"></div>

<input type="text" name="title" placeholder="Title" required>
<input type="date" name="gossip_date">
<select name="visibility">
<option value="public">Public</option>
<option value="friends">Friends</option>
<option value="private">Private</option>
</select>
<textarea name="content" placeholder="Content"required></textarea>

<button name="add_gossip">Add Intel</button>
</form>
</div>

</body>
</html>