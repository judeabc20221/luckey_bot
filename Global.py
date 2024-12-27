import pytz

import os
from apscheduler.schedulers.background import BackgroundScheduler

class Global:
    # 機率
    chance = [ 0.8, 0.1, 0.09, 0.009, 0.001 ]
    
    # 輸出的emoji
    emoji = [ ':military_medal:', ':third_place:', ':second_place:', ':first_place:', ':gem:' ]

    # 所有資料
    player_data = {}

    # 排程器
    scheduler = BackgroundScheduler( timezone="Asia/Taipei" )

    # 身分組
    gamble_role = int( os.getenv( 'role' ) )

    # 頻道
    gamble_channel = int( os.getenv( 'channel' ) )

    # 時區
    timezone = pytz.timezone( 'Asia/Taipei' )