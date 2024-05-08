## Get Started

> 走之底[web-cli](https://zzd.show/users/cli/)，本地调用多功能接口

1. 安装`python`
2. 安装本地python包

```sh
pip install zzd
```

3. 之后您应该可以在cli中使用`zzd`

> 这里建议全局安装，您也可以创建venv然后进行安装，但记得通过`source bin/activate`激活虚拟环境

***

## 1. 登录

```sh
zzd login 你的id 你的密匙
```

- 走之底平台登录后，回到此页面生成自己的登录密匙。
- 为了您的账号安全，请不要将此密匙告知他人。

## 2. 退出

```sh
zzd logout
```

- 您本地的电脑将安全退出走之底终端。

> 若这是您的私人电脑，您没必要每次操作都进行登录退出。您可以长时间保持登录状态，若是认为账号有安全隐患，可以前往web端重置密匙，这会使所有客户端cli登录失效。

## 3. 列表

```sh
zzd list
```

> 整理式呈现您最近接触的页面

## 4. 详细数据

```sh
zzd info DEMO
```

> 调取demo详细信息，demo可以是一个链接，也可以是一个序号

## 5. 复制

```sh
zzd clone DEMO
```

> 将demo复制到本地，demo可以是一个链接，也可以是一个序号

## 6. 推进

```sh
zzd push
```

**使用之前，请先`cd`到对应文件目录。**

> 将当前文件夹作为页面，推进到服务器。

1. 若本目录为**复刻的他人的页面**，则创建自己新的页面，保存到服务器，同时将本目录转为自己新的页面。(仍然留有复刻记录，方便您查看初始源)
2. 若本目录为**复制的自己的作品**，则推进更改。
3. 若本目录为**自己本地创建的文件夹**，将会创建新的页面，保存到服务器。

## 文件结构

> 若要直接上传前端静态项目，您的文件结构应该看起来像这样：

```
proj
├── log.json
├── css
│   ├── index.css
│   └── style.css
├── html
│   └── index.html
├── js
│   └── index.js
└── static
    ├── 1.jpg
    └── lib.js
```

#### 文件夹

> 文件夹中只能包含文件，不能包含子文件夹等更复杂的结构

- `html`, `css`, `js` 文件夹中可以包含一个或者多个文件，需是支持的代码格式，如html, pug, haml等
- `static` 可以包含您的其他资源，如图片，视频，字体，或者第三方代码库等等。

#### 上传预处理

- 上传操作有详细的步骤引导，我们依次帮助您处理静态文件，替换内部引用等等。
- 上传过程中我们只需要您的`body`标签内部内容，并且会自动读取您的`html`文件，自动识别cdn并添加。
- 但是若您直接使用了`pug`, `haml`，而项目中不包含`html`文件，很遗憾我们暂无法识别cdn外部链接，请手动在`log.json`中叙述，如：

```json
{"cdns": {
	"css": ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"],
	"js": []
}}
```

- 若使用了任何预处理技术，如`scss`, `typescript`等等，请上传成功后前往web页面进行一次保存，否则可能会导致编译后代码缺失从而无法显示页面。

## `DEBUG`常见问题

1. zsh特殊字符

```sh
zzd clone https://zzd.show/shows/detail/33/#panda-syntax
zsh: bad pattern: https://zzd.show/shows/detail/33/#panda-syntax
```

> zsh把url中常用的#看做标注的开头，因此我们带上url参数时尽量带上双引号

```sh
zzd clone "https://zzd.show/shows/detail/33/#panda-syntax"
```
