<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$username = $_POST['username'];
$name = $_POST['name'];
$email = $_POST['email'];        
$isTrainer = $_POST['isTrainer'];
$conn = mysqli_connect("localhost", "root", "MLFitness@123", "ml_fitness"); //connect
$sql = "select * from user where (user_id = '".$id."' and api_key = '".$apiKey."')";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $row = mysqli_fetch_assoc($res);
    if(!empty($_POST['old_password'])){
        if(password_verify($_POST['old_password'], $row["password"])){
	    $newPassword = password_hash($_POST['new_password'], PASSWORD_DEFAULT);
            $sql = "UPDATE user SET username = '".$username."', name = '".$name."', email = '".$email."', password = '".$newPassword."' WHERE user_id = '".$id."';";
            $res = mysqli_query($conn, $sql); 
            echo "success";
        }else{
            echo "Wrong Password";
        }
    }else{
        $sql = "UPDATE user SET username = '".$username."', name = '".$name."', email = '".$email."' WHERE user_id = '".$id."';";
	$res = mysqli_query($conn, $sql); 
	echo "success";
    }
}else{
    echo "An Error Ocurred";
}