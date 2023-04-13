<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$workout_id["workout_id"];
$feedback["feedback"];

$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT user_id, api_key, is_trainer from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $row = mysqli_fetch_assoc($res);
    if($row["is_trainer"] == 1){
        $sql = "SELECT feedback_id FROM feedback WHERE workout_workout_id = ".$workout_id.";";
        $res = mysqli_query($conn, $sql);
        if(mysqli_num_rows($res) != 0){
            $sql = "UPDATE feedback SET trainer_trainer_id = ".$id.", feedback = ".$feedback.", date = '".date('Y-m-d')."';";
            $res = mysqli_query($conn, $sql);
            echo "success";
        }else{
            $sql = "INSERT INTO feedback(workout_workout_id, feedback, date, trainer_trainer_id) values(".$workout_id.", '".$feedback."', '".date('Y-m-d')."', ".$id.");";
        }
    }else{
        echo "Denied: Not a trainer";
    }
}else{
    echo "Denied";
}