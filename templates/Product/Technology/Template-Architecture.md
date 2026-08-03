# [产品/系统名称（英文名）] - 架构设计文档（ADD）

> **文档状态：** 🟡 评审中 / 🟢 已通过 / 🔴 驳回
>
> **保密级别：** 机密 / 内部公开 / 公开
>
> **版本：** vX.X
>
> **日期：** YYYY-MM-DD
>
> **撰写人：** [架构师/技术负责人]
>
> **评审人：** [Kirky.X/TL]
>
> **阅读对象：** [角色列表]
>
> **关联 Charter：** [Charter编号]
>
> **关联 BRD：** [BRD编号]
>
> **关联 PRD：** [PRD编号]

---

## 0. 文档导读

### 0.1 文档目的与适用范围

[说明本文档的目的、适用场景和不适用场景]

### 0.2 相关文档

| 文档类型 | 文件名              | 相关章节   |
| -------- | ------------------- | ---------- |
| [类型]   | [文件名] [行号范围] | [章节描述] |

> **引用格式说明**：关联文档使用 `文件名 行号范围` 格式（如 `【模板】架构设计文档.md 3-21`），行号随文档更新可能变化，请以实际内容为准。

### 0.3 变更记录

| 版本   | 日期       | 修订人 | 变更内容                                           | 审核人    |
| :----- | :--------- | :----- | :------------------------------------------------- | :-------- |
| v0.1   | YYYY-MM-DD | [姓名] | 初稿：上下文+容器图                                | [姓名]    |
| v0.2   | YYYY-MM-DD | [姓名] | 补充组件图+部署图                                  | [姓名]    |
| v0.3   | YYYY-MM-DD | [姓名] | 补充ADR+风险评估                                   | [姓名]    |
| v0.4   | YYYY-MM-DD | [姓名] | 正式发布                                           | [Kirky.X] |
| v0.4.1 | 2026-06-09 | 谢董   | 修复：quadrantChart 模板改为表格格式（飞书不兼容） | —         |
| v0.4.2 | 2026-06-09 | 谢董   | 修复xychart-beta图为表格以兼容飞书渲染             | —         |
| v0.4.3 | 2026-06-09 | 谢董   | 修复gantt图为表格以兼容飞书渲染                    | —         |
| v0.4.4 | 2026-06-20 | 谢董   | 消息中间件示例 Kafka→Pulsar（统一事件总线规范）    | —         |

---

## 1. 执行摘要（Executive Summary）

> **技术决策层导读：** 一页纸说清"系统边界、技术选型、核心风险、关键决策"。

| 要素         | 内容                                                   |
| :----------- | :----------------------------------------------------- |
| **系统定位** | [一句话，如：支撑日均千万级订单的高可用交易内核]       |
| **核心挑战** | [如：高并发秒杀 / 分布式事务一致性 / 多活容灾]         |
| **技术选型** | [如：Spring Cloud + PostgreSQL + Redis + Pulsar + K8s] |
| **架构风格** | [如：微服务 / 领域驱动设计(DDD) / 事件驱动架构(EDA)]   |
| **关键指标** | QPS ≥ [X] / P99 延迟 ≤ [Y]ms / 可用性 ≥ [Z]%           |
| **重大决策** | [如：放弃分布式事务2PC，采用Saga+本地消息表]           |
| **风险等级** | 🟢 低风险 / 🟡 中风险 / 🔴 高风险                      |

```mermaid
mindmap
  root((架构总览))
    业务上下文
      [用户场景]
      [系统边界]
    技术架构
      [C4视图]
      [部署拓扑]
    核心决策
      [技术选型]
      [取舍权衡]
    质量属性
      [性能]
      [可用性]
      [安全]
```

---

## 2. 现状与需求分析（Current State & Requirements）

### 2.1 现状痛点

| 维度       | 现状               | 痛点                          | 量化数据                  |
| :--------- | :----------------- | :---------------------------- | :------------------------ |
| **性能**   | [如：单体架构]     | [如：高峰期CPU 95%，响应超时] | [如：P99=3s，目标<<500ms] |
| **可用性** | [如：单机房部署]   | [如：机房故障导致全站停摆]    | [如：年故障3次，每次>2h]  |
| **扩展性** | [如：垂直扩容]     | [如：扩容需停机，耗时4h]      | [如：峰值只能支撑1万QPS]  |
| **维护性** | [如：代码耦合度高] | [如：改一行代码影响5个模块]   | [如：回归测试周期2周]     |

### 2.2 需求矩阵（功能性 + 非功能性）

> **引用说明**：详细的技术需求、性能指标、可靠性要求、安全合规要求，请参阅 **【模板】技术需求文档(TRD).md**。本文档仅引用关键架构需求。

| 需求类型 | 需求描述 | 优先级 | 架构影响 | 来源文档 |
| :--- | :--- | :---: | :--- | :--- |
| **功能性** | [如：支持10万QPS秒杀下单] | P0 | [架构设计要点] | 引用TRD§1.1 |
| **非功能性** | [如：P99延迟≤200ms] | P0 | [性能设计要点] | 引用TRD§3.1 |
| **非功能性** | [如：RTO≤30s，RPO≤5s] | P0 | [容灾设计要点] | 引用TRD§4.1 |
| **非功能性** | [如：支持灰度发布] | P1 | [部署设计要点] | 引用TRD§7.2 |

> **完整需求**：技术挑战清单、性能基线、容量规划、降级策略详见 **【模板】技术需求文档(TRD).md §1-4**。

---

## 3. C4 架构视图（C4 Model Views）

> 遵循 Simon Brown 提出的 C4 模型，从宏观到微观逐层展开。

### 3.1 Level 1：系统上下文图（System Context）

> **受众：** 全员（产品、运营、管理层、技术）
>
> **抽象层级：** 30,000 英尺，描述系统与外部世界的交互边界。

```mermaid
C4Context
    title 系统上下文图 - [系统名称]
    Person(customer, "普通用户", "浏览商品、下单、支付")
    Person(admin, "运营管理员", "配置活动、查看报表")

    System_Boundary(c1, "本系统边界") {
        System(orderSystem, "订单交易系统", "处理用户下单、支付、履约全流程")
    }

    System_Ext(paymentGateway, "支付网关", "支付宝/微信/银联")
    System_Ext(logisticsSystem, "物流平台", "顺丰/京东/菜鸟")
    System_Ext(userCenter, "用户中心", "统一用户认证与画像")
    System_Ext(productCenter, "商品中心", "SKU、价格、库存")
    System_Ext(messageCenter, "消息中心", "短信/推送/邮件")

    Rel(customer, orderSystem, "下单/查询/取消", "HTTPS/JSON")
    Rel(admin, orderSystem, "管理/监控", "HTTPS/JSON")
    Rel(orderSystem, paymentGateway, "发起支付/查询结果", "HTTPS/JSON")
    Rel(orderSystem, logisticsSystem, "下发物流单", "HTTPS/JSON")
    Rel(orderSystem, userCenter, "查询用户信息", "gRPC")
    Rel(orderSystem, productCenter, "查询商品/校验库存", "gRPC")
    Rel(orderSystem, messageCenter, "发送通知", "Pulsar")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

> **若平台不支持 C4Context 语法，可用以下标准 Mermaid 替代：**

```mermaid
graph TB
    subgraph 外部参与者
        U1[👤 普通用户 / 浏览/下单/支付]
        U2[👤 运营管理员 / 配置/监控]
    end

    subgraph 本系统边界
        S1[(🟦 订单交易系统 / Order System)]
    end

    subgraph 外部依赖系统
        E1[💳 支付网关 / 支付宝/微信]
        E2[🚚 物流平台 / 顺丰/京东]
        E3[👤 用户中心 / 认证/画像]
        E4[📦 商品中心 / SKU/库存]
        E5[📧 消息中心 / 短信/推送]
    end

    U1 -->|HTTPS/JSON / 下单/查询| S1
    U2 -->|HTTPS/JSON / 管理| S1
    S1 -->|HTTPS/JSON / 支付| E1
    S1 -->|HTTPS/JSON / 物流| E2
    S1 -.->|gRPC / 用户信息| E3
    S1 -.->|gRPC / 商品/库存| E4
    S1 -.->|Pulsar / 通知| E5

    style S1 fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style U1 fill:#e1f5e1,stroke:#2e7d32
    style U2 fill:#e1f5e1,stroke:#2e7d32
```

### 3.2 Level 2：容器图（Container Diagram）

> **受众：** 技术负责人、开发、测试、运维
>
> **抽象层级：** 10,000 英尺，描述系统内部的可部署单元（进程/服务/存储）及交互。

```mermaid
C4Container
    title 容器图 - [系统名称] 内部架构
    Person(customer, "普通用户")
    Person(admin, "运营管理员")

    System_Boundary(c1, "订单交易系统") {
        Container(webApp, "Web App", "React", "用户端H5/PC页面")
        Container(mobileApp, "Mobile App", "Flutter", "iOS/Android客户端")
        Container(adminWeb, "Admin Web", "React", "运营管理后台")
        Container(apiGateway, "API Gateway", "Spring Cloud Gateway", "统一入口/鉴权/限流")
        Container(orderService, "订单服务", "Spring Boot", "订单生命周期管理")
        Container(payService, "支付服务", "Spring Boot", "支付路由/对账")
        Container(scheduleService, "调度服务", "XXL-JOB", "超时取消/定时任务")
        ContainerDb(orderDB, "订单库", "PostgreSQL", "主从与分库分表")
        ContainerDb(orderCache, "订单缓存", "Redis Cluster", "热点数据/分布式锁")
        ContainerDb(orderES, "订单搜索", "Elasticsearch", "复杂查询/报表")
        ContainerQueue(orderMQ, "订单队列", "Pulsar", "异步解耦/事件溯源")
    }

    System_Ext(payment, "支付网关")
    System_Ext(logistics, "物流平台")

    Rel(customer, webApp, "使用", "HTTPS")
    Rel(customer, mobileApp, "使用", "HTTPS")
    Rel(admin, adminWeb, "使用", "HTTPS")
    Rel(webApp, apiGateway, "调用API", "JSON/HTTPS")
    Rel(mobileApp, apiGateway, "调用API", "JSON/HTTPS")
    Rel(adminWeb, apiGateway, "调用API", "JSON/HTTPS")
    Rel(apiGateway, orderService, "路由", "gRPC")
    Rel(apiGateway, payService, "路由", "gRPC")
    Rel(orderService, orderDB, "读写", "JDBC")
    Rel(orderService, orderCache, "缓存/锁", "Redis协议")
    Rel(orderService, orderES, "写入", "REST")
    Rel(orderService, orderMQ, "发布事件", "Pulsar协议")
    Rel(payService, payment, "调用", "HTTPS")
    Rel(orderService, logistics, "调用", "HTTPS")
    Rel(scheduleService, orderService, "触发任务", "gRPC")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

> **标准 Mermaid 替代方案：**

```mermaid
graph TB
    subgraph 前端层
        F1[📱 Mobile App / Flutter]
        F2[🌐 Web App / React]
        F3[⚙️ Admin Web / React]
    end

    subgraph 接入层
        G1[🛡️ API Gateway / Spring Cloud Gateway / 鉴权/限流/路由]
    end

    subgraph 服务层
        S1[📋 订单服务 / Spring Boot / 订单生命周期]
        S2[💳 支付服务 / Spring Boot / 支付路由/对账]
        S3[⏰ 调度服务 / XXL-JOB / 超时取消/定时任务]
    end

    subgraph 数据层
        D1[(🗄️ 订单主库 / PostgreSQL / 主从与分片)]
        D2[(⚡ 订单缓存 / Redis Cluster / 热点/锁)]
        D3[(🔍 订单搜索 / Elasticsearch / 复杂查询)]
        D4[(📨 消息队列 / Pulsar / 异步/事件)]
    end

    subgraph 外部系统
        E1[💳 支付网关]
        E2[🚚 物流平台]
    end

    F1 --> |HTTPS/JSON| G1
    F2 --> |HTTPS/JSON| G1
    F3 --> |HTTPS/JSON| G1
    G1 -->|gRPC| S1
    G1 -->|gRPC| S2
    S1 -->|JDBC| D1
    S1 -->|Redis| D2
    S1 -->|REST| D3
    S1 -->|Pulsar| D4
    S2 -->|HTTPS| E1
    S1 -->|HTTPS| E2
    S3 -->|gRPC| S1

    style G1 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style S1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style D1 fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

### 3.3 Level 3：组件图（Component Diagram）

> **受众：** 开发团队、架构师
>
> **抽象层级：** 1,000 英尺，描述单个容器内部的组件结构与交互。

```mermaid
graph TB
    subgraph 订单服务内部组件
        C1[🎮 OrderController / 接口层 / REST/gRPC入口]
        C2[⚙️ OrderService / 业务层 / 订单状态机/业务规则]
        C3[🔗 OrderManager / 聚合层 / 跨域编排/事务管理]
        C4[🗃️ OrderDAO / 数据层 / MyBatis/CRUD]
        C5[🔌 RPC Client / 调用层 / 用户/商品/库存/消息]
        C6[📦 StockComponent / 组件 / 库存扣减/预占/回滚]
        C7[🎁 PromoComponent / 组件 / 优惠计算/规则引擎]
        C8[📊 EventPublisher / 组件 / 领域事件发布]
    end

    C1 -->|DTO/VO| C2
    C2 --> C6
    C2 --> C7
    C2 --> C8
    C2 -->|领域对象| C3
    C3 -->|聚合根| C4
    C3 -->|Feign/gRPC| C5
    C4 -->|SQL| D1[(订单库)]
    C5 -->|调用| E1[外部服务]
    C8 -->|发布| Q1[(Pulsar)]

    style C2 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style C3 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
```

### 3.4 Level 4：代码/类图（Code Diagram）【可选】

> **受众：** 核心开发
>
> **说明：** 仅对核心复杂组件（如状态机、规则引擎）绘制，一般不建议全量产出，避免过度设计。

```mermaid
classDiagram
    class Order {
        +Long orderId
        +Long userId
        +BigDecimal totalAmount
        +OrderStatus status
        +List~OrderItem~ items
        +pay()
        +cancel()
        +ship()
    }

    class OrderItem {
        +Long itemId
        +String skuId
        +Integer quantity
        +BigDecimal unitPrice
    }

    class OrderStatus {
        <<enumeration>>
        CREATED
        PAID
        SHIPPED
        COMPLETED
        CANCELLED
    }

    class OrderService {
        +createOrder()
        +payOrder()
        +cancelOrder()
    }

    class OrderStateMachine {
        +fire(event)
        +canTransition(from, to)
    }

    Order "1" *-- "N" OrderItem
    Order --> OrderStatus
    OrderService --> Order
    OrderService --> OrderStateMachine
```

---

## 4. 动态行为视图（Dynamic Views）

> 描述关键场景的运行时行为，补充 C4 静态视图。

### 4.1 核心流程序列图

#### 场景：用户下单支付全流程

```mermaid
sequenceDiagram
    actor U as 用户
    participant App as Mobile/Web App
    participant GW as API Gateway
    participant OS as 订单服务
    participant PS as 支付服务
    participant US as 用户中心
    participant PCS as 商品中心
    participant ICS as 库存中心
    participant MQ as Pulsar
    participant Pay as 支付网关

    U->>App: 1. 提交订单
    App->>GW: 2. 创建订单请求
    GW->>OS: 3. 路由至订单服务
    OS->>US: 4. 校验用户状态
    US-->>OS: 用户正常
    OS->>PCS: 5. 查询商品/价格
    PCS-->>OS: 返回SKU信息
    OS->>ICS: 6. 预占库存
    ICS-->>OS: 预占成功
    OS->>OS: 7. 计算优惠/生成订单
    OS->>MQ: 8. 发布 OrderCreated 事件
    OS-->>GW: 返回订单信息
    GW-->>App: 订单创建成功
    App-->>U: 展示待支付订单

    U->>App: 9. 确认支付
    App->>GW: 10. 支付请求
    GW->>PS: 11. 路由至支付服务
    PS->>Pay: 12. 发起预下单
    Pay-->>PS: 返回支付参数
    PS-->>GW: 返回调起参数
    GW-->>App: 调起收银台
    App->>Pay: 13. 用户完成支付
    Pay->>PS: 14. 异步支付回调
    PS->>OS: 15. 通知订单已支付
    OS->>ICS: 16. 确认扣减库存
    OS->>MQ: 17. 发布 OrderPaid 事件
    OS->>MQ: 18. 发送支付成功通知
```

### 4.2 状态机图

```mermaid
stateDiagram-v2
    [*] --> CREATED: 用户下单
    CREATED --> PAID: 支付成功
    CREATED --> CANCELLED: 超时/主动取消
    PAID --> SHIPPED: 仓库发货
    PAID --> CANCELLED: 发货前退款
    SHIPPED --> DELIVERED: 物流签收
    DELIVERED --> COMPLETED: 确认收货
    DELIVERED --> RETURNING: 售后退货
    RETURNING --> REFUNDED: 退款完成
    CANCELLED --> [*]
    COMPLETED --> [*]
    REFUNDED --> [*]

    note right of CREATED
        支付倒计时:30分钟
        超时自动取消
    end note
```

### 4.3 异常/补偿流程

```mermaid
sequenceDiagram
    participant OS as 订单服务
    participant ICS as 库存中心
    participant PS as 支付服务
    participant MQ as Pulsar
    participant CS as 补偿服务

    MQ->>CS: 监听 OrderCancelled 事件
    CS->>OS: 1. 查询订单状态
    OS-->>CS: 已取消
    CS->>ICS: 2. 释放预占库存
    ICS-->>CS: 释放成功
    CS->>PS: 3. 查询支付状态
    PS-->>CS: 已支付（需退款）
    CS->>PS: 4. 发起原路退款
    PS-->>CS: 退款受理
    CS->>MQ: 5. 发布 RefundInitiated 事件
```

---

## 5. 部署架构（Deployment Architecture）

> 描述容器如何映射到基础设施，回答"跑在哪里、怎么容灾"。

### 5.1 部署拓扑图

```mermaid
graph TB
    subgraph 流量入口层
        DNS[🌍 DNS / GeoDNS/智能解析]
        CDN[📦 CDN / 静态资源加速]
        WAF[🛡️ WAF / 防火墙/DDoS防护]
    end

    subgraph 可用区 AZ-1a
        LB1[⚖️ SLB-1a / 负载均衡]
        K8S1[☸️ K8s Cluster-1a]
        APP1[🟦 订单服务 Pod]
        APP2[🟦 支付服务 Pod]
        DB1[(🗄️ PostgreSQL 主 / Master)]
        RED1[(⚡ Redis 主 / Master)]
    end

    subgraph 可用区 AZ-1b
        LB2[⚖️ SLB-1b / 负载均衡]
        K8S2[☸️ K8s Cluster-1b]
        APP3[🟦 订单服务 Pod]
        APP4[🟦 支付服务 Pod]
        DB2[(🗄️ PostgreSQL 从 / Slave)]
        RED2[(⚡ Redis 从 / Slave)]
    end

    subgraph 可用区 AZ-1c
        DB3[(🗄️ PostgreSQL 从 / Slave)]
        RED3[(⚡ Redis 从 / Slave)]
        ES1[(🔍 ES 节点1)]
        ES2[(🔍 ES 节点2)]
    end

    subgraph 中间件层
        PULSAR[📨 Pulsar Cluster / 3 Broker]
        ZK[🔍 ZooKeeper / 协调]
    end

    DNS --> CDN --> WAF
    WAF --> LB1
    WAF --> LB2
    LB1 --> K8S1
    LB2 --> K8S2
    K8S1 --> APP1
    K8S1 --> APP2
    K8S2 --> APP3
    K8S2 --> APP4

    APP1 --> DB1
    APP2 --> DB1
    APP3 --> DB1
    APP4 --> DB1
    DB1 -.->|主从同步| DB2
    DB1 -.->|主从同步| DB3

    APP1 --> RED1
    APP2 --> RED1
    APP3 --> RED1
    APP4 --> RED1
    RED1 -.->|复制| RED2
    RED1 -.->|复制| RED3

    APP1 --> PULSAR
    APP2 --> PULSAR
    APP3 --> PULSAR
    APP4 --> PULSAR
    APP1 --> ES1
    APP2 --> ES1
    APP3 --> ES1
    APP4 --> ES1

    style DB1 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style RED1 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style PULSAR fill:#e1f5e1,stroke:#2e7d32,stroke-width:2px
```

### 5.2 多活/容灾策略

| 策略           | 实现方式                                     |  RTO  | RPO  | 适用场景     |
| :------------- | :------------------------------------------- | :---: | :--: | :----------- |
| **同城双活**   | AZ-1a / AZ-1b 同时承接流量，数据库主从切换   |  30s  |  0s  | 机房级故障   |
| **异地冷备**   | AZ-2 定时备份，故障时手动切换                | 30min | 5min | 城市级灾难   |
| **数据多副本** | PostgreSQL 半同步复制 + Redis Cluster 3主3从 |   -   |  -   | 数据可靠性   |
| **降级预案**   | 库存校验降级读缓存 / 支付降级走兜底通道      |  5s   |  -   | 依赖服务故障 |

---

## 6. 数据架构（Data Architecture）

### 6.1 数据流图

```mermaid
flowchart LR
    subgraph 业务系统
        A1[订单服务]
        A2[支付服务]
    end

    subgraph 实时链路
        B1[Binlog采集 / Canal]
        B2[Pulsar / 实时流]
        B3[Flink / 实时计算]
    end

    subgraph 离线链路
        C1[ODS贴源层]
        C2[DWD明细层]
        C3[DWS汇总层]
        C4[ADM应用层]
    end

    subgraph 数据消费
        D1[BI报表]
        D2[算法模型]
        D3[对账系统]
    end

    A1 -->|业务写入| DB1[(PostgreSQL)]
    DB1 -->|Canal| B1
    B1 --> B2
    B2 --> B3
    B3 --> C3
    C1 --> C2 --> C3 --> C4
    C4 --> D1
    C3 --> D2
    B2 --> D3
```

### 6.2 数据分片与路由

| 数据类型  | 分片键        | 分片策略               | 路由方式       |
| :-------- | :------------ | :--------------------- | :------------- |
| 订单主表  | `user_id`     | 128 分片，Hash 取模    | ShardingSphere |
| 订单明细  | `order_id`    | 与主表同分片（绑定表） | 本地路由       |
| 支付流水  | `order_id`    | 128 分片               | ShardingSphere |
| 日志/审计 | `create_time` | 按月分区               | 时间范围路由   |

---

## 7. 核心算法与机制设计（Core Mechanisms）

### 7.1 全局唯一ID生成

```mermaid
flowchart LR
    A[时间戳 / 41bit] --> E[雪花算法 / 64bit]
    B[机器ID / 10bit] --> E
    C[序列号 / 12bit] --> E
    D[业务标识 / 1bit] --> E
    E --> F[Long类型 / 全局唯一ID]

    style F fill:#fff9c4,stroke:#f9a825,stroke-width:2px
```

| 属性     | 设计值 | 说明                           |
| :------- | :----- | :----------------------------- |
| 时间戳位 | 41bit  | 支持约69年（从自定义起始时间） |
| 机器ID位 | 10bit  | 支持1024个节点                 |
| 序列号位 | 12bit  | 每节点每毫秒4096个ID           |
| 业务标识 | 1bit   | 区分不同业务线（订单/支付）    |

### 7.2 分布式锁设计

| 场景         | 实现方案        | Key设计                      | 过期时间 | 续期策略         |
| :----------- | :-------------- | :--------------------------- | :------: | :--------------- |
| 库存扣减     | Redis RedLock   | `lock:stock:{skuId}`         |   10s    | Watchdog自动续期 |
| 订单创建防重 | DB唯一索引      | `uniq:order:{userId}:{date}` |   永久   | 无需续期         |
| 支付回调幂等 | Redis SET NX EX | `lock:pay:{orderId}`         |   60s    | 业务完成主动释放 |

### 7.3 缓存策略

```mermaid
flowchart TD
    A[读请求] --> B{缓存命中?}
    B -->|是| C[返回缓存数据]
    B -->|否| D[查询数据库]
    D --> E[写入缓存]
    E --> C
    F[写请求] --> G[更新数据库]
    G --> H[删除/更新缓存 / Cache Aside]

    style C fill:#e1f5e1,stroke:#2e7d32
    style H fill:#fff3e0,stroke:#ef6c00
```

| 策略          | 适用场景     | 一致性等级 | 实现方式             |
| :------------ | :----------- | :--------- | :------------------- |
| Cache Aside   | 订单详情查询 | 最终一致   | 读时回源，写时删缓存 |
| Write Through | 库存实时扣减 | 强一致     | 同步写库+写缓存      |
| Read Through  | 商品基础信息 | 最终一致   | 缓存组件自动回源     |

---

## 8. 非功能需求设计（NFR / Quality Attributes）

### 8.1 性能设计

| 指标         | 目标值    | 达成手段                           |
| :----------- | :-------- | :--------------------------------- |
| **峰值 QPS** | ≥ 100,000 | 水平扩展 + 缓存预热 + 异步化       |
| **P99 延迟** | ≤ 200ms   | 本地缓存 + 数据库索引优化 + 连接池 |
| **并发连接** | ≥ 50,000  | 网关长连接优化 + K8s HPA           |

> **说明**：xychart-beta为飞书不兼容Mermaid类型，改为表格描述（模板示例数据）。

**性能容量规划**

| 时间节点 |   QPS   |
| :------- | :-----: |
| 当前     |  5,000  |
| 3个月后  | 30,000  |
| 6个月后  | 80,000  |
| 12个月后 | 120,000 |

### 8.2 高可用设计

```mermaid
flowchart LR
    subgraph 故障场景
        F1[服务实例故障]
        F2[数据库主库故障]
        F3[缓存主节点故障]
        F4[依赖服务故障]
    end

    subgraph 应对策略
        S1[K8s自动重启 / 流量摘除]
        S2[主从切换 / VIP漂移]
        S3[哨兵选举 / 主从切换]
        S4[熔断降级 / 兜底响应]
    end

    F1 --> S1
    F2 --> S2
    F3 --> S3
    F4 --> S4
```

### 8.3 安全设计

| 层级       | 措施                               | 实现                           |
| :--------- | :--------------------------------- | :----------------------------- |
| **接入层** | HTTPS/TLS 1.3、WAF、DDoS防护       | 云厂商安全产品                 |
| **网关层** | OAuth2.1 + JWT、签名验签、限流防刷 | Spring Security + 自定义过滤器 |
| **服务层** | 零信任网络、mTLS、RBAC             | Istio Service Mesh             |
| **数据层** | 敏感字段加密、SQL注入防护          | AES-256-GCM + MyBatis参数化    |
| **审计层** | 全链路日志、操作审计               | SkyWalking + 审计表            |

---

## 9. 架构决策记录（ADR）

> 所有影响两个以上服务、或不可逆转的决策必须记录 ADR。

| 决策ID      | 决策内容       |   状态    | 上下文                             | 决策                          | 后果                             | 日期       |
| :---------- | :------------- | :-------: | :--------------------------------- | :---------------------------- | :------------------------------- | :--------- |
| **ADR-001** | 微服务 vs 单体 | ✅ 已采纳 | 团队>50人，需独立迭代              | 采用微服务，按领域拆分        | 运维复杂度增加，需建设DevOps能力 | YYYY-MM-DD |
| **ADR-002** | 数据库选型     | ✅ 已采纳 | 团队熟悉PostgreSQL，TiDB学习成本高 | PostgreSQL主从+分库分表       | 分片逻辑自研，中期可迁移TiDB     | YYYY-MM-DD |
| **ADR-003** | 分布式事务方案 | ✅ 已采纳 | 性能优先，允许短暂不一致           | Saga + 本地消息表（最终一致） | 需对账补偿机制，放弃强一致       | YYYY-MM-DD |
| **ADR-004** | 缓存一致性策略 | ✅ 已采纳 | 高并发读多写少                     | Cache Aside + 延迟双删        | 极端情况下存在短暂不一致         | YYYY-MM-DD |
| **ADR-005** | 部署方式       | ✅ 已采纳 | 弹性伸缩需求，云原生趋势           | K8s + Docker 容器化           | 需建设K8s运维能力                | YYYY-MM-DD |

### ADR 详细示例：ADR-003 分布式事务

```markdown
## ADR-003：分布式事务一致性方案

### 状态

已采纳 ✅

### 上下文

订单创建涉及订单库、库存库、优惠券库三个独立数据库，需保证数据一致性。

### 候选方案

1. **2PC/XA**：强一致，但阻塞性能差，不适合高并发。
2. **TCC**：性能较好，但业务侵入性高，需为每个操作写Try/Confirm/Cancel。
3. **Saga + 本地消息表**：最终一致，性能最好，通过异步补偿保证一致性。

### 决策

选择方案3：Saga + 本地消息表。

### 理由

- 业务场景允许秒级不一致（库存预占后未及时扣减不影响用户体验）
- 团队已有消息队列基础设施（Pulsar）
- 避免2PC的阻塞和单点问题

### 后果

- 需开发对账补偿服务，定时扫描异常状态订单
- 需建立人工介入流程，处理补偿失败订单
- 监控需覆盖"长时间未完结事务"告警
```

---

## 10. 风险评估与缓解（Risk Assessment）

> **引用说明**：项目级风险（商业风险、市场风险、人员风险）请参阅 **【模板】项目任务书.md §11.1**。本文档仅列出技术架构层面的风险。

| 风险ID    | 风险描述                       | 可能性 | 影响度 | 风险等级 | 缓解措施                              | 责任人 |
| :-------- | :----------------------------- | :----: | :----: | :------: | :------------------------------------ | :----- |
| **R-001** | 分库分表后跨分片查询性能差     |   高   |   高   |    🔴    | ES冗余全量数据，复杂查询走搜索        | [姓名] |
| **R-002** | 缓存雪崩导致DB被打挂           |   中   |   高   |    🔴    | 多级缓存+随机过期+熔断降级            | [姓名] |
| **R-003** | 消息队列消费延迟导致库存不一致 |   中   |   中   |    🟡    | 监控消费延迟，超阈值自动扩容消费者    | [姓名] |
| **R-004** | K8s集群故障导致全量服务不可用  |   低   |   高   |    🟡    | 同城双活+异地灾备，核心服务保留VM部署 | [姓名] |
| **R-005** | 第三方支付接口变更             |   中   |   中   |    🟡    | 抽象支付适配层，支持多渠道快速切换    | [姓名] |

> **项目级风险**：政策风险、市场风险、人员风险等项目级风险的完整登记册（含触发条件和退出条件）详见 **【模板】项目任务书.md §11.1**。

> **说明**：此象限图模板已转为表格描述。

<!--
原 quadrantChart 结构参考：
- title: 风险热力图（可能性 vs 影响度）
- x-axis: "低可能性" --> "高可能性"

- y-axis: "低影响度" --> "高影响度"
- quadrant-1: 重点关注（高/高）
- quadrant-2: 密切监控（低/高）
- quadrant-3: 一般关注（低/低）
- quadrant-4: 定期回顾（高/低）
- 数据点: "R-001 分片查询": [0.8, 0.9]; "R-002 缓存雪崩": [0.6, 0.9]; "R-003 消费延迟": [0.5, 0.6]; "R-004 K8s故障": [0.3, 0.9]; "R-005 支付变更": [0.5, 0.5]
  -->

| 象限                       | 区域特征          | 策略建议               |
| :------------------------- | :---------------- | :--------------------- |
| 象限1（高可能性·高影响度） | 重点关注（高/高） | 制定应急预案，定期演练 |
| 象限2（低可能性·高影响度） | 密切监控（低/高） | 设定预警阈值，持续跟踪 |
| 象限3（低可能性·低影响度） | 一般关注（低/低） | 常规管理，不必过度关注 |
| 象限4（高可能性·低影响度） | 定期回顾（高/低） | 建立流程化管理         |

| 名称           | X值 | Y值 | 象限              |
| :------------- | :-: | :-: | :---------------- |
| R-001 分片查询 | 0.8 | 0.9 | 象限1（重点关注） |
| R-002 缓存雪崩 | 0.6 | 0.9 | 象限1（重点关注） |
| R-003 消费延迟 | 0.5 | 0.6 | 象限1（重点关注） |
| R-004 K8s故障  | 0.3 | 0.9 | 象限2（密切监控） |
| R-005 支付变更 | 0.5 | 0.5 | 中线位置          |

---

## 11. 实施路线图（Implementation Roadmap）

> **说明**：甘特图为飞书不兼容类型，改为表格描述。

| 阶段     | 任务             | 开始日期       | 工期 | 状态 |
| :------- | :--------------- | :------------- | :--: | :--: |
| 基础设施 | K8s集群搭建      | YYYY-MM-DD     | 14d  |  ⚪  |
| 基础设施 | 中间件部署       | 集群搭建完成后 | 10d  |  ⚪  |
| 核心服务 | 订单服务开发     | YYYY-MM-DD     | 20d  |  ⚪  |
| 核心服务 | 支付服务开发     | YYYY-MM-DD     | 20d  |  ⚪  |
| 核心服务 | 集成测试         | 开发完成后     | 10d  |  ⚪  |
| 数据迁移 | 分库分表方案设计 | YYYY-MM-DD     | 10d  |  ⚪  |
| 数据迁移 | 双写迁移         | 方案设计完成后 | 15d  |  ⚪  |
| 数据迁移 | 切流验证         | 双写迁移完成后 | 10d  |  ⚪  |
| 上线     | 灰度发布         | 集成测试完成后 |  7d  |  ⚪  |
| 上线     | 全量上线         | 灰度发布完成后 |  3d  |  ⚪  |
| 上线     | 监控告警         | 全量上线完成后 |  5d  |  ⚪  |

| 阶段        | 里程碑           | 时间   | 交付物            | 通过标准               |
| :---------- | :--------------- | :----- | :---------------- | :--------------------- |
| **Phase 1** | 基础设施就绪     | T+2周  | K8s集群、中间件   | 压测通过               |
| **Phase 2** | 核心服务开发完成 | T+6周  | 订单/支付服务代码 | 单元测试>80%           |
| **Phase 3** | 数据迁移完成     | T+10周 | 双写验证报告      | 数据一致性校验通过     |
| **Phase 4** | 灰度上线         | T+12周 | 灰度监控报告      | P0事故=0，核心指标达标 |
| **Phase 5** | 全量上线         | T+13周 | 上线发布报告      | 业务验证通过           |

---

## 12. 附录（Appendix）

### 12.1 术语表

| 术语         | 定义                                              |
| :----------- | :------------------------------------------------ |
| **C4 Model** | Context/Container/Component/Code 四层架构描述模型 |
| **ADR**      | Architecture Decision Record，架构决策记录        |
| **Saga**     | 分布式事务模式，通过本地事务+补偿实现最终一致     |
| **RTO**      | Recovery Time Objective，恢复时间目标             |
| **RPO**      | Recovery Point Objective，恢复点目标              |
| **QPS**      | Queries Per Second，每秒查询数                    |
| **P99**      | 99%分位延迟                                       |

### 12.2 关联文档

| 文档                | 编号          | 链接   |
| :------------------ | :------------ | :----- |
| 产品需求文档（PRD） | PRD-2026-XXX  | [链接] |
| 数据字典            | DD-2026-XXX   | [链接] |
| 接口文档（API Doc） | API-2026-XXX  | [链接] |
| 测试方案            | TEST-2026-XXX | [链接] |
| 运维手册            | OPS-2026-XXX  | [链接] |

---

## 13. 评审签核（Review & Sign-off）

| 角色       | 姓名 | 签字 | 日期 | 评审意见 |
| :--------- | :--- | :--: | :--: | :------- |
| 技术负责人 |      |      |      |          |
| 架构师     |      |      |      |          |
| 开发代表   |      |      |      |          |
| 测试代表   |      |      |      |          |
| 运维代表   |      |      |      |          |
| 安全负责人 |      |      |      |          |
| 项目总监   |      |      |      |          |
