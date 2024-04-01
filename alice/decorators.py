def is_auth(func):
    def wrapper():
        print('BEFORE FUNC')
        func()
        print('AFTER FUNC')
    return