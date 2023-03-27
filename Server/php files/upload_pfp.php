<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$conn = mysqli_connect("localhost", "root", "MLFitness@123", "ml_fitness"); //connect
$sql = "SELECT * from user where (user_id = '".$id."' and api_key = '".$apiKey."')";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $row = mysqli_fetch_assoc($res);    
    if(!empty($_POST['image'])){
        if(file_put_contents('pfps/'.$_POST['id'].'.jpg', base64_decode($_POST['image']))){
            echo "success";
        }else{
	    echo "Failed to save image";
	}
    }else{
        echo "No Image";
    }
}else{
    echo "An Error Ocurred";
}