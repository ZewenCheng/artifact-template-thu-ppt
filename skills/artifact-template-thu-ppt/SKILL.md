---
name: artifact-template-thu-ppt
description: "制作或改版清华紫学术 PPT。适用于论文解读、组会和技术报告。沿用 #660874 顶栏、左侧白色标题、右上机构标志位、可编辑科研图表与中文逐页讲稿。用户提到 THU PPT、清华紫模板或点名本技能时使用。"
license: MIT
---

# 清华紫学术 PPT

以随包的 16∶9 可编辑演示为起点。标题置于深紫色顶栏左侧，正文使用白底，右上预留机构标志位。模板提供 20 种页型，页数和顺序由本次汇报决定。

## 选择页型

1. 在[模板清单](artifact-template.json)中找到[可编辑参考稿](assets/reference.pptx)。复制工作副本，根据[版式索引](references/layout-catalog.md)挑选相近的页。可先看[第 1 至 10 页](assets/reference-contact-sheet-01-10.jpg)和[第 11 至 20 页](assets/reference-contact-sheet-11-20.jpg)。
2. 根据[视觉规范](references/visual-system.md)和[设计参数](assets/design-tokens.json)设置页眉、字体、边距及页脚。正文页顶栏高 124/720，封面色块高 328/720。如果提供了可用的机构标志，按[标志放置说明](references/logo.md)替换右上角的预留区。
3. 根据[信息排列](references/information-order.md)为每一页确定问题、证据和解释。论文解读通常围绕方法展开。沿用用户提供的研究主线、指定页数和语言。默认使用英文标题、模型名称和图内短标签，配简明中文解释，完整中文讲稿写入演讲者备注。
4. 用当前环境中支持 PPTX 的演示工具导入、编辑和导出，优先使用可用的 Presentations 技能。直接修改标题、正文、图形、连接线、原生表格和图表。复制页时更新演讲者备注、图注、引用、替代文本、隐藏对象和文档属性。

## 科研图与验收

绘制架构、公式或实验图时读取[图形与公式](references/image-workflow.md)。核对数据、评估口径、科学结论和最终输出时读取[科研验收](references/research-workflow.md)。示例使用自拟教学序列，实际汇报中的题目、作者、结果、机构和出处均来自本次材料。

按用户要求交付。制作完整本地研究报告的默认交付是可编辑 PPTX、同版 PDF 和中文逐页讲稿。需复用的新图和公式附带源文件。使用最终保存的文件逐页渲染，核查中文、公式、图例、备注、标志、裁切与对齐。仅在用户要求时核算演讲时长。
