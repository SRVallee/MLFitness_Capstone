<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT * from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $sql = "SELECT trainer_id from trainer;";
    $res = mysqli_query($conn, $sql);
    $array = [];
    for ($i = 0; $i < mysqli_num_rows($res); $i +=1){
        $row = mysqli_fetch_assoc($res);
        $array += $row["trainer_id"];
    }
    $result = array("status" => "success", "trainers" => $array);
}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);