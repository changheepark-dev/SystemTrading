from datetime import datetime, timedelta

def check_transaction_open():
    """현재 시간이 장 중인지 확인하는 함수 9:00 ~ 15:20"""
    now = datetime.now()
    start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=15, minute=20, second=0, microsecond=0)
    return not(start_time <= now <= end_time)


def check_transaction_closed():
    """현재 시간이 장이 끝난 시간인지 확인하는 함수 15:20 ~ 9:00"""
    now = datetime.now()
    start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=15, minute=20, second=0, microsecond=0)
    return (start_time < now < end_time)


def check_adjacent_transaction_closed():
    """현재 시간이 장 종료 부근인지 확인하는 함수(매수 조건 검색) 14:50 ~ 15:20"""
    now = datetime.now()
    base_time = now.replace(hour=14, minute=50, second=0, microsecond=0)
    end_time = now.replace(hour=15, minute=20, second=0, microsecond=0)
    return base_time <= now < end_time


def check_buy_timing():
    """현재 시간이 장 종료 부근인지 확인하는 함수(매수 주문) 15:10 ~ 15:20"""
    now = datetime.now()
    base_time = now.replace(hour=15, minute=10, second=0, microsecond=0)
    end_time = now.replace(hour=15, minute=20, second=0, microsecond=0)
    return base_time <= now < end_time


def check_before_open():
    """현재 시간이 장이 열리기 전 시간인지 확인하는 함수 15:20 ~ N 5:30"""
    now = datetime.now()
    before_open = now.replace(hour=5, minute=30, second=0, microsecond=0)

    if before_open < now:
        return datetime.now().strftime('%Y%m%d')
    else:
        return (datetime.now() - timedelta(1)).strftime('%Y%m%d')


def check_before_open_s():
    """서버 업데이트 전 시간인지 확인하는 함수 5:30 ~ 9:00"""
    now = datetime.now()
    before_open = now.replace(hour=5, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=9, minute=5, second=0, microsecond=0)

    return not(before_open <= now < end_time)


def check_open_second_gep():
    """현재 시간부터 장이 열리기 전 까지의 초 차이"""
    now = datetime.now()
    before_open = now.replace(hour=9, minute=0, second=0, microsecond=0)

    timegep = (before_open - now).seconds + 60
    if timegep >= 1200:
        return 1200
    else:
        return timegep