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
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-delete-method.jpg)

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

###### 修改响应：list中的类型
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-list-type.jpg)

9002:
```
@ApiOperation(value = "修改响应：list中的类型")
@PostMapping(value = "/modify-method-response-list-type")
public List<Integer> modifyMethodResponseListType() {
    return Arrays.asList(1);
}
```

9003:
```
@ApiOperation(value = "修改响应：list中的类型")
@PostMapping(value = "/modify-method-response-list-type")
public List<String> modifyMethodResponseListType() {
    return Arrays.asList(UUID.randomUUID().toString());
}
```

###### 修改响应：set中的类型
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-set-type.jpg)

9002:
```
@ApiOperation(value = "修改响应：set中的类型")
@PostMapping(value = "/modify-method-response-set-type")
public Set<Integer> modifyMethodResponseSetType() {
    Set<Integer> set = new HashSet<>();
    return set;
}
```

9003:
```
@ApiOperation(value = "修改响应：set中的类型")
@PostMapping(value = "/modify-method-response-set-type")
public Set<String> modifyMethodResponseSetType() {
    Set<String> set = new HashSet<>();
    return set;
}
```

###### 修改响应：集合类型-基本类型
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-collection-to-base.jpg)

9002:
```
@ApiOperation(value = "修改响应：集合类型-基本类型")
@PostMapping(value = "/modify-method-response-collection-to-base")
public List<Integer> modifyMethodResponseCollectionToBase() {
    List<Integer> list = Arrays.asList(1);
    return list;
}
```

9003:
```
@ApiOperation(value = "修改响应：集合类型-基本类型")
@PostMapping(value = "/modify-method-response-collection-to-base")
public String modifyMethodResponseCollectionToBase() {
    return UUID.randomUUID().toString();
}
```

###### 修改响应：对象类型中添加字段
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-object-add-field.jpg)

9002:
```
@ApiOperation(value = "修改响应：对象类型中添加字段")
@PostMapping(value = "/modify-method-response-object-add-field")
public AddFieldResponse modifyMethodResponseObjectAddField() {
    return new AddFieldResponse();
}
```

9003:
```
@ApiOperation(value = "修改响应：对象类型中添加字段")
@PostMapping(value = "/modify-method-response-object-add-field")
public AddFieldResponse modifyMethodResponseObjectAddField() {
    return new AddFieldResponse();
}
```

###### 修改响应：对象类型中删除字段
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-object-delete-field.jpg)

9002:
```
@ApiOperation(value = "修改响应：对象类型中删除字段")
@PostMapping(value = "/modify-method-response-object-delete-field")
public DeleteFieldResponse modifyMethodResponseObjectDeleteField() {
    return new DeleteFieldResponse();
}
```

9003:
```
@ApiOperation(value = "修改响应：对象类型中删除字段")
@PostMapping(value = "/modify-method-response-object-delete-field")
public DeleteFieldResponse modifyMethodResponseObjectDeleteField() {
    return new DeleteFieldResponse();
}
```

###### 修改响应：对象类型中修改字段定义
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-object-modify-field-value.jpg)

9002:
```
@ApiOperation(value = "修改响应：对象类型中修改字段定义")
@PostMapping(value = "/modify-method-response-object-modify-field-value")
public ModifyFieldValueResponse modifyMethodResponseObjectModifyFieldValue() {
    return new ModifyFieldValueResponse();
}
```

9003:
```
@ApiOperation(value = "修改响应：对象类型中修改字段定义")
@PostMapping(value = "/modify-method-response-object-modify-field-value")
public ModifyFieldValueResponse modifyMethodResponseObjectModifyFieldValue() {
    return new ModifyFieldValueResponse();
}
```

###### 修改响应：对象类型中修改字段类型：基本-基本
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-object-modify-field-type.jpg)

9002:
```
@ApiOperation(value = "修改响应：对象类型中修改字段类型：基本-基本")
@PostMapping(value = "/modify-method-response-object-modify-field-type")
public ModifyFieldTypeResponse modifyMethodResponseObjectModifyFieldType() {
    return new ModifyFieldTypeResponse();
}
```

9003:
```
@ApiOperation(value = "修改响应：对象类型中修改字段类型：基本-基本")
@PostMapping(value = "/modify-method-response-object-modify-field-type")
public ModifyFieldTypeResponse modifyMethodResponseObjectModifyFieldType() {
    return new ModifyFieldTypeResponse();
}
```

###### 修改响应：对象类型中修改字段允许输入的值范围
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-object-modify-field-allow-values.jpg)

9002:
```
@ApiOperation(value = "修改响应：对象类型中修改字段允许输入的值范围")
@PostMapping(value = "/modify-method-response-object-modify-field-allow-values")
public ModifyFieldAllowValuesResponse modifyMethodResponseObjectModifyFieldAllowValue() {
    return new ModifyFieldAllowValuesResponse();
}
```

9003:
```
@ApiOperation(value = "修改响应：对象类型中修改字段允许输入的值范围")
@PostMapping(value = "/modify-method-response-object-modify-field-allow-values")
public ModifyFieldAllowValuesResponse modifyMethodResponseObjectModifyFieldAllowValues() {
    return new ModifyFieldAllowValuesResponse();
}
```

###### 修改响应：对象类型中修改字段必填属性
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-object-modify-field-required.jpg)

9002:
```
@ApiOperation(value = "修改响应：对象类型中修改字段必填属性")
@PostMapping(value = "/modify-method-response-object-modify-field-required")
public ModifyFieldRequiredResponse modifyMethodResponseObjectModifyFieldRequired() {
    return new ModifyFieldRequiredResponse();
}
```

9003:
```
@ApiOperation(value = "修改响应：对象类型中修改字段必填属性")
@PostMapping(value = "/modify-method-response-object-modify-field-required")
public ModifyFieldRequiredResponse modifyMethodResponseObjectModifyFieldRequired() {
    return new ModifyFieldRequiredResponse();
}
```

###### 修改响应：对象类型中修改字段输出例子
![image](https://github.com/kungyutucheng/swaggerComparator/blob/master/resources/images/swagger-diff-modify-method-response-object-modify-field-example.jpg)

9002:
```
@ApiOperation(value = "修改响应：对象类型中修改字段输出例子")
@PostMapping(value = "/modify-method-response-object-modify-field-example")
public ModifyFieldExampleResponse modifyMethodResponseObjectModifyFieldExample() {
    return new ModifyFieldExampleResponse();
}
```

9003:
```
@ApiOperation(value = "修改响应：对象类型中修改字段输出例子")
@PostMapping(value = "/modify-method-response-object-modify-field-example")
public ModifyFieldExampleResponse modifyMethodResponseObjectModifyFieldExample() {
    return new ModifyFieldExampleResponse();
}
```
