import sentry_sdk
def main():
    print("Hello from sentry-test!")
    division_by_zero = 1 / 0



sentry_sdk.init(
    dsn="https://7d4d087faa404bd5e11792526ab12705@o4509191222460416.ingest.us.sentry.io/4509191229538304",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

if __name__ == "__main__":
    main()
