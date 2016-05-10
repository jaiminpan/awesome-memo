# DIV+CSS规范命名大全集合

## 一、命名规则说明

  1）、所有的命名最好都小写  
  2）、属性的值一定要用双引号("")括起来，且一定要有值如class="divcss5",id="divcss5"  
  3）、每个标签都要有开始和结束，且要有正确的层次，排版有规律工整  
  4）、空元素要有结束的tag或于开始的tag后加上"/"  
  5）、表现与结构完全分离，代码中不涉及任何的表现元素，如style、font、bgColor、border等  
  6）、`<h1>`到`<h5>`的定义，应遵循从大到小的原则，体现文档的结构，并有利于搜索引擎的查询。  
  7）、给每一个表格和表单加上一个唯一的、结构标记id  
  8）、给图片加上alt标签  
  9）、尽量使用英文命名原则  
  10）、尽量不缩写，除非一看就明白的单词  

## 二、相对网页外层重要部分CSS样式命名

  * 外套 wrap ------------------用于最外层
  * 头部 header ----------------用于头部
  * 主要内容 main ------------用于主体内容（中部）
  * 左侧 main-left -------------左侧布局
  * 右侧 main-right -----------右侧布局
  * 导航条 nav -----------------网页菜单导航条
  * 内容 content ---------------用于网页中部主体
  * 底部 footer -----------------用于底部
```
CSS样式命名	说明
网页公共命名
#wrapper	页面外围控制整体布局宽度
#container或#content	容器,用于最外层
#layout	布局
#head, #header	页头部分
#foot, #footer	页脚部分
#nav	主导航
#subnav	二级导航
#menu	菜单
#submenu	子菜单
#sideBar	侧栏
#sidebar_a, #sidebar_b	左边栏或右边栏
#main	页面主体
#tag	标签
#msg #message	提示信息
#tips	小技巧
#vote	投票
#friendlink	友情连接
#title	标题
#summary	摘要
#loginbar	登录条
#searchInput	搜索输入框
#hot	热门热点
#search	搜索
#search_output	搜索输出和搜索结果相似
#searchBar	搜索条
#search_results	搜索结果
#copyright	版权信息
#branding	商标
#logo	网站LOGO标志
#siteinfo	网站信息
#siteinfoLegal	法律声明
#siteinfoCredits	信誉
#joinus	加入我们
#partner	合作伙伴
#service	服务
#regsiter	注册
arr/arrow	箭头
#guild	指南
#sitemap	网站地图
#list	列表
#homepage	首页
#subpage	二级页面子页面
#tool, #toolbar	工具条
#drop	下拉
#dorpmenu	下拉菜单
#status	状态
#scroll	滚动
.tab	标签页
.left .right .center	居左、中、右
.news	新闻
.download	下载
.banner	广告条(顶部广告条)
电子贸易相关
.products	产品
.products_prices	产品价格
.products_description	产品描述
.products_review	产品评论
.editor_review	编辑评论
.news_release	最新产品
.publisher	生产商
.screenshot	缩略图
.faqs	常见问题
.keyword	关键词
.blog	博客
.forum	论坛
```

#### CSS文件命名	说明
* master.css,style.css	主要的
* module.css	模块
* base.css	基本共用
* layout.css	布局，版面
* themes.css	主题
* columns.css	专栏
* font.css	文字、字体
* forms.css	表单
* mend.css	补丁
* print.css	打印
