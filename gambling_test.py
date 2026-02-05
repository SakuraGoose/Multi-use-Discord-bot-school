#!/usr/bin/env python3
from Gambling import Coinfilp, Dice


def test_coin():
    print("Coinflip tests:")
    for choice in ["heads", "tails"]:
        game = Coinfilp(user_id=1, bet=10, choice=choice)
        text, payout = game.play()
        print(text)


def test_dice():
    print("\nDice tests:")
    for _ in range(5):
        game= Dice(user_id=1, bet=10)
        text, payout = game.play()
        print(text)


if __name__ == '__main__':
    test_coin()
    test_dice()

