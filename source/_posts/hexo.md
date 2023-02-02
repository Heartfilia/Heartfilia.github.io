---
title: 【hexo】从零开始搭建一个博客
date: 2022-12-06 12:27:27
tags: 美化
categories: 教程
toc: true
---

从环境到项目部署成功一个hexo博客的教程~

<!-- more -->

我们这里是讲把项目部署到`github pages` 服务器部署自己搞 很简单的 都一样
我这里是在linux服务器上面弄的，如果你是windows本地弄的话 基本都一样 就是弄git密钥的时候有点差别百度一下就好了


# 一、前期准备
## 1.node
### 1.1 安装
这里没啥好说的，直接去官网下载或者直接用服务器的镜像源的，但是建议-->node版本不要太低了,去官网下载就下载最新的长期支持版本就好了，用服务器源的话最好不要低于10版本，我这里懒得去官网弄，我直接用我服务器的yum源里的nodejs，我的node是12+版本的
### 1.2 注意
因为国内源比较慢，我们这里建议更新一下npm的源，后续下载任务操作会快很多，我这里直接用了`cnpm`的安装源(没有用`cnpm`只是用了他的镜像哈哈)
```bash
npm config set registry https://registry.npmmirror.com
```
配置完后可以查看一下
![查看npm的配置](https://static.litetools.top/blogs/hexo/0.png)
## 2.git
这里是教如何搭建`github pages`并和`hexo`关联
安装git就不用这里教了，网上一大把教程 我这里还是直接  `yum install git`
## 3. 为啥要写这个
**来源于hexo官网下面的评论**
**确实很多地方看着迷迷糊糊的，都是自己去多试试，然后想记录下来**
![官网亮点评论](https://static.litetools.top/blogs/hexo/1.png)
# 二、GithubPages操作
## 1.github设置
在主页这里创建一个仓库 **建议先别创建README 我们就只要一个空仓库，里面会有很多绑定仓库的提示，不会玩的话搞不好会冲突哈哈哈**
![创建github仓库](https://static.litetools.top/blogs/hexo/2.png)
## 2.服务器git配置
### 2.1配置git
我们这里需要配置一下git，我们现在在服务器上面先绑定github啦
```python
git config --global user.name "你gihub的用户名"
git config --global user.email "你gihub的邮箱"

# 然后生成sshkey
ssh-keygen -t rsa -C "你gihub的邮箱"
# 然后把 id_rsa.pub 里面的内容复制出来我们要贴在github里面
cat ~/.ssh/id_rsa.pub
```
登录了github后，在Settings里面找到 `SSH and GPG keys`
然后点击`New SSH key`
标题随便取，我是要做页面的我标注一下 `github.io`  下面的`key`把上面cat出来的内容复制过来粘贴上去除首位空字符
![github密钥](https://static.litetools.top/blogs/hexo/3.png)
然后我们测试一下
`ssh -T git@github.com`
出现了用户名就是ok的，如下
![测试和git的链接](https://static.litetools.top/blogs/hexo/4.png)
### 2.2 如何关联到hexo
这里我们先不描述 上面操作完了后就先等等，我们接下来看看代码那边如何配置先
**这里是后面配置完了再翻回来看这里的**
**等hexo项目创建好了后**，我们根据创建的仓库页面的提示信息 我们在hexo项目里面初始化git
然后把本地的绑定到远程main(老版本可能叫master) 这里就是无脑复制github空白仓库里面的提示信息，以后每次操作前建议先 `git pull` 一下，然后再改文件测试 然后再进行`git`三连

1. git add .       # 因为有`.gitignore`文件 所以我们直接`add .` 
2. git commit -m 提交的信息
3. git push origin main         # 老版本可能叫master  

然后我们在github 我们创建的这个仓库上面点击

1. setttings
2. Pages
3. Branch 这里选择 我们`deploy` 那里填的那个分支，我这里填写的 `pages`

![默认分支情况](https://static.litetools.top/blogs/hexo/5.png)
后面只要`hexo d` 等传输完毕后，github这里会构建，我们可以在 github仓库页面上面的 `Actions`目录下面看到构建的进度
![actions情况](https://static.litetools.top/blogs/hexo/6.png)
**如果这里绿了就可以访问啦～**
是不是很奇怪，这里才是文章的最终结束～
# 三、hexo的启动部署
## 1.安装
我们打开 [hexo官网](https://hexo.io/)，因为开发者是一个台湾人，所以中文支持比较好，可以直接中文阅读网站
直接输入主页给我们的
```python
npm install hexo-cli -g
# 顺道安装一下下面的东西 部署到git要用
npm install hexo-deployer-git --save

# 后面如果要弄live2d啥的还需要装下面的
npm install hexo-deployer-git --save
# 下载 lieve2d模型
npm install --save live2d-widget-model-模型名字
```
### 1.1 模型预览
这里参考可以去这里看看，然后下载自己喜欢的模型就ok了 [模型预览](https://blog.csdn.net/wang_123_zy/article/details/87181892)
我这里用的是 `npm install --save live2d-widget-model-shizuku`
然后在主配置文件下面加上这个就好了， 页面加载这个东西会有点点慢 但是不会太久
```python
live2d:
  enable: true
  scriptFrom: local
  pluginRootPath: live2dw/   # 如果加载有问题可以关闭这个
  pluginJsPath: lib/         # 如果加载有问题可以关闭这个
  pluginModelPath: assets/
  tagMode: false
  debug: false
  model:
    use: live2d-widget-model-shizuku   # 这里换上下载好的模型就好了
  display:
    position: right
    width: 150
    height: 300
  mobile:
    show: false   # 这里一定要关 要不然手机端体验不好
  react:
    opacity: 0.7
```

装完了后 可以在终端测试一下  `hexo version` 查看一下是否正常输出内容，如果ok的话我们进行接下来的操作步骤
## 2.初始化
我们找到一个目录里面就专门放以后存放的各种博客网站，**不找目录**直接在 `~`目录下也可以操作
`hexo init myBlogs`这样会初始化一个`myBlogs`目录出来，这里的名称随意
我是**自己创建了一个blogs父目录**，然后在里面init项目，这样子方便多个项目管理好看
![初始化目录](https://static.litetools.top/blogs/hexo/7.png)
**上面操作在配置了前期准备里面换源后是会比较快完成**
![当前目录文件](https://static.litetools.top/blogs/hexo/8.png)
然后进入我们刚才init好的项目这里我进入`cd myBlogs`,然后执行 `npm install`即可
后续页面有改动那些，可以先使用`hexo cl`清理之前的缓存然后再执行下面的操作
然后`hexo g` 计算一下文件
然后`hexo server -p 80`在80端口开启一个服务
最后我们直接浏览器输入ip访问一下，看看是不是会出来如下一个页面
测试完没有问题可以直接`ctrl + c`停止服务
![大概情况](https://static.litetools.top/blogs/hexo/9.png)
如果到这里都可以，那么最基础的搭建已经完成了，接下来就是 `美化`及 `日常更新`了
## 3. 美化
### 3.1 挑选主题
我们去[这里](https://hexo.io/themes/)挑选喜欢的主题
**我这里选择的是 **[ParticleX](https://github.com/argvchs/hexo-theme-particlex)

再推荐两个好看的主题 后面我也要换一下
> [https://github.com/Candinya/Kratos-Rebirth](https://github.com/Candinya/Kratos-Rebirth)  (目前我用的这个这个好看)
> [https://github.com/tangyuxian/hexo-theme-tangyuxian](https://github.com/tangyuxian/hexo-theme-tangyuxian)
> [https://github.com/auroral-ui/hexo-theme-aurora](https://github.com/auroral-ui/hexo-theme-aurora)

### 3.2 下载主题
按照github页面介绍 我们在**主题目录下**执行命令
```bash
git clone https://github.com/argvchs/hexo-theme-particlex.git themes\particlex
```
![下载主题位置](https://static.litetools.top/blogs/hexo/10.png)
然后返回项目主目录 我这里的 `/root/blogs/myBlogs`下面找到 `_config.yml`我们进行一些基础的配置，后面还有主题的配置我们单独再说
### 3.3 项目配置文件
#### > 一些描述信息
注意下面是yaml文件，`:`后面必须要空格, 单引号可写可不写
```python
# 我没有单独写的都是用默认值就好了 

title: HeartfiliaのBlogs # 标题
subtitle: 个人博客啦 # 副标题
description: 往下滑动可以浏览更多啦~ # 描述
keywords: # 关键字
author: Lodge Heartfilia # 作者
language: zh # 语言
timezone: 'Asia/Shanghai' # 时区

url: https://heartfilia.github.io # 网址
root: # 根目录 这里注意 这里要是写错了可能网站访问不到 默认即可 有需要再调整
permalink: # 文章链接格式
permalink_defaults: # 链接默认值
source_dir: # 源文件夹，内容的存储位置
public_dir: # 公用文件夹，静态文件的生成位置
tag_dir: # 标签目录
archive_dir: # 存档目录
category_dir: # 分类目录
skip_render: # 复制到原始路径，不进行渲染
new_post_name: # 新帖子的文件名格式
titlecase: # 将标题转换为小写1/大写2 *
external_link.enable: # 在新标签页中打开外部链接
post_asset_folder: # 启用资源文件夹功能 建议默认false 文章里面的图片啥的用图床，本地图片多了巨卡
filename_case: # 将文件名转换小写小写1/大写2
relative_link: # 是否创建相对于根文件夹的链接
index_generator.per_page: # 每页显示的文章数
index_generator.order_by: # 发布顺序
date_format: # 日期格式
time_format: # 时间格式
per_page: # 每个页面上显示的文章数
pagination_dir: # 网址格式
theme: # 主题名称
theme_config: # 主题配置，覆盖主题默认值
deploy: # 部署设置
include: # 包括隐藏文件
exclude: # 排除文件/文件夹
ignore: # 忽略文件/文件夹
```

#### > 配置

1. 按照github网站介绍，关闭`highlight`和`prismjs`
- 上面两个主配置这里 `enable: false`只需要把这里设置为`false` 即可
2. 然后把主题那里换乘我们`theme`文件夹下面的主题名称
- 我这里是`themesparticlex`我就换成这个
- ![主题预览](https://static.litetools.top/blogs/hexo/10_1.png)
3. **每次要重新测试啥的最好都按照如下操作执行一下**
- `hexo cl` 清理静态文件缓存
- `hexo g`   重新生成静态文件
- `hexo s -p 80`  开启一个80端口的服务，不加`-p 80`默认是4000端口
4. 后续配置 `deploy`
#### > GitHubPage配置
```yaml
deploy:
  type: 'git'
  repo: git@github.com:Heartfilia/Heartfilia.github.io.git  # 这里就是你git那里复制的
  branch: pages   # 分支名，git那边没有也没事，我们这里弄了后会自动创建

# 然后我们自己的项目代码就在git的 main 分支
# github pages展示的项目就是 这里的 pages 分支
```
### 3.4 主题配置文件
#### > 主题下面的
这里的配置文件是在`theme/xxxx/_config.yml`
可以看到里面很多图片其实是空的我这里先添加一些图片，这里为了图片长久可以使用，我这里注册了一个`七牛云` 每个用户有10G的存储空间，我把一些图片视频啥的就往里面放的

#### > 常用配置
```yaml
head_img: 头像图标链接
home_background: 背景图链接

footer:
    since: 2022
    # Customize the server domain name ICP
    ICP:
        enable: true
        code: 这里是ICP备案码
        link: https://www.beian.gov.cn/
```
我这里简单的配置了一下 然后返回项目目录下执行**老三样, **然后我们去浏览器看一下，如果之前有浏览过，可能会有浏览器缓存，看不出来新样式，这里建议，测试的时候用 **浏览器无痕浏览**
```bash
hexo cl
hexo g

# 下面两个看你自己部署情况 二选一 二选二都可以
hexo s -p 80   # 如果直接用服务器或者本地部署
hexo d   # 这里就会根据上面的配置自动把项目部署到 github pages 这里别忘记了前面还要装包哦
```
![预览](https://static.litetools.top/blogs/hexo/11.png)
## 4.日常更新
接下来我们就来讲讲日常的博客日志更新维护，在这之前先留意一下这里
![标签](https://static.litetools.top/blogs/hexo/12.png)
这里我们目前直接去点 很多东西都没有反馈的，那是因为我们没有项目填充，如果不想要这里可以直接在配置文件里面注释掉对应的板块
```yaml
menu:
    home:
        name: house
        theme: solid
        src: /
    about:
        name: id-card
        theme: solid
        src: /about
    archives:
        name: box-archive
        theme: solid
        src: /archives
    categories:
        name: bookmark
        theme: solid
        src: /categories
    tags:
        name: tags
        theme: solid
        src: /tags
```
如果要把上面写的改成自己写的内容的话如图
![改过后](https://static.litetools.top/blogs/hexo/13.png)
直接如下demo那样子修改就好了
```yaml
menu:
    关于我:    # 只需要改这里 下面的板块不要动 要不然会导致图标加载不出来或者路由出错
        name: id-card
        theme: solid
        src: /about
```

**为了能正常显示上面的内容 我们这里需要手动创建几个页面，如果你需要添加其它页面也需要同样的创建一下**
```bash
hexo new page categories    # 后面内容的分类都会在这里面显示
hexo new page tags          # 后面内容的标签都会在这里显示
hexo new page about         # 这里就是一个个人的介绍页面，可以放自己的简介啥的
```
创建了上面的页面后，**目前来说这里是不需要做任何操作的** 这些东西都在  `source/`这个目录下面 点进去就可以看到对应了上面创建出来的目录，里面有一个 `index.md` 然后要做啥就在里面操作就好了
### 4.1 项目创建
具体详细的命令啥的去[官网](https://hexo.io/zh-cn/docs/writing)查看
我们直接在主目录下面执行
`hexo new 文章标题`   >> 这里的标题一般来说中文英文都可以建议这里用 英文 然后标题在markdown文件里面去修改
然后我们会在主目录下面的`source/_posts`下面有一个同名的`md`文件
![创建项目](https://static.litetools.top/blogs/hexo/14.png)
这里默认会有一个`hello-world.md`存在，我这里面删除了
接下来我们就可以直接编辑这个markdown文件了
> 我们用hexo new 创建的文件里面会有一些默认的参数在里面
> 这里创建是只创建一个md文件，如果里面有本地图片的话，可以在
> config.yml 文件中的 post_asset_folder 选项设为 true 来打开，然后再创建就是一个文件夹，然后就可以在文件夹里面引用本地的静态文件了，不建议自己弄，图片多了巨卡巨卡巨卡巨卡巨卡巨卡

#### > 博客内容标签解释
```markdown
---
title: 用了英文名创建后这里可以创建你想要的标题，中文创建的就不用管这个，反正页面显示的内容是根据这里
date: 2022-11-17 10:10:23
tags: 
  - note
  - blog
categories: 随笔
---
更多语法可以查这里: https://hexo.io/zh-cn/docs/front-matter

引言 使用可以查看: https://hexo.io/zh-cn/docs/tag-plugins

大概如此 我这里省略了一些东西
```

想看看可以浏览一下[我的博客](https://heartfilia.github.io)

关于草稿 还有 资源文件 还有啥东西的 可以去

- [标签插件](https://hexo.io/zh-cn/docs/tag-plugins)
- [资源文件夹](https://hexo.io/zh-cn/docs/asset-folders)
- [数据文件夹](https://hexo.io/zh-cn/docs/data-files)
### 4.2 项目发布
只要弄好了都弄好了我们就
```bash
hexo cl
hexo g
hexo d
```
## 5.留言功能
我们可以从我们上面这个主题那里看到其实是有两个默认的留言功能选择给我们

我这里选择了第二个 `waline` 这东西有个不好的，就是后面要用的一个服务端得有科学才可以正常使用，不过问题不大是吧
我们去 [waline官网](https://waline.js.org/)  跟着他们的教程其实也可以直接搭建好，我这里直接用它提供的文档来弄

熟悉按照这里 我们先去注册一个 [存储服务](https://waline.js.org/guide/get-started.html#waline-%E9%83%A8%E7%BD%B2%E6%95%99%E7%A8%8B-%E5%BF%AB%E9%80%9F%E4%B8%8A%E6%89%8B)
 这里使用的是 `leancloud` 这东西国际版要科学， 国内版需要备案

我们直接点页面上很明显的
![部署](https://static.litetools.top/blogs/hexo/15.png)
然后用github绑定登录一下就好了，按照它下面贴的那两个B站教学视频可以完成这里的操作，不懂得反复看一下就好了
最后我们拿到属于自己的一个服务地址

然后我们填入主题的配置里面 
```yaml
waline:
    enable: true
    serverURL: https://***********.vercel.app/
```
然后我们在部署好的博客的单篇文章下面就会有一个评论框了
![评论框](https://static.litetools.top/blogs/hexo/16.png)

# 题外话
其他主题很多配置不太一样，可以根据主题的作者写出来的教程慢慢来配置就好啦
目前我这里还有很多没有美化完，后面继续美化
