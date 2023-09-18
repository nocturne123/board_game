from ENUMS import CardTypeEnum, CardStateEnum
import abc

# from player import Player

from transitions import Machine

"""卡牌的状态机实现"""

transtions = [
    {
        "trigger": "get_draw",
        "source": CardStateEnum.in_draw_pile,
        "dest": CardStateEnum.on_draw,
    },
    {
        "trigger": "get_into_hand",
        "source": CardStateEnum.on_draw,
        "dest": CardStateEnum.in_hand,
    },
    {
        "trigger": "get_played",
        "source": CardStateEnum.in_hand,
        "dest": CardStateEnum.on_use,
    },
    {
        "trigger": "choose_target",
        "source": CardStateEnum.on_use,
        "dest": CardStateEnum.on_choose_target,
    },
    {
        "trigger": "take_effect",
        "source": CardStateEnum.on_choose_target,
        "dest": CardStateEnum.taking_effect,
    },
    {
        "trigger": "get_equipped",
        "source": CardStateEnum.on_choose_target,
        "dest": CardStateEnum.on_equipment,
    },
    {
        "trigger": "get_discarded",
        "source": CardStateEnum.in_hand,
        "dest": CardStateEnum.on_discard,
    },
    {
        "trigger": "get_stolen",
        "source": CardStateEnum.in_hand,
        "dest": CardStateEnum.in_hand,
    },
    {
        "trigger": "get_unmounted",
        "source": CardStateEnum.on_equipment,
        "dest": CardStateEnum.on_discard,
    },
    {
        "trigger": "get_into_discard_pile",
        "source": CardStateEnum.on_discard,
        "dest": CardStateEnum.in_discard_pile,
    },
]


class Card(metaclass=abc.ABCMeta):
    """卡牌的基类，所有摸牌堆里的卡牌继承于此类"""

    def __init__(
        self,
        draw_pile,
        discard_pile,
        card_type: CardTypeEnum,
        states=CardStateEnum,
        transitions=transtions,
    ):
        self.distance_limited = True
        self.draw_pile = draw_pile
        self.discard_pile = discard_pile
        self.machine = Machine(
            model=self,
            states=states,
            transitions=transitions,
            initial=CardStateEnum.in_draw_pile,
        )
        self.card_type = card_type


if __name__ == "__main__":
    card1 = Card(None, None, CardTypeEnum.magic_attack)

    print(card1.state)
    card1.get_draw()
    print(card1.state)
