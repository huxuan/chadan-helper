# chadan-helper

## Usage 使用方法

1. 将 `config.json.example` 重命名为 `config.json`。
2. 按照 [配置说明](#configuration-配置说明) 修改相应配置。
3. 执行 `python3 main.py` 或者双击打包好的 `main.exe`。

## Configuration 配置说明

- `username`: 用户名，通常为电话号码，如18912345678。
- `password`: 密码。
- `options`: 抢单配置，一行对应一个抢单条目，每个条目由三个元素组成，格式为`[value, amount, operators]`。
  - `value`: 面额，如10, 20, 30, 50, 100, 200, 300, 500。
  - `amount`: 数量，需注意级别黄金及以下的只能为1，否则会出错。
  - `operators`: 运营商列表。
    - 目前支持4种: 移动 `MOBILE`, 联通 `UNICOM`, 电信 `TELECOM`, 特价单 `SPECIAL`。
    - 例如 `["MOBILE", "UNICOM", "TELECOM", "SPECIAL"]`。
- `auto_confirmation`: 是否自动报单的开关。
- `confirmation_delay`: 自动报单的延时，默认是500-600秒直接的随机数。
- `sleep_duration`: 每条抢单条目中请求之间的间隔
  - 注意: 不同抢单条目之间互不影响。
- `sckeys`: 通过 [ServerChan](http://sc.ftqq.com/3.version) 实现微信通知的 key 列表。
  - 注意: 这里是一个列表，为了实现多个微信同时通知，格式为 `“sckeys”: ["key2", "key2"]`。
- `check_time`: 是否检查时间的开关，在非设定时间将不进行抢单。
- `startTime`: 开始抢单的时间，请勿修改格式，否则会影响解析。
  - 注意：这里是UTC时间，北京时间需减去8小时，如北京时间上午7点应设置为23:00。
- `endTime`: 结束抢单的时间，注意事项同 `startTime`。
