<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$exercise_id = $_POST["exercise_id"];
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT * from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $sql = "SELECT * FROM exercise WHERE exercise_id = ".$exercise_id.";";
    $res = mysqli_query($conn, $sql);
    if(mysqli_num_rows($res) != 0){
        $row = mysqli_fetch_assoc($res);
    
        $result = array("status" => "success", 
        "name" => $row["exercise"],
        "description" => $row["notes"],
        "trainer_id" => $row["trainer_trainer_id"]);
    }else{
        $result = array("status" => "Exercise not found");
    }
}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);