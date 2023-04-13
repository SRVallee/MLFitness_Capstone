<?php
$id = $_POST['id'];
$id2 = $_POST['id2'];
$apiKey = $_POST['apiKey'];
$rating = $_POST["rating"];

if($id == $id2){
    echo "can't rate yourself";
}else{
    $conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
    $sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
    $res = mysqli_query($conn, $sql);
    if(mysqli_num_rows($res) != 0){

        $sql = "SELECT ratings_amount, rating FROM trainer WHERE trainer_id = ".$id2.";";
        $res = mysqli_query($conn, $sql);
        if(mysqli_num_rows($res) != 0){
            $row = mysqli_fetch_assoc($res);
            if($row["ratings_amount"] == 0){
                $sql = "UPDATE trainer SET ratings_amount = +1, rating = ".$rating." WHERE trainer_id = ".$id2.";";
            }
            else{
                $newRating = ((($row["ratings_amount"] * $row["rating"]) + $rating)/($row["ratings_amount"] + 1));
                $sql = "UPDATE trainer SET ratings_amount = +1, rating = ".$newRating." WHERE trainer_id = ".$id2.";";
            }
            $result = array("status" => "success");
        }else{                          
            $result = array("status" => "Failed to rate");
        }
    }else{
        $result = array("status" => "Denied");
    }
}
    
echo json_encode($result, JSON_PRETTY_PRINT);