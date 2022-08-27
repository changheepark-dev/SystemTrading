from util.db_helper import *
from universe.make_up_universe import *
import sqlite3
from strategy.RSIStrategy import *
#
# universe_df = pd.DataFrame({
#                 'code': '156',
#                 'code_name': '44',
#                 'created_at': '555'
#             })
#
#             # universe라는 테이블명으로 Dataframe을 DB에 저장함
# insert_df_to_db('oder', 'hgjkhkhl', universe_df)
# last_order_check("buy", '005640', 3544.44)

# aaaa = {}

# sql = .format('buy')
#
# cur = execute_sql('C:/TR/SystemTrading/strategy/LOC', 'select * from buy')
# cols = [column[0] for column in cur.description]
#
# # 데이터베이스에서 조회한 데이터를 DataFrame으로 변환해서 저장
# df = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)
#
# df['rank'] = df['score'].rank(method='first')
# df = df.sort_values(by=['rank'])
#
# print()
#
#
#
# print(df)
RSIStrategy.order_buy('RSIStrategy')





















# # 매수 대상인지 확인하고 주문을 접수하는 함수 ==================================================================================
#     def check_buy_signal_and_order(self, code):
#         """매수 대상인지 확인하고 주문을 접수하는 함수"""
#         # 매수 가능 시간 확인
#         # if not check_adjacent_transaction_closed():
#         #     return False
#
#         universe_item = self.universe[code]
#
#         # (1)현재 체결정보가 존재하지 않는지 확인
#         if code not in self.kiwoom.universe_realtime_transaction_info.keys():
#             # 존재하지 않다면 더이상 진행하지 않고 함수 종료
#             print("매수대상 확인 과정에서 아직 체결정보가 없습니다.")
#             return
#
#         # (2)실시간 체결 정보가 존재하면 현 시점의 시가 / 고가 / 저가 / 현재가 / 누적 거래량이 저장되어 있음
#         open = self.kiwoom.universe_realtime_transaction_info[code]['시가']
#         high = self.kiwoom.universe_realtime_transaction_info[code]['고가']
#         low = self.kiwoom.universe_realtime_transaction_info[code]['저가']
#         close = self.kiwoom.universe_realtime_transaction_info[code]['현재가']
#         volume = self.kiwoom.universe_realtime_transaction_info[code]['누적거래량']
#
#         # 오늘 가격 데이터를 과거 가격 데이터(DataFrame)의 행으로 추가하기 위해 리스트로 만듦
#         today_price_data = [open, high, low, close, volume]
#
#         df = universe_item['price_df'].copy()
#
#         # 과거 가격 데이터에 금일 날짜로 데이터 추가
#         df.loc[datetime.now().strftime('%Y%m%d')] = today_price_data
#
#         # (3)매수 신호 확인(조건에 부합하면 주문 접수)
#         if check_bay(df, today_price_data, code):
#             # (4)이미 보유한 종목, 매수 주문 접수한 종목의 합이 보유 가능 최대치(10개)라면 더 이상 매수 불가하므로 종료
#             if (self.get_balance_count() + self.get_buy_order_count()) >= 10:
#                 return
#
#             # (5)주문에 사용할 금액 계산(10은 최대 보유 종목 수로써 consts.py에 상수로 만들어 관리하는 것도 좋음)
#             budget = self.deposit / (10 - (self.get_balance_count() + self.get_buy_order_count()))
#
#             # 최우선 매도호가 확인
#             bid = self.kiwoom.universe_realtime_transaction_info[code]['(최우선)매수호가']
#
#             # (6)주문 수량 계산(소수점은 제거하기 위해 버림)
#             quantity = math.floor(budget / bid)
#
#             # (7)주문 주식 수량이 1 미만이라면 매수 불가하므로 체크
#             if quantity < 1:
#                 return
#
#             # (8)현재 예수금에서 수수료를 곱한 실제 투입금액(주문 수량 * 주문 가격)을 제외해서 계산
#             amount = quantity * bid
#             self.deposit = math.floor(self.deposit - amount * 1.00015)
#
#             # (8)예수금이 0보다 작아질 정도로 주문할 수는 없으므로 체크
#             if self.deposit < 0:
#                 return
#
#             # (9)계산을 바탕으로 지정가 매수 주문 접수
#             if method_buy:
#                 order_result = self.kiwoom.send_order('send_buy_order', '1001', 1, code, quantity, bid, '00')
#             else:
#                 order_result = self.kiwoom.send_order('send_buy_order', '1001', 1, code, quantity, 0, '03')
#
#             # _on_chejan_slot가 늦게 동작할 수도 있기 때문에 미리 약간의 정보를 넣어둠
#             self.kiwoom.order[code] = {'주문구분': '매수', '미체결수량': quantity}
#
#             # # LINE 메시지를 보내는 부분
#             # message = "[{}]buy order is done! quantity:{}, bid:{}, order_result:{}, deposit:{}, get_balance_count:{}, get_buy_order_count:{}, balance_len:{}".format(
#             #     code, quantity, bid, order_result, self.deposit, self.get_balance_count(), self.get_buy_order_count(),
#             #     len(self.kiwoom.balance))
#             # send_message(message, RSI_STRATEGY_MESSAGE_TOKEN)
#
#         # 매수신호가 없다면 종료
#         else:
#             return