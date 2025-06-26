# Alembic 使用教程

> 官方文档：https://hellowac.github.io/alembic-doc-zh/zh/_front_matter.html
## 1. 创建迁移脚本
在修改模型后，生成迁移脚本：

```bash
alembic revision --autogenerate -m "描述你的变更"

如: 
alembic revision --autogenerate -m "Create table xxx"
```

这会在 `alembic/versions/` 目录下创建一个新的迁移脚本。


生成的迁移文件包括一个upgrade和一个downgrade函数
你需要在这两个函数中添加数据库表的创建和删除操作（如果使用了--autogenerate 参数，则会依据Model的定义自动生成）


## 2. 应用迁移
将迁移应用到数据库：

```bash
# 升级到最新版本
alembic upgrade head

# 升级到特定版本
alembic upgrade <revision_id>

# 降级一个版本
alembic downgrade -1
```

运行一下 `alembic upgrade head`

就可以新增一个数据表 并更新到最新版本

## 3. 管理迁移
常用命令：

```bash
# 查看当前数据库版本
alembic current

# 查看迁移历史
alembic history --verbose

# 标记为已应用(不执行迁移)
alembic stamp <revision>
```

这样设置后，你就可以使用 Alembic 来管理数据库架构变更了。

