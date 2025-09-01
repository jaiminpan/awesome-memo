### /brief - 写会话摘要

如果会话快结束了，并且用户输入 `/brief` 或者让你 "写摘要"，立即：
1. 检查 `./docs/Brief.md` 以查看是否有任何现有内容可以保留
2. 写一个全面的摘要，涵盖：
   - 当前会话中取得的重要进展
   - 关键的决策和架构变更
   - 未完成的任务和下一步
   - 需要保留的技术细节
   - 任何使用 compact 功能可能会丢失的上下文
3. 在开头包含当前的日期和时间 (EST)
4. 用新内容覆盖整个 Brief.md 文件

**目的**: 摘要作为 Claude Code 的 "compact" 功能之上的一个额外层，以确保会话之间不会丢失重要细节。 这与简洁无关 - 尽可能彻底，以保留所有重要上下文。

**何时使用**:
- 在重要的开发会话结束时
- 当做出重要的架构决策时
- 在使用 compact 功能之前，如果关键细节可能会丢失
- 当用户明确要求时

**注意**: 当被要求 "阅读摘要" 时，只需阅读 Brief.md 文件，无需修改它。 这通常发生在 /start 之后会话的开始。


## > vi Brief.md

在创建新的 Brief 时，除非用户指示，否则始终覆盖整个 Brief，因为有时我们只需要更新现有的 Brief（除了顶部的这一段，它应该始终保持原样）。 创建 Brief 时，始终包含 Brief 的日期和时间 EST。 Brief 是临时的，仅用于帮助从一个会话延续到另一个会话。 始终只有一个 Brief 文档。 我们不使用 Claude Code CLI 的 "compact" 功能。 相反，我们使用 Brief 作为在需要时确保会话到会话连续性的手段。

# 摘要

**日期/时间**: 2025 年 7 月 5 日，凌晨 12:11 EST


Create a futuristic website banner inspired by this layout: https://i.ibb.co/s9YRj9nM/2-1.png. The design is for "iPunic", a global IP proxy service. Enhance the tech aesthetic by adding elements like glowing global networks, digital nodes, abstract 3D world maps, and data streams. Use a dark gradient background (deep blue to purple), with luminous lines, cyber grid overlays, and motion-inspired visuals to convey speed and security. Incorporate HUD-style UI details and abstract server visuals. Leave central space for headline text. The overall tone should be high-tech, secure, futuristic, and 