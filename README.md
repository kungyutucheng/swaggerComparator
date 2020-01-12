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

9003:
```
@ApiOperation(value = "新增的api")
@PostMapping(value = "/add-api")
public void addApi() {

}
```
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
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-add-method.jpg)

9002:
```
@ApiOperation(value = "旧有api新增method")
@GetMapping(value = "/add-method")
public void addMethod() {

}
```

9003:
```
@ApiOperation(value = "旧有api新增method")
@RequestMapping(value = "/add-method", method = {RequestMethod.POST, RequestMethod.GET})
public void addMethod() {

}
```

###### 旧有api删除method
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-delet-method.jpg)

9002:
```
@ApiOperation(value = "旧有api删除method")
@RequestMapping(value = "/delete-method", method = {RequestMethod.GET, RequestMethod.POST})
public void deleteMethod() {

}
```

9003:
```
@ApiOperation(value = "旧有api删除method")
@RequestMapping(value = "/delete-method", method = {RequestMethod.GET})
public void deleteMethod() {

}
```

###### 修改method的tags
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-tags.jpg)

9002:
```
@ApiOperation(value = "修改method的tags", tags = {"旧tag"})
@PostMapping(value = "/modify-method-tag")
public void modifyMethodTag() {

}
```

9003:
```
@ApiOperation(value = "修改method的tags", tags = {"新tag"})
@PostMapping(value = "/modify-method-tag")
public void modifyMethodTag() {

}
```

###### 修改接口描述
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-value.jpg)

9002:
```
@ApiOperation(value = "修改前接口描述")
@PostMapping(value = "/modify-method-value")
public void modifyMethodValue() {

}
```

9003:
```
@ApiOperation(value = "修改后接口描述")
@PostMapping(value = "/modify-method-value")
public void modifyMethodValue() {

}
```

###### 修改请求参数报文格式
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-consumes.jpg)

9002:
```
@ApiOperation(value = "修改请求参数报文格式", consumes = MediaType.APPLICATION_PDF_VALUE)
@PostMapping(value = "/modify-method-consumes")
public void modifyMethodConsumes() {

}
```

9003:
```
@ApiOperation(value = "修改请求参数报文格式", consumes = MediaType.APPLICATION_JSON_VALUE)
@PostMapping(value = "/modify-method-consumes")
public void modifyMethodConsumes() {

}
```

###### 修改响应参数报文格式
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-produces.jpg)

9002:
```
@ApiOperation(value = "修改响应参数报文格式", produces = MediaType.APPLICATION_PDF_VALUE)
@PostMapping(value = "/modify-method-produces")
public void modifyMethodProduces() {

}
```

9003:
```
@ApiOperation(value = "修改响应参数报文格式", produces = MediaType.APPLICATION_JSON_VALUE)
@PostMapping(value = "/modify-method-produces")
public void modifyMethodProduces() {

}
```

###### 修改接口备注
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-desc.jpg)

9002:
```
@ApiOperation(value = "修改接口备注", notes = "修改前备注")
@PostMapping(value = "/modify-method-desc")
public void modifyMethodDesc() {

}
```

9003:
```
@ApiOperation(value = "修改接口备注", notes = "修改后备注")
@PostMapping(value = "/modify-method-desc")
public void modifyMethodDesc() {

}
```

###### 修改响应：基本类型-基本类型
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-base-type.jpg)

9002:
```
@ApiOperation(value = "修改响应：基本类型-基本类型")
@PostMapping(value = "/modify-method-response-base-type")
public Integer modifyMethodResponseBaseType() {
    return 1;
}
```

9003:
```
@ApiOperation(value = "修改响应：基本类型-基本类型")
@PostMapping(value = "/modify-method-response-base-type")
public String modifyMethodResponseBaseType() {
    return UUID.randomUUID().toString();
}
```
