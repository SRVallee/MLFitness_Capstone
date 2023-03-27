<?php

$user_id = (int)$_POST["id"];
$apiKey = $_POST["api_key"];
$workout_name = $_POST["workout_name"];
$important_angles = $_POST["important_angles"];
//$increase
$demo = $_POST["demo"];
$exclude_angles = $_POST["excluded_angles"];
$videos = $_POST["videos"];
$description = $_POST["description"];
$model_location = "wherever that is";
$type = $_POST["type"]; //if type is default or trainer owned


$conn = mysqli_connect("localhost", "root", "MLFitness@123", "ml_fitness"); //connect
$sql = "SELECT * from user where (user_id = '".$id."' and api_key = '".$apiKey."')";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $row = mysqli_fetch_assoc($res);
    if ($type == "default"){
        $sql = "INSERT INTO exercise(exercise, demo_location, model_location, notes) values('".$workout_name."',".$demo.", '".$model_location."','".$description."');";
        $res = mysqli_query($conn, $sql); 
    }else if($row["is_trainer"] == 1){
        $sql = "INSERT INTO exercise(exercise, demo_location, model_location, notes, trainer_trainer_id) values('".$workout_name."',".$demo.",'".$model_location."','".$description."', ".$user_id.");";
        $res = mysqli_query($conn, $sql); 
    }else{
        echo "action not allowed";
    }
    
}

