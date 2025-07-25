


创建 CLAUDE.md 上下文文件
# 常用命令
- `npm run build`: 构建项目  
- `npm run typecheck`: 运行类型检查  

# 代码风格  
- 使用 ES 模块语法（`import/export`），而非 CommonJS（`require`）  
- 尽可能使用解构导入（例如：`import { foo } from 'bar'`）  

# 工作流程  
- 完成一系列代码修改后，务必进行类型检查  
- 出于性能考虑，优先运行单个测试，而非整个测试套件

# 核心文件与函数
- 项目中的关键模块或工具函数。

# 测试说明
- 如何运行单元测试或端到端测试。

# 仓库规范
- 分支命名规则、合并策略等。

# 仓库规范
- pyenv 的使用、特定编译器的要求。

# 项目特有的行为
- 任何需要注意的警告或非预期行为。


```
<instruction>
你希望 Claude 执行的主要任务或目标
</instruction>

<context>
任务的背景信息，比如涉及的框架、业务逻辑、团队规范等
</context>

<code_example>
可以参考的代码片段、接口规范或已有实现
</code_example>
```


1.
确认需求，详细的需求

2.
基于需求文档，列一个计划，渐进的TODO列表

3.
不只是测试，不要硬编码，要实现真正的逻辑，代码要健壮可维护可扩展，如果需求不合理请直接告诉我


3. 探索常见的高效工作流
Claude Code 的灵活性允许你自由设计工作流。以下是社区中沉淀下来的一些高效模式。


a. 探索、规划、编码、提交
这是一个适用于多种复杂任务的通用工作流，它强调在编码前进行充分的思考和规划。

探索：要求 Claude 阅读相关文件、图片或 URL，但明确指示它暂时不要编写任何代码。
规划：让 Claude 制定解决问题的计划。使用“think”、“think hard”或“ultrathink”等关键词，可以给予 Claude 更多的计算时间来评估不同方案。
编码：在确认计划后，让 Claude 开始实施。
提交：最后，让 Claude 提交代码、创建 PR，并更新相关文档。

b. 测试驱动开发（TDD）
TDD 与代理式编程相结合，威力倍增。Claude 在有明确目标（如通过测试用例）时表现最佳。

编写测试：让 Claude 根据预期输入输出编写测试用例。
确认失败：运行测试，确保它们因功能未实现而失败。
提交测试：将测试用例提交到版本控制。
实现功能：指示 Claude 编写能通过所有测试的代码，并在此过程中不断迭代。
提交代码：在所有测试通过后，提交最终实现。


c. 视觉驱动开发
与 TDD 类似，你可以为 Claude 提供视觉目标，尤其适用于 UI 开发。

1. 提供截图工具：通过 Puppeteer MCP 服务器或 iOS 模拟器 MCP 服务器，让 Claude 能够截取浏览器或应用的界面。
2. 提供视觉稿：通过粘贴、拖拽或文件路径的方式，将设计稿图片提供给 Claude。
3. 迭代实现：要求 Claude 编写代码、截图、比对视觉稿，并循环迭代直至结果匹配。
4. 提交：满意后提交代码。



