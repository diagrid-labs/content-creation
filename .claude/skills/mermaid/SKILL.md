---
name: mermaid
description: This defines the rules of a Diagrid styled mermaid diagram. Use this skill when the user mentions: draw a mermaid diagram, create a workflow diagram, generate a diagram.
---

- Flowchart is the default diagram type that should be used unless explicitly asked otherwise.
- The default direction should be left to right (LR) unless the number of nodes are more than 5, then use top down (TD).
- Each application/service requires an AppID in Catalyst. The AppID nodes should be part of a subgraph named Catalyst. 
- If a Catalyst node or subgraph is present in the diagram the stroke color of that node or subgraph should be #0bdda3.
- If a diagram of a workflow with its activities should be drawn using unidirectional lines between the activities `-->`. A Workflow always starts with a Start node and ends with an End node.

## Node formats

- Application or service node: `APP(My App)`
- Catalyst node: `CAT(Catalyst)`
- State store node: `STATE[(State store)]`
- Pub/Sub message broker or queue: `BROKER@{ shape: das, label: "Message broker" }`
- Workflow activity node: `ACT(Activity)`
- Workflow start node: `START((Start))`
- Workflow end node: `END((End))`
- Workflow decision node: `CHOICE{Check}`

## Line formats

- Regular line: `-->`
- Bidirectional line: `<-->`
- Line with label: `--"Label"-->`
- Async communication line (for pub/sub): `-.->` 

## Examples

```mermaid
---
title: Communication between two applications via service invocation
config:
  theme: 'base'
  themeVariables:
    textColor: '#888'
    titleColor: '#333'
    background: '#EEE'
    primaryColor: '#EEE'
    primaryTextColor: '#333'
    primaryBorderColor: '#333'
    lineColor: '#0bdda3'
  flowchart:
    nodeSpacing: 60
    rankSpacing: 40
---
flowchart LR
  APP1(App 1)
  subgraph Catalyst
    APPID1(App ID1)
    APPID2(App ID2)
  end
  APP2(App 2)
  APP1-->APPID1
  APPID1-->APPID2
  APPID2-->APP2

  style Catalyst stroke:#0bdda3
```

```mermaid
---
title: Communication between two applications via pub/sub messaging
config:
  theme: 'base'
  themeVariables:
    textColor: '#888'
    titleColor: '#333'
    background: '#EEE'
    primaryColor: '#EEE'
    primaryTextColor: '#333'
    primaryBorderColor: '#333'
    lineColor: '#0bdda3'
  flowchart:
    nodeSpacing: 60
    rankSpacing: 40
---
flowchart LR
  APP1(App 1)
  subgraph Catalyst
    APPID1(App ID1)
    APPID2(App ID2)
  end
  BROKER@{ shape: das, label: "Message broker" }
  APP2(App 2)
  APP1-->APPID1
  APPID1-.->BROKER
  BROKER-.->APPID2
  APPID2-->APP2

  style Catalyst stroke:#0bdda3
```

```mermaid
---
title: Bidirectional communication between workflow  application, Catalyst, and state store
config:
  theme: 'base'
  themeVariables:
    textColor: '#888'
    titleColor: '#333'
    background: '#EEE'
    primaryColor: '#EEE'
    primaryTextColor: '#333'
    primaryBorderColor: '#333'
    lineColor: '#0bdda3'
  flowchart:
    nodeSpacing: 60
    rankSpacing: 40
---
flowchart LR
  APP(My Workflow App)
  CAT(Catalyst 
  Workflow Engine)
  STORAGE[(State Store)]
  APP<-->CAT
  CAT<-->STORAGE

```


```mermaid
---
title: An activity chaining workflow with a decision point after the 1st activity.
config:
  theme: 'base'
  themeVariables:
    textColor: '#888'
    titleColor: '#333'
    background: '#EEE'
    primaryColor: '#EEE'
    primaryTextColor: '#333'
    primaryBorderColor: '#333'
    lineColor: '#0bdda3'
  flowchart:
    nodeSpacing: 60
    rankSpacing: 40
---
flowchart LR
  START((Start))
  ACT1(Activity1)
  ACT2(Activity2)
  ACT3(Activity3)
  CHOICE1{Decision}
  END((End))
  START-->ACT1
  ACT1-->CHOICE1
  CHOICE1--"No"-->END
  CHOICE1--"Yes"-->ACT2
  ACT2-->ACT3
  ACT3-->END
```