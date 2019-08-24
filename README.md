# chadan-helper

## Usage 使用方法

1. 将 `config.example.json` 重命名为 `config.json`。
2. 按照 [配置说明](#configuration-配置说明) 修改相应配置。
3. 执行 `python3 main.py` 或者双击打包好的 `main.exe`。

## Configuration 配置说明

- `accounts`: 账号信息部分，目前只支持茶蛋。
  - `platform`: 平台标识。
    - 必须以对应平台代称开头，如茶蛋账号必须以 `chadan` 开头。
    - 后面可以添加其它字符，如 `chadan1`，`chadantest` 等，不建议使用标点符号。
  - `username`: 用户名，通常为电话号码，如 `18912345678`。
  - `password`: 对应账号的密码。
  - `auto_confirmation`: 是否自动报单的开关。
  - `confirmation_delay`: 自动报单的延时，默认是500-600秒之间的随机数。
- `options`: 抢单配置，列表中的每一项对应一个抢单条目，每个条目由三个元素组成，格式为`[value, amount, operators]`。
  - `value`: 面额，应是对应平台支持的数值，如茶蛋平台应为 10, 20, 30, 50, 100, 200, 300, 500 中的一个。
  - `amount`: 想要抢的订单总数。
  - `operators`: 不同账号的运营商列表。
    - 不同账号用其 `platform` 的值为 key，对应的运营商列表为 value。
    - 运营商目前支持4种，分别用4个大写字母标识，`M` 是移动，`U` 是联通，`T`是电信，`S`是特价单。
    - 例如 `"chadan1" : "MUTS"`，表示 `chadan1` 对应的账号抢所有运营商的单子。
- `sleep_duration`: 每条抢单条目中不同账号运营商请求之间的间隔。
  - 注意: 这里的间隔指同一条目所有运营商请求之间间隔的总和，不同抢单条目之间互不影响。
- `sckeys`: 通过 [ServerChan](http://sc.ftqq.com/3.version) 实现微信通知的 key 列表。
  - 注意: 这里是一个列表，为了实现多个微信同时通知，格式为 `"sckeys": ["key2", "key2"]`。
- `check_time`: 是否检查时间的开关，在非设定时间将不进行抢单。
- `start_time`: 开始抢单的时间，请勿修改格式，否则会影响解析。
  - 注意：这里是UTC时间，北京时间需减去8小时，如北京时间上午7点应设置为23:00。
- `end_time`: 结束抢单的时间，注意事项同 `start_time`。
