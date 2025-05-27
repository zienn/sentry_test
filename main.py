import sentry_sdk

class MyFormatter:
    def format(self, data):
        # 简单的格式化方法
        return data

class DataProcessor:
    def __init__(self, config=None):
        self.config = config if config is not None else {}
        # 初始化formatter属性，以防止AttributeError
        if self.config.get('enable_formatting'):
            self.formatter = MyFormatter()
        else:
            self.formatter = None
    
    def process_data(self, data):
        result = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'divisor' in value:
                divisor = value['divisor']
                # 修复逻辑：仅当除数不为0时执行除法
                if divisor != 0:
                    result[key] = 100 / divisor
                else:
                    result[key] = None
            elif isinstance(value, list):
                result[key] = [item * 2 for item in value]
            else:
                result[key] = value
        
        return self._post_process(result)
    
    def _post_process(self, result):
        # 如果启用了格式化，使用formatter处理结果
        if self.config.get('enable_formatting'):
            return self.formatter.format(result)
        return result

def main():
    print("你好，来自sentry-test！")
    
    # 测试数据，包含一个除数为0的项
    sample_data = {
        "item1": {
            "divisor": 0,
            "value": 42
        },
        "item2": {
            "divisor": 2,
            "value": 100
        },
        "item3": [1, 2, 3]
    }
    
    # 使用启用格式化的配置创建处理器
    processor = DataProcessor(config={'enable_formatting': True})
    processed = processor.process_data(sample_data)
    
    print("处理结果:", processed)

sentry_sdk.init(
    dsn="https://7d4d087faa404bd5e11792526ab12705@o4509191222460416.ingest.us.sentry.io/4509191229538304",
    # 添加用户数据如请求头和IP，
    # 详情请见 https://docs.sentry.io/platforms/python/data-management/data-collected/
    send_default_pii=True,
)

if __name__ == "__main__":
    main()
