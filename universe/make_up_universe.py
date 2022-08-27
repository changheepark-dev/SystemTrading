# 유니버셜 생성

from util.execute_crawler import *

def get_universe():

    # 크롤링 결과를 불러옴
    days = [' (월)', ' (화)', ' (수)', ' (목)', ' (금)', ' (토)', ' (일)']
    now = datetime.now().strftime("%Y-%m-%d")
    savepoint = "C:/TR/SystemTrading/util/date/" + now + days[datetime.today().weekday()] + ".xlsx"

    try:                                                                                # 크롤링 결과가 없으면 생성후 조회
        df = pd.read_excel(savepoint)
    except FileNotFoundError:
        execute_crawler()
        df = pd.read_excel(savepoint)




    mapping = {',': '', 'N/A': '0'}
    df.replace(mapping, regex=True, inplace=True)

    # 사용할 column들 설정
    cols = ['거래량', '매출액', '매출액증가율', 'ROE', 'PER']

    # column들을 숫자타입으로 변환(Naver Finance를 크롤링해온 데이터는 str 형태)
    df[cols] = df[cols].astype(float)

    # 유니버스 구성 조건 (1)~(4)를 만족하는 데이터 가져오기
    df = df[(df['거래량'] > 0) & (df['매출액'] > 0) & (df['매출액증가율'] > 0) & (df['ROE'] > 0) & (df['PER'] > 0) & (~df.종목명.str.contains("지주")) & (~df.종목명.str.contains("홀딩스"))]

    # PER의 역수
    df['1/PER'] = 1 / df['PER']

    # ROE의 순위 계산
    df['RANK_ROE'] = df['ROE'].rank(method='max', ascending=False)

    # 1/PER의 순위 계산
    df['RANK_1/PER'] = df['1/PER'].rank(method='max', ascending=False)

    # ROE 순위, 1/PER 순위 합산한 랭킹
    df['RANK_VALUE'] = (df['RANK_ROE'] + df['RANK_1/PER']) / 2

    # RANK_VALUE을 기준으로 정렬
    df = df.sort_values(by=['RANK_VALUE'])

    # 필터링한 데이터프레임의 index 번호를 새로 매김
    df.reset_index(inplace=True, drop=True)

    # 상위 200개만 추출
    df = df.loc[:numbers -1]

    # 유니버스 생성 결과를 엑셀 출력
    df.to_excel('c:/TR/SystemTrading/universe/universe_date/universe.xlsx')

    return df['종목명'].tolist()


if __name__ == "__main__":
    print('Start!')
    universe = get_universe()
    print(universe)
    print('End')