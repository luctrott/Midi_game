from Game import Game
from flügel import main
from threading import Thread
import time

class Main:
    def __init__(self) -> None:
        self.game=Game()
        self.game.lcd.backlight_enable=True
        print("game done")
        self.main=main(game=self.game)
        a=self.main._game
        self.thread=Thread(target=self.run_logic)
        self.thread.start()
        print("init done")
        self.game.run()
    
    def run_logic(self)->None:
        #TODO
        while self.game.running:
            time.sleep(1)
        self.main.close()

if __name__ == "__main__":    
    a=Main()