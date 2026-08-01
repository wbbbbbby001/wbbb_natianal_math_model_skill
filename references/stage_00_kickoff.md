# 阶段0：启动与选题

> 目标：黄金 30 分钟定题，确定题型与问题拆解，写 72h 时间规划。建议耗时 0.5-2h。

## 入口条件

- 用户说"开始建模"/"选题"，或已提供题号/题目路径；
- `<PROJECT_ROOT>/state/decision_log.json` 已初始化（无则从 `templates/decision_log.json` 复制）。

## 任务

1. **收集启动字段**（已提供的不再问）：竞赛、题号/题目路径、队员分工、截止时间。
2. **选题（黄金 30 分钟流程）**，可加载 `references/judging_standards.md` 的 A/B/C 定位：
   ```
   1. 三人通读 A/B/C 三题
   2. 列出各题难点与数据
   3. 匹配团队能力与优势
   4. 投票表决
   5. 立刻定题，停止讨论
   ```
   - **选题铁律**：新手绝不硬刚 A 题；数据不可得立刻换题；思路不清晰立刻换题；定题后不反悔。
3. **读取题面**（PDF/文本），逐句拆解：
   - 已知条件、决策目标、约束规则、行业/物理限定；
   - 拆分每个子问题，记录：直接目标、输出要求、前后递进逻辑；
   - 每问题型归类（优化/评价/预测/机理/数据处理），可参考 `references/seven_steps.md`。
4. **数据盘点**：题目自带数据 vs 需自主检索；核心缺失参数假设依据。
5. **72h 时间规划**（加载 `references/time_plan_72h.md`）：按剩余时间生成阶段耗时分配，写入 state。

## 出口门禁（L1）

- [ ] 题号、题型（含每问）、子问题数 N 已写入 `state/decision_log.json`
- [ ] 选题铁律满足（无数据不可得、思路不清晰却强行选题）
- [ ] 时间规划已写入 state 的 `budget`
- [ ] 无 high 级问题

**verdict**：`block`（选题违规/无数据硬选）> `refine`（拆解不完整）> `pass`（进入阶段1）。

## 产出

- `state/decision_log.json` 更新：competition、problem_id、task_type、qi_count、qi_weights、budget、current_stage=1。
