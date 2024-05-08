# iaklogger
## A (very) simple logger for python. 

Nothing fancy, basic functionality to start working right ahead. 
Some examples below to understand the usage:

### EXAMPLE 1: Printing by default
```python
import iaklogger as lg

lg.log("Hi! I'm Default, This prints by default")
```
output:
```
Hi! I'm Default, This prints by default
```

### EXAMPLE 2: Printing by tag
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "Welcome"]

lg.log("Hi!, I'm Iakl! This prints if tags 'IAKL' and 'Welcome' are allowed.", tags=["IAKL", "Welcome"])
```
output:
```
Hi!, I'm Iakl! This prints if tags 'IAKL' and 'Welcome' are allowed
```

### EXAMPLE 3: Filtering messages
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "Welcome"]

lg.log("Hi Iakl!, I'm Losa! This will not print because tag 'LOSA' is not allowed, sadly", tags=["LOSA", "Welcome"])
```
output (blank):
```
```
### EXAMPLE 4: Adding more tags
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "Welcome", "LOSA"]

lg.log("Let's allow tag 'LOSA' so Losa can talk too!", tags=["IAKL", "Welcome"])

lg.log("Oh, It works!, but, how do we know now who is talking?", tags=["LOSA", "Welcome"])
```
output:
```
Let's allow tag 'LOSA' so Losa can talk too!
Oh, It works!, but, how we know now who is talking?
```

### EXAMPLE 5: Showing tags
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "Welcome", "LOSA"]
lg.OPTIONS.show_tags = True

lg.log("Lets show the tags!", tags=["IAKL", "Welcome"])
lg.log("Nice!", tags=["LOSA", "Welcome"])
lg.log("Nice!")

```
output:
```
[IAKL-Welcome] Lets show the tags!
[LOSA-Welcome] Nice!
[DEFAULT] Nice!
```

### EXAMPLE 6: Filtering Default tag
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "Welcome", "LOSA"]
lg.OPTIONS.show_tags = True
lg.OPTIONS.mute_default = True

lg.log("Now Default can't interrupt", tags=["IAKL", "Welcome"])
lg.log("Nice!", tags=["LOSA", "Welcome"])
lg.log("Hey!")

```
output:
```
[IAKL-Welcome] Now Default can't interrupt
[LOSA-Welcome] Nice!
```

### EXAMPLE 7: More Filtering tags 
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "Welcome", "LOSA"]
lg.OPTIONS.show_tags = True

lg.log("No more Welcome tags!", tags=["IAKL", "Welcome"])

lg.OPTIONS.allowed_tags = ["IAKL", "LOSA"]

lg.log("Ok!", tags=["LOSA", "Welcome"])
lg.log("Hey!", tags=["LOSA", "Welcome"])
lg.log("Yes!")

```
output:
```
[IAKL-Welcome] No more Welcome tags!
[DEFAULT] Yes!
```

### EXAMPLE 8: Muting all tags
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "LOSA"]
lg.OPTIONS.show_tags = True

lg.log("Hi Iakl, Hi Losa")
lg.log("Hi Default, Hi Losa", tags=["IAKL"])
lg.log("Hi Default, Hi Iakl", tags=["LOSA"])

lg.OPTIONS.mute_all = True

lg.log("Do you hear me?")
lg.log("I can't hear you!", tags=["IAKL"])
lg.log("Is any one out there?", tags=["LOSA"])

```
output:
```
[DEFAULT] Hi Iakl, Hi Losa
[IAKL] Hi Default, Hi Losa
[LOSA] Hi Default, Hi Iakl
```

### EXAMPLE 8: Save log to file and show current time
```python
import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "LOSA"]
lg.OPTIONS.show_tags = True
lg.OPTIONS.log_file = "log.txt"

lg.log("Hi everyone, I will record this conversation")
lg.log("Hi Default, Ok", tags=["IAKL", "CONVERSATION"])
lg.log("Hi Default, Ok for me too", tags=["LOSA", "CONVERSATION"])

lg.OPTIONS.allowed_tags = ["IAKL", "LOSA", "CONVERSATION"]
lg.OPTIONS.show_time = True

lg.log("Ok Iakl, you start")
lg.log("No no, you Losa", tags=["IAKL", "CONVERSATION"])
lg.log("Why me? you Default", tags=["LOSA", "CONVERSATION"])

```
output (stdout and log.txt):
```
[DEFAULT] Hi everyone, I will record this conversation
2024-03-07 11:11:11 [DEFAULT] Ok Iakl, you start
2024-03-07 11:11:11 [IAKL-CONVERSATION] No no, you Losa
2024-03-07 11:11:11 [LOSA-CONVERSATION] Why me? you Default
```

### EXAMPLE 9: Other options
```python
import iaklogger as lg

# maximum log file size in mb (Default = 10 mb)
lg.OPTIONS.log_file_max_size_mb = 5
```
## License

MIT
