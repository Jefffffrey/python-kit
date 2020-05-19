# QPS 测试

## 并发为1

一个进程一直循环调用N次取平均值

取1次，取10次，取100次，去1000次发现值越来越高，感觉不是很合理，因为是单线程，分析出原因如下：

1. 没有预热，数据库没准备好相关的缓存之类的
2. Python代码有的代码执行次数越多越快，推测是指令缓存之类的

同时测试的时候需要尽量减少Python代码本身的性能损耗，比如拼接字符串使用join比+和format快，另外需要注意到不使用SQL_NO_CACHE，更加符合真实情况


| SQL                                                  | QPS            |
| ---------------------------------------------------- | -------------- |
| select  emp_no from `employees` where emp_no = 30000 | 6000           |
| select * from `employees` where emp_no = 30000       | 5000           |
| select * from `employees` where emp_no = {}          | 5000(差别不大) |

上面的测试中第三个SQL更加符合真实的情况，因此其余测试都以这个为基准

测试环境：
Intel(R) Core(TM) i9-9880H CPU @ 2.30GHz 8核16线程

换做MySQLDb后，第三个的QPS达到了11K

猜测：
最高大约11000*8*1.3 ~ 110K QPS

结果只有40K.

MySQL 40K
Redis 80K

https://www.simform.com/mongodb-vs-mysql-databases/ MongoDB的不准，MySQL比较准
MongoDB 20K


