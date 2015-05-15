<?php

if (!file_exists("blockage")){
    file_put_contents(rand(),"Testing");
	$i = 1000;
	while (--$i) echo $i; // Simulating big things happening on the server
    file_put_contents("blockage", "blocked");
}else{
    echo "You dun goofed";
}

?>
