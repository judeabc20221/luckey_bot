import json

from datetime import datetime

from Global import Global
from Player import Player

class Backup():
    def backup():
        transfer = {}
        for key, value in Global.player_data.items():
            transfer[key] = value.to_dict()

        with open( f"player_data.json", "w", encoding = "utf-8" ) as file:
            json.dump( transfer, file, ensure_ascii = False, indent = 4 )
        
        current = datetime.now( Global.timezone )
        current = current.strftime("%Y-%m-%d %H:%M:%S")
        print( f"已備份完成 完成時間:{current}" )

    def restore():
        try:
            with open( f"player_data.json", "r", encoding = "utf-8" ) as file:
                data = json.load( file )
            
            restore_data = {}
            for key, value in data.items():
                restore_data[ int( key ) ] = Player.from_dict( value )
            Global.player_data = restore_data
        except FileNotFoundError:
            print( "備份檔案未建立" )
            pass
