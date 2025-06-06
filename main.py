import sentry_sdk

def calculate_average(numbers):
    if not numbers: # Check if the list is empty
        print("提示：数字列表为空，无法计算平均值。返回 0.0。")
        return 0.0
    # Original calculation
    return sum(numbers) / len(numbers)

def main():
    print("Hello from sentry-test!")
    
    # 尝试计算平均值，可能触发除零异常
    user_input = input("请输入一些数字，用逗号分隔(或直接按回车使用空列表): ")
    
    numbers = []
    if user_input.strip():
        # Replace spaces with commas for flexible splitting
        processed_input = user_input.replace(' ', ',')
        
        potential_numbers = processed_input.split(',')
        for item in potential_numbers:
            item_stripped = item.strip()
            if item_stripped:
                try:
                    numbers.append(float(item_stripped))
                except ValueError:
                    print(f"警告：输入 '{item_stripped}' 不是有效的数字，将被忽略。")
    
    try:
        avg = calculate_average(numbers)
        print(f"平均值是: {avg}")
    except Exception as e:
        print(f"计算平均值时出错: {e}")

sentry_sdk.init(
    dsn="https://7d4d087faa404bd5e11792526ab12705@o4509191222460416.ingest.us.sentry.io/4509191229538304",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

if __name__ == "__main__":
    main()
