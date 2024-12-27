# 存一個人的資料
class Player:
    def __init__( self, user_id: int, user_name: str ):
        # ID
        self.player_id = user_id

        # 名字
        self.player_name = user_name

        # 總抽卡次數
        self.gamble_times = 0

        # 抽卡紀錄
        self.gamble_times_detail = []

        # 抽卡結果
        self.gamble_history = []

        # 剩餘點數
        self.coins = 0

        # 上次簽到時間
        self.last_sign_time = None

    # 將 Player 物件轉換為字典
    def to_dict( self ):
        return {
            'player_id': self.player_id,
            'player_name': self.player_name,
            'gamble_times': self.gamble_times,
            'gamble_times_detail': self.gamble_times_detail,
            'gamble_history': self.gamble_history,
            'coins': self.coins,
            'last_sign_time': self.last_sign_time.isoformat() if self.last_sign_time else None
        }
    
    # 將 Player 物件的資料轉回 Player 型別
    @classmethod
    def from_dict( cls, data ):
        player = cls( data['player_id'], data['player_name'] )
        player.gamble_times = data.get( 'gamble_times', 0 )
        player.gamble_times_detail = data.get( 'gamble_times_detail', [] )
        player.gamble_history = data.get( 'gamble_history', [] )
        player.coins = data.get( 'coins', 0 )
        player.last_sign_time = data.get( 'last_sign_time', None )
        return player
