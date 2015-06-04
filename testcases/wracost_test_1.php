<?php

/********************************************************************
 * Test 1: Race condition met when writing to disk.          *
 * ---------------------------------------------------------------- *
 * This test will try to write to disk unless blockfile is present  *
 * a file called "blockage".                                        *
 *                                                                  *
 * WRACOST Testing command:                                         *
 * wracost.py http://localhost:80//testcases/wracost_test_1.php     *
 *                                                       HEAD -t 20 *
 ********************************************************************
 */
$data_folder = "./data/test1_hd_write/"

if (!file_exists($data_folder."blockage")){
    file_put_contents($data_folder."RaceConditionFileN".rand(),"Testing");
	$i = 1000;
	while (--$i) echo $i; // Simulating big things happening on the server
    file_put_contents($data_folder."blockage", "blocked");
}else{
    echo "Nope";
}

?>
