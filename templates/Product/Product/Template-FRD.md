# [产品/系统名称（英文名）] - 功能需求文档（FRD）

> **文档状态：** 🟡 评审中 / 🟢 已通过 / 🔴 驳回
>
> **保密级别：** 机密 / 内部公开 / 公开
>
> **版本：** vX.X
>
> **日期：** YYYY-MM-DD
>
> **撰写人：** [姓名/角色]
>
> **评审人：** [姓名/角色]
>
> **阅读对象：** [角色列表]
>
> **文档层级：** MRD → PRD → **FRD**（本文档）
>
> **关联MRD：** [MRD编号] · [MRD版本]
>
> **关联PRD：** [PRD编号] · [PRD版本]

---

## 0. 文档导读

### 0.1 文档体系位置

FRD 承接 PRD 的产品方案，回答 **"这个功能如何实现"**，是研发、测试、运维的 **唯一技术事实来源**。

```mermaid
graph LR
    A[MRD / '市场机会与用户'] -->|商业评审通过| B[PRD / '产品方案与交互']
    B -->|需求评审通过| C[FRD / '技术实现与接口']
    C -->|技术评审通过| D[开发&测试]
    D -->|验收通过| E[灰度发布]

    style C fill:#e3f2fd,stroke:#1565c0,stroke-width:4px
    style B fill:#fff3e0,stroke:#e65100
    style A fill:#f3e5f5,stroke:#7b1fa2
```

### 0.2 相关文档

| 文档类型 | 文件名              | 相关章节   |
| -------- | ------------------- | ---------- |
| [类型]   | [文件名] [行号范围] | [章节描述] |

> **引用格式说明**：关联文档使用 `文件名 行号范围` 格式（如 `【模板】技术需求文档(TRD).md 3-17`），行号随文档更新可能变化，请以实际内容为准。

### 0.3 变更记录

| 版本   | 日期       | 修订人 | 变更内容                                           | 审核人     |
| :----- | :--------- | :----- | :------------------------------------------------- | :--------- |
| v0.1   | YYYY-MM-DD | [姓名] | 初稿完成                                           | [架构师]   |
| v0.2   | YYYY-MM-DD | [姓名] | 补充异常流程与熔断策略                             | [架构师]   |
| v1.0   | YYYY-MM-DD | [姓名] | 技术评审通过，归档基线                             | [技术总监] |
| v1.0.1 | 2026-06-09 | 谢董   | 修复xychart-beta图为表格以兼容飞书渲染             | —          |
| v1.0.2 | 2026-06-20 | 谢董   | 消息中间件示例 RocketMQ→Pulsar（统一事件总线规范） | —          |

---

## 1. 功能概述（Functional Overview）

### 1.1 功能定义

| 属性         | 说明                                                                                     |
| :----------- | :--------------------------------------------------------------------------------------- |
| **功能名称** | [模块名称，如：智能订单履约引擎]                                                         |
| **功能ID**   | FUNC-XXX                                                                                 |
| **关联PRD**  | [PRD编号-章节，如：PRD-2026-001 §3.2]                                                    |
| **功能目标** | [一句话：系统需要实现的核心能力，如：实现高并发场景下的库存精准扣减与订单状态一致性保障] |
| **业务价值** | [量化价值：如：支撑大促期间10万TPS下单，库存超卖率<<0.001%]                              |

### 1.2 功能全景图（Use Case）

```mermaid
graph LR
    subgraph 外部参与者
        U1[终端用户 / C端消费者]
        U2[商家运营 / B端管理员]
        U3[内部系统 / ERP/WMS]
    end

    subgraph 功能边界
        F1[提交订单]
        F2[订单查询]
        F3[订单取消]
        F4[订单改价]
        F5[自动分仓]
    end

    subgraph 外部依赖
        D1[支付网关]
        D2[物流平台]
        D3[消息推送]
    end

    U1 --> F1
    U1 --> F2
    U1 --> F3
    U2 --> F4
    U3 --> F5
    F1 --> D1
    F5 --> D2
    F1 --> D3

    style F1 fill:#c8e6c9,stroke:#2e7d32
    style F3 fill:#ffcdd2,stroke:#c2185b
```

### 1.3 系统架构

```mermaid
graph TB
    subgraph 接入层
        A1[CDN/静态资源]
        A2[API网关 / 鉴权/限流/路由]
        A3[负载均衡 / SLB]
    end

    subgraph 服务层
        B1[订单服务 / Order Service]
        B2[库存服务 / Inventory Service]
        B3[价格服务 / Pricing Service]
        B4[优惠服务 / Promotion Service]
        B5[履约服务 / Fulfillment Service]
    end

    subgraph 中间件
        C1[(Redis / 分布式锁/缓存)]
        C2[(Pulsar / 异步消息)]
        C3[(ElasticJob / 定时任务)]
    end

    subgraph 数据层
        D1[(PostgreSQL / 订单库-分库分表)]
        D2[(TiDB / 库存流水)]
        D3[(OSS / 订单附件)]
    end

    A2 --> A3
    A3 --> B1
    A3 --> B2
    A3 --> B3
    A3 --> B4
    B1 --> B2
    B1 --> B3
    B1 --> B4
    B1 --> C1
    B1 --> C2
    B2 --> C1
    B5 --> C2
    B5 --> C3
    B1 --> D1
    B2 --> D2
    B5 --> D3

    style B1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style C1 fill:#fff3e0,stroke:#e65100
    style D1 fill:#f3e5f5,stroke:#7b1fa2
```

---

## 2. 领域模型（Domain Model）

### 2.1 实体关系图（ER）

```mermaid
erDiagram
    ORDER ||--o{ ORDER_ITEM : contains
    ORDER ||--|| PAYMENT : has
    ORDER ||--o{ ORDER_LOG : records
    ORDER_ITEM }o--|| SKU : references
    SKU ||--|| INVENTORY : tracks

    ORDER {
        string order_id PK "订单号 O2026xxxx"
        string user_id FK "用户ID"
        int status "状态枚举"
        decimal total_amount "订单总金额"
        decimal pay_amount "实付金额"
        datetime create_time "创建时间"
        datetime expire_time "过期时间"
    }

    ORDER_ITEM {
        string item_id PK "行ID"
        string order_id FK "订单号"
        string sku_id FK "SKU编码"
        int quantity "数量"
        decimal unit_price "单价"
    }

    INVENTORY {
        string sku_id PK "SKU编码"
        int available_stock "可用库存"
        int frozen_stock "冻结库存"
        int version "乐观锁版本号"
        datetime update_time "更新时间"
    }

    PAYMENT {
        string payment_id PK "支付流水号"
        string order_id FK "订单号"
        int channel "支付渠道"
        int status "支付状态"
        decimal amount "支付金额"
    }
```

### 2.2 领域事件（Domain Events）

```mermaid
graph LR
    E1[OrderCreated / 订单已创建] --> H1[库存预占]
    E1 --> H2[优惠券冻结]
    E1 --> H3[消息通知]

    E2[OrderPaid / 订单已支付] --> H4[库存扣减]
    E2 --> H5[生成履约单]
    E2 --> H6[积分发放]

    E3[OrderCancelled / 订单已取消] --> H7[库存释放]
    E3 --> H8[优惠券返还]
    E3 --> H9[退款发起]

    style E1 fill:#e3f2fd,stroke:#1565c0
    style E2 fill:#c8e6c9,stroke:#2e7d32
    style E3 fill:#ffcdd2,stroke:#c2185b
```

---

## 3. 业务流程（Business Process）

### 3.1 核心流程（Happy Path）

```mermaid
flowchart TD
    Start([开始]) --> A[① 接收下单请求]
    A --> B{② 网关校验 / 鉴权/限流/防重}
    B -->|不通过| C[返回 401/429/403]
    B -->|通过| D[③ 参数基础校验]
    D -->|不通过| E[返回 400 参数错误]
    D -->|通过| F[④ 分布式锁 / 防并发超卖]
    F -->|获取失败| G[返回 409 操作冲突]
    F -->|获取成功| H[⑤ 库存校验]
    H -->|库存不足| I[返回 400 库存不足]
    H -->|库存充足| J[⑥ 价格计算 / 实时价与优惠]
    J --> K[⑦ 创建订单 / 订单项与支付单]
    K --> L[⑧ 异步消息 / 库存预占/通知]
    L --> M[⑨ 返回订单结果]
    M --> End([结束])

    C --> End
    E --> End
    G --> End
    I --> End

    style Start fill:#e1f5fe
    style End fill:#e1f5fe
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style C fill:#ffcdd2
    style E fill:#ffcdd2
    style G fill:#ffcdd2
    style I fill:#ffcdd2
```

### 3.2 异常与降级流程

```mermaid
flowchart TD
    A[主流程异常] --> B{异常类型}

    B -->|下游超时| C[熔断策略]
    C --> C1[价格服务>500ms]
    C1 --> C2[返回缓存价格 / 误差容忍±5%]
    C2 --> C3[记日志与告警 / 人工核验]

    B -->|库存不一致| D[对账补偿]
    D --> D1[定时扫描 / 预占>15min未支付]
    D1 --> D2[自动释放库存]
    D2 --> D3[优惠券返还]

    B -->|支付回调丢失| E[消息兜底]
    E --> E1[支付状态轮询 / 每30s×10次]
    E1 -->|仍失败| E2[人工工单 / 客服介入]

    B -->|系统崩溃| F[事务回滚]
    F --> F1[订单创建失败]
    F1 --> F2[库存未预占]
    F2 --> F3[优惠券未冻结]
    F3 --> F4[幂等Key保留 / 防重复提交]

    style C fill:#fff3e0,stroke:#e65100
    style D fill:#e3f2fd,stroke:#1565c0
    style E fill:#f3e5f5,stroke:#7b1fa2
```

### 3.3 异常场景矩阵

| 异常ID      | 场景     | 触发条件             | 系统行为           | 错误码 | 用户提示                 | 监控告警 |
| :---------- | :------- | :------------------- | :----------------- | :----: | :----------------------- | :------: |
| TPL-ERR-001 | 参数缺失 | 必填字段为空         | 拒绝请求，记录日志 | 400001 | "请完善必填信息"         |    否    |
| TPL-ERR-002 | 重复提交 | 幂等Key已存在        | 返回上次结果       | 200001 | "操作成功"               |    否    |
| TPL-ERR-003 | 并发冲突 | 乐观锁版本不一致     | 提示数据已变更     | 409001 | "数据已更新，请刷新重试" |    是    |
| TPL-ERR-004 | 库存不足 | 可用库存<<购买量     | 拒绝下单           | 400002 | "商品库存不足，仅剩X件"  |    是    |
| TPL-ERR-005 | 依赖超时 | 下游服务>500ms未响应 | 熔断，返回降级数据 | 503001 | "服务繁忙，请稍后再试"   |    是    |
| TPL-ERR-006 | 价格变动 | 实时价与缓存价差>5%  | 提示价格更新       | 400003 | "商品价格已更新，请确认" |    否    |

---

## 4. 状态机（State Machine）

### 4.1 订单状态流转

```mermaid
stateDiagram-v2
    [*] --> CREATED: 提交订单
    CREATED --> PAID: 支付成功
    CREATED --> CANCELLED: 用户取消/超时未付
    CREATED --> CLOSED: 系统关单(15min)

    PAID --> SHIPPED: 仓库发货
    PAID --> REFUNDING: 用户申请退款

    SHIPPED --> DELIVERED: 物流签收
    SHIPPED --> RETURNING: 用户拒收

    DELIVERED --> COMPLETED: 用户确认收货(7d自动)
    DELIVERED --> REFUNDING: 售后申请

    REFUNDING --> REFUNDED: 退款完成
    REFUNDING --> REJECTED: 退款驳回

    RETURNING --> RETURNED: 退货入库
    CANCELLED --> [*]
    CLOSED --> [*]
    COMPLETED --> [*]
    REFUNDED --> [*]
    RETURNED --> [*]
    REJECTED --> COMPLETED

    note right of CREATED
        超时时间:15分钟
        定时任务:ElasticJob 每1分钟扫描
    end note

    note right of PAID
        支付成功后触发:
        1. 库存正式扣减
        2. 生成履约单
        3. 消息通知仓库
    end note
```

### 4.2 状态转换规则

| 当前状态  | 目标状态  | 触发事件     | 前置条件       | 后置动作             | 权限 |
| :-------- | :-------- | :----------- | :------------- | :------------------- | :--- |
| CREATED   | PAID      | 支付回调成功 | 金额匹配       | 扣减库存、通知仓库   | 系统 |
| CREATED   | CANCELLED | 用户点击取消 | 未支付         | 释放库存、返还优惠券 | 买家 |
| CREATED   | CLOSED    | 超时关单     | 创建时间>15min | 释放库存、返还优惠券 | 系统 |
| PAID      | SHIPPED   | 仓库扫描出库 | 库存已扣减     | 更新物流单号         | 商家 |
| DELIVERED | COMPLETED | 自动确认收货 | 签收时间>7d    | 结算商家、发放积分   | 系统 |

---

## 5. 接口定义（Interface Definition）

### 5.1 接口清单

| 接口ID  | 接口名称     | 方法 | 路径                              |     调用方     | 并发预期  | 优先级 |
| :------ | :----------- | :--: | :-------------------------------- | :------------: | :-------- | :----: |
| API-001 | 创建订单     | POST | `/api/v1/orders`                  | App/Web/小程序 | 5000 TPS  |   P0   |
| API-002 | 查询订单详情 | GET  | `/api/v1/orders/{orderId}`        | App/Web/小程序 | 10000 TPS |   P0   |
| API-003 | 取消订单     | PUT  | `/api/v1/orders/{orderId}/cancel` |    App/Web     | 1000 TPS  |   P0   |
| API-004 | 订单列表     | GET  | `/api/v1/orders`                  |    App/Web     | 5000 TPS  |   P1   |
| API-005 | 支付回调     | POST | `/callback/payment`               |    支付网关    | 3000 TPS  |   P0   |

### 5.2 详细接口：API-001 创建订单

#### 5.2.1 接口概述

| 项           | 内容                                                             |
| :----------- | :--------------------------------------------------------------- |
| **接口名称** | 创建订单                                                         |
| **请求路径** | `POST /api/v1/orders`                                            |
| **接口描述** | 用户提交订单，系统校验库存、价格、优惠后创建订单，返回待支付订单 |
| **幂等性**   | 是（通过`idempotency-key`保证）                                  |
| **超时时间** | 3000ms                                                           |
| **降级策略** | 价格服务超时则使用缓存价格（误差容忍±5%）                        |

#### 5.2.2 请求头（Request Headers）

| 参数              |  类型  | 必填 | 示例                        | 说明                                       |
| :---------------- | :----: | :--: | :-------------------------- | :----------------------------------------- |
| Authorization     | string |  是  | `Bearer eyJhbG...`          | 访问令牌                                   |
| X-Request-ID      | string |  是  | `req_20260525103000_abc123` | 链路追踪ID，全局唯一                       |
| X-Idempotency-Key | string |  是  | `idem_user123_1625103000`   | 幂等键，同一键30分钟内重复请求返回相同结果 |
| Content-Type      | string |  是  | `application/json`          | 固定值                                     |
| X-Client-Version  | string |  否  | `ios/3.2.1`                 | 客户端版本，用于兼容性处理                 |

#### 5.2.3 请求体（Request Body）

```json
{
  "skuList": [
    {
      "skuId": "SKU20260525001",
      "quantity": 2,
      "source": "cart"
    }
  ],
  "addressId": "ADDR123456",
  "couponId": "CPN789012",
  "remark": "请尽快发货，急用",
  "source": "app_ios",
  "extInfo": {
    "deviceId": "device_abc123",
    "ip": "123.45.67.89"
  }
}
```

| 参数        |  类型  | 必填 | 校验规则                                 | 说明                       |
| :---------- | :----: | :--: | :--------------------------------------- | :------------------------- |
| skuList     | array  |  是  | 非空，长度1-50                           | 商品列表                   |
| └─ skuId    | string |  是  | 格式：`SKU`+年月日+3位流水               | 商品SKU                    |
| └─ quantity |  int   |  是  | 1~999                                    | 购买数量                   |
| └─ source   | string |  否  | 枚举：`cart`/`direct`/`activity`         | 来源：购物车/直接购买/活动 |
| addressId   | string |  是  | 已存在且有效的地址ID                     | 收货地址                   |
| couponId    | string |  否  | 有效优惠券ID                             | 优惠券                     |
| remark      | string |  否  | 长度≤200，过滤敏感词                     | 订单备注                   |
| source      | string |  否  | 枚举：`app_ios`/`app_android`/`web`/`mp` | 客户端来源                 |
| extInfo     | object |  否  | —                                        | 扩展信息，用于风控         |

#### 5.2.4 响应体（Response Body）

**成功响应（200 OK）：**

```json
{
  "code": 200,
  "message": "success",
  "traceId": "req_20260525103000_abc123",
  "data": {
    "orderId": "ORD202605250001",
    "status": "CREATED",
    "totalAmount": 299.0,
    "discountAmount": 30.0,
    "payAmount": 269.0,
    "itemCount": 2,
    "createTime": "2026-05-25T10:30:00+08:00",
    "expireTime": "2026-05-25T10:45:00+08:00",
    "paymentUrl": "https://pay.example.com/prepare?token=xxx"
  }
}
```

| 参数           |  类型   | 说明                                                                     |
| :------------- | :-----: | :----------------------------------------------------------------------- |
| orderId        | string  | 订单唯一标识，全局唯一                                                   |
| status         | string  | 订单状态：`CREATED`/`PAID`/`SHIPPED`/`DELIVERED`/`COMPLETED`/`CANCELLED` |
| totalAmount    | decimal | 订单总金额（元）                                                         |
| discountAmount | decimal | 优惠金额（元）                                                           |
| payAmount      | decimal | 实付金额（元）                                                           |
| itemCount      |   int   | 商品件数                                                                 |
| createTime     | string  | 创建时间（ISO8601）                                                      |
| expireTime     | string  | 支付截止时间（15分钟）                                                   |
| paymentUrl     | string  | 支付跳转链接（仅CREATED状态返回）                                        |

**错误响应（400 Bad Request）：**

```json
{
  "code": 400002,
  "message": "库存不足",
  "traceId": "req_20260525103000_abc123",
  "data": {
    "skuId": "SKU20260525001",
    "availableStock": 1,
    "requestQuantity": 2
  }
}
```

#### 5.2.5 错误码总表

| 错误码 | HTTP状态 | 说明         | 客户端处理建议                               |
| :----: | :------: | :----------- | :------------------------------------------- |
| 400001 |   400    | 参数校验失败 | 检查必填字段和格式                           |
| 400002 |   400    | 库存不足     | 提示商品库存不足，引导减少数量或选择其他商品 |
| 400003 |   400    | 优惠券不可用 | 提示优惠券已过期/不适用/已使用               |
| 400004 |   400    | 收货地址无效 | 引导用户重新选择地址                         |
| 401001 |   401    | 登录态失效   | 跳转登录页                                   |
| 429001 |   429    | 请求过于频繁 | 展示倒计时，限制提交频率                     |
| 409001 |   409    | 并发操作冲突 | 提示"数据已更新，请刷新重试"                 |
| 500001 |   500    | 系统内部错误 | 展示友好错误页，上报日志                     |
| 503001 |   503    | 下游服务繁忙 | 提示"服务繁忙，请稍后再试"，建议3秒后重试    |

---

## 6. 数据流与交互时序（Data Flow）

### 6.1 核心下单时序

```mermaid
sequenceDiagram
    autonumber
    actor U as 用户
    participant C as 客户端
    participant GW as API网关 / 鉴权/限流/防重
    participant OS as 订单服务 / Order Service
    participant IS as 库存服务 / Inventory Service
    participant PS as 价格服务 / Pricing Service
    participant CS as 优惠服务 / Promotion Service
    participant DB as 订单库 / PostgreSQL
    participant RC as 缓存 / Redis
    participant MQ as 消息队列 / Pulsar

    U->>C: 提交订单
    C->>GW: POST /api/v1/orders /与Token与Idempotency-Key
    GW->>GW: JWT验签与限流检查

    alt 限流触发
        GW-->>C: 429 Too Many Requests
        C-->>U: 提示操作频繁
    else 正常通过
        GW->>OS: 转发请求

        OS->>OS: 参数基础校验

        OS->>RC: SET order_lock:{userId} NX EX 10
        alt 锁获取失败
            RC-->>OS: 已存在
            OS-->>GW: 409 操作冲突
            GW-->>C: 返回冲突提示
        else 锁获取成功
            OS->>IS: 校验并预占库存
            IS->>RC: DECR available_stock / INCR frozen_stock
            IS->>IS: 写库存流水
            IS-->>OS: 预占成功

            OS->>PS: 获取实时价格
            alt 价格服务超时>500ms
                OS->>RC: 读取缓存价格
                OS->>OS: 标记价格待核验
            else 正常响应
                PS-->>OS: 返回实时价
            end

            opt 使用优惠券
                OS->>CS: 校验并冻结优惠券
                CS-->>OS: 冻结成功
            end

            OS->>DB: 开启事务
            OS->>DB: INSERT 订单主表
            OS->>DB: INSERT 订单项表
            OS->>DB: INSERT 支付单
            DB-->>OS: 返回订单ID

            OS->>MQ: 发送 OrderCreated 事件
            Note over MQ: 异步:通知仓库 / 发送短信/推送 / 更新统计报表

            OS->>RC: DEL order_lock:{userId}
            OS-->>GW: 返回订单详情
            GW-->>C: 200 OK与订单数据
            C-->>U: 展示待支付订单
        end
    end
```

### 6.2 支付回调时序

```mermaid
sequenceDiagram
    autonumber
    participant PG as 支付网关
    participant GW as API网关
    participant OS as 订单服务
    participant DB as 订单库
    participant MQ as 消息队列
    participant FS as 履约服务
    participant WH as 仓库系统

    PG->>GW: POST /callback/payment / 支付结果通知
    GW->>GW: 验签与防重放

    GW->>OS: 转发回调
    OS->>DB: 查询订单状态
    alt 订单已支付/已取消
        OS-->>GW: 返回 200（幂等）
    else 订单待支付
        OS->>DB: 开启事务
        OS->>DB: UPDATE 订单状态 PAID
        OS->>DB: UPDATE 支付单状态 SUCCESS
        OS->>DB: COMMIT

        OS->>MQ: 发送 OrderPaid 事件

        MQ->>FS: 消费事件
        FS->>WH: 创建履约单
        FS->>MQ: 发送 FulfillmentCreated

        OS-->>GW: 返回 200 Success
    end
    GW-->>PG: 200 Success（通知方要求必须返回200）
```

---

## 7. 非功能需求（NFR / SLA）

### 7.1 性能指标

> **说明**：xychart-beta为飞书不兼容Mermaid类型，改为表格描述（模板示例数据）。

**接口性能目标（P99响应时间 ms）**

| 接口        | P99 响应时间(ms) |
| :---------- | :--------------: |
| API-001创建 |       300        |
| API-002查询 |       100        |
| API-003取消 |       200        |
| API-004列表 |       150        |

| 指标项          | 目标值     | 测量方式              | 责任方 |
| :-------------- | :--------- | :-------------------- | :----- |
| 核心接口P99延迟 | ≤ 300ms    | APM监控（SkyWalking） | 后端   |
| 查询接口P99延迟 | ≤ 100ms    | APM监控               | 后端   |
| 并发处理能力    | ≥ 5000 TPS | 全链路压测            | 架构   |
| 数据库QPS       | ≥ 10000    | 慢查询监控            | DBA    |
| 缓存命中率      | ≥ 95%      | Redis监控             | 后端   |

### 7.2 可用性与可靠性

| 指标项     | 目标值                     | 实现方式                   |
| :--------- | :------------------------- | :------------------------- |
| 系统可用性 | ≥ 99.95%                   | 多活部署 + 自动故障转移    |
| 数据一致性 | 强一致性（订单/库存/支付） | 分布式事务（Seata AT模式） |
| 数据持久化 | RPO=0, RTO<<30s            | 主从同步 + 自动切换        |
| 降级能力   | 核心链路可降级             | 熔断（Sentinel）+ 兜底缓存 |

### 7.3 安全与合规

| 项         | 要求                            | 验证方式       |
| :--------- | :------------------------------ | :------------- |
| 传输加密   | TLS 1.3                         | SSL Labs扫描   |
| 敏感数据   | 手机号/身份证 AES-256加密存储   | 安全审计       |
| 防重放攻击 | 时间戳+随机数+签名，有效期5分钟 | 渗透测试       |
| 权限控制   | RBAC + 数据权限隔离             | 自动化权限扫描 |
| 审计日志   | 所有资金操作留痕，保留180天     | 日志审计       |

---

## 8. 验收标准（Acceptance Criteria）

### 8.1 功能验收（Given-When-Then）

| AC-ID  | 验收标准（Gherkin格式）                                                                                                                                    |   测试类型   | 通过标准 |
| :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------: | :------: |
| AC-001 | **Given** 用户已登录且购物车有2件商品<br>**When** 用户提交订单并选择有效地址<br>**Then** 系统创建状态为CREATED的订单<br>**And** 返回15分钟内有效的支付链接 |   集成测试   | 100%通过 |
| AC-002 | **Given** 商品库存仅剩1件<br>**When** 用户尝试购买2件<br>**Then** 系统拒绝下单<br>**And** 返回错误码400002<br>**And** 库存未被预占                         |   异常测试   | 100%通过 |
| AC-003 | **Given** 用户已提交订单未支付<br>**When** 15分钟后系统关单任务执行<br>**Then** 订单状态变为CLOSED<br>**And** 库存自动释放<br>**And** 优惠券自动返还       | 定时任务测试 | 100%通过 |
| AC-004 | **Given** 1000并发用户同时购买同一SKU<br>**When** 库存为500件<br>**Then** 成功订单数=500<br>**And** 无超卖现象<br>**And** 无重复扣款                       |   并发测试   | 100%通过 |
| AC-005 | **Given** 价格服务响应>500ms<br>**When** 用户提交订单<br>**Then** 系统使用缓存价格<br>**And** 订单创建成功<br>**And** 触发价格差异告警                     |   降级测试   | 100%通过 |

### 8.2 性能验收

| 验收项   | 场景                 | 目标                               | 测试工具       |
| :------- | :------------------- | :--------------------------------- | :------------- |
| 压测-001 | 创建订单接口         | 5000 TPS，P99<<300ms，错误率<<0.1% | JMeter/Gatling |
| 压测-002 | 混合场景（查/创/取） | 10000 TPS，系统负载<<70%           | 全链路压测平台 |
| 压测-003 | 数据库容量           | 单表1亿行，查询P99<<100ms          | 容量测试       |

---

## 9. 发布与灰度计划（Release Plan）

### 9.1 灰度策略

```mermaid
graph LR
    A[内测 / 1%员工与种子用户] --> B[白名单 / 10%特邀商家]
    B --> C[地域灰度 / 30%华南区用户]
    C --> D[全量发布 / 100%用户]
    D --> E[监控观察 / 72小时]

    A -->|观察3天 / 无P0 Bug| B
    B -->|观察5天 / 核心指标正常| C
    C -->|观察7天 / 无异常告警| D

    style A fill:#fff3e0,stroke:#e65100
    style D fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
```

### 9.2 发布检查清单

| 阶段   | 检查项                         | 负责人    | 状态 |
| :----- | :----------------------------- | :-------- | :--: |
| 发布前 | 代码Review通过（≥2人）         | Tech Lead |  ⬜  |
| 发布前 | 单元测试覆盖率≥80%             | 研发      |  ⬜  |
| 发布前 | 接口契约测试通过               | 测试      |  ⬜  |
| 发布前 | 数据库变更脚本评审通过         | DBA       |  ⬜  |
| 发布前 | 监控大盘/告警规则配置完成      | SRE       |  ⬜  |
| 发布中 | 蓝绿部署，流量切换10%→50%→100% | SRE       |  ⬜  |
| 发布后 | 核心接口P99延迟监控            | SRE       |  ⬜  |
| 发布后 | 错误率<<0.1%持续30分钟         | SRE       |  ⬜  |
| 发布后 | 业务指标（下单成功率）无下跌   | 产品      |  ⬜  |

### 9.3 回滚策略

| 触发条件          | 回滚动作                         | 回滚时间目标 | 负责人 |
| :---------------- | :------------------------------- | :----------- | :----- |
| P0 Bug影响>1%用户 | 立即切换流量至旧版本             | ≤ 5分钟      | SRE    |
| 性能下跌>50%      | 降级非核心链路，保留核心下单     | ≤ 3分钟      | SRE    |
| 数据库异常        | 暂停写入，切换只读模式，人工介入 | ≤ 10分钟     | DBA    |

---

## 10. 附录（Appendix）

- **附录A：** 数据库变更脚本（DDL/DML）
- **附录B：** 接口契约测试用例集
- **附录C：** 压测报告模板与历史基线
- **附录D：** 第三方服务对接文档（支付/物流/短信）
- **附录E：** 名词解释与数据字典

> **FRD 撰写原则（大厂标准）：**
>
> 1. **可测试性**：每个功能点必须对应至少一条 AC（验收标准）。
> 2. **可观测性**：每个接口必须定义 traceId、错误码、监控埋点。
> 3. **可回滚性**：每个变更必须考虑回滚方案，数据变更需兼容旧版本。
> 4. **防御性**：每个外部依赖必须有超时、熔断、降级策略。
> 5. **一致性**：状态机必须覆盖全生命周期，禁止出现"悬停状态"。
