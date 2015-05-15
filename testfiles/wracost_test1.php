<?php

if (!file_exists("blockage")){
    file_put_contents(rand(),"Hello World. Testing!");
	$i = 1000;
	while (--$i) echo $i; // Simulating big things happening in the server
    file_put_contents("blockage", "blockedfuckit");
}else{
    echo "You dun goofed";
}

?>
