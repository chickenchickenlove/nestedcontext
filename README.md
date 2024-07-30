### How to test?
- Please ensure that server(`/src/main/java/org/example/Main.java`) is running.
- Then, execute test script below.

```shell
$ cd pytest 
$ pip install -r requirements.txt
$ py.test my_test.py

=============================================================================== test session starts ===============================================================================
platform darwin -- Python 3.9.13, pytest-7.2.0, pluggy-1.4.0
rootdir: ...
plugins: asyncio-0.20.3
asyncio: mode=strict
collected 21 items                                                                                                                                                                

my_test.py .....................                                                                                                                                           [100%]

=============================================================================== 21 passed in 0.43s ================================================================================
```
