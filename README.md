# swaggerComparator

## 简介
众所周知，swagger生成的接口数据是没有修订记录的，只会显示最终修改完成的版本，利用此项目，再搭配俩个不同接口版本的运行环境，即可生成前后俩个版本的接口修订记录

## 原理
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-theory.png)

## json结构

### swagger

###### 修改host

![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-host.jpg)

###### 修改上下文
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-basepath.jpg)

###### 增加api
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-add-api.jpg)

###### 删除api
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-delete-api.jpg)

9002
```
@ApiOperation(value = "删除api")
@PostMapping(value = "/delete-api")
public void deleteApi() {

}
```

###### 旧有api新增method
