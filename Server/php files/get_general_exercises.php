<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$exercise_id["exercise_id"];
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT * from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $sql = "SELECT * FROM exercise WHERE trainer_trainer_id = null;";
    $res = mysqli_query($conn, $sql);
    $array = array();
    while($row = mysqli_fetch_assoc($res)){
        $array[] = $row["exercise_id"];
    }
    $result = array("status" => "success", "exercises" => $array);
}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);