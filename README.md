# WRACOST

### Usage
* Please take 1 minute to read the help command: **python wracost.py --help**
![WRACOST Help Command](https://raw.githubusercontent.com/n30m1nd/WRACOST/master/wracost_help.jpg)
* Also check the Test Cases below
  * *Note: These test cases use files to store data and/or block incoming requests instead of a database registry. It's left for the user to imagine that those "back-end" functionalities could be triggered by anything, not just files.*

#### Test Case 1
* Suggested command for Test Case 1:
  * `python wracost.py http://localhost:80//testcases/wracost_test_1.php HEAD -t 20`
* Why and How **The Race Condition** happens:
  * After the first request, the server tries to block incoming requests by checking if a file under the name **blockage** is present in the server. If not, it will create it. It's this process of accessing to disk which adds to the race condition since *it takes more time for the server to write to disk than to process incoming requests*.
* What it does:
  * Makes 20 concurrent (at the same time) http `HEAD` requests to the given url.
* What to expect:
  * Should create near to 20 files in the same folder as the test file with a name like *RaceConditionFileN{random_number}*
* Explanation of the command: 
  * `HEAD`: This tells WRACOST what kind of HTTP request we are going to make. This is the first mandatory and positional argument.
  * `-t 20`: Tells to make 20 concurrent requests. `-t` stands for threads. This is an "optional" argument, meaning that if you don't use `-t` you'd have to specify other arguments that will help WRACOST calculate how many concurrent requests we're making.

#### Test Case 2:
* Suggested command for Test Case 2:
  * `wracost.py http://localhost:80/testcases/wracost_test_2.php POST -p band -y 0:opt1 0:opt2 0:opt2 0:opt3`
* Why and How **The Race Condition** happens: 
  * As in Test Case 1, if a file under the name **localhost** is present it will block incoming vote requests. Here we can also check that we could be messing up the voting system since it all is accessing the same file because we're triggering a **race condition** inside the `file_put_contents` php function since all the requests are trying to access the same file at the same time and trying to write in it. Note that this could be fixed with the LOCK_EX option in the php function.
* What it does:
  * Makes 4 concurrent and different `POST` requests, each with a different value (`opt1`, `opt2`, ...) for the parameter `band`.
* What to expect:
  * In the file called **localhost** in the server, in the same folder as the Test Case 2
* Explanation of the command:
  * `POST`: Tells WRACOST to make a POST request First mandatory and positional argument.
  * `-p band`: Is the `POST` parameter where we want to inject our payloads.
  * `-y`: Here we specify the payloads and their positions to be injected
    * `0`: Means, for the payload in position 0 (in our case we only have one param so `0` is the `band` param
    * `opt1`: Is the payload to inject into that position.

