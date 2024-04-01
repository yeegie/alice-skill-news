from typing import Optional
import random

class WordGenerator:
    __secret = 'яблоко стол книга машина кот пальма океан звезда печенье солнце мост дом ручка радуга гитара бабочка кофе сумка вода космос шарик карандаш луна пальто облако ветер ковер котенок дерево камень телефон окно чашка собака лампа планета пицца чайник компьютер зонт телевизор птица змея медведь фонарь фрукт сумка камера платье рука море огонь бутылка шкаф дверь сапоги котлета стул попугай конфеты деревня холодильник банан книжка огурец коробка фонарик картина подушка кружка ключи кресло ваза радио кровать шоколад чемодан картошка торт печка банк глаз карман пирог ложка лягушка вилка курица птицы попугаи звонок камень кольцо газета браслет перец радость сладкое муха мясо сахар кошка лиса плита рис песок торт рюкзак дракон гора воздух крыша корзина воздушный шар бабах хлеб куртка сумка пудинг кот крыло цветок шарик котлета птица голова пицца молоко диск мотоцикл снег солнце брюки стенка сыр блин ролик велосипед конь молоко плита пудинг груша сахар соль шарф футболка брелок шоколад сыр мяч сок стакан тело краска цепь лук водопад хлеб чай яйцо пирог бутылка фантастик лампа бутерброд котлета радуга соль ведро банан весло белка вилка банк машина ботинок бутылка вода вилка гриб блин дверь дом заяц зеркало игра камень кровать лес муха облако очки пасха пирог река роза свеча свинья семена солнце соль стол стул суп трава туман фонарь хлеб холодильник цветок чай чашка часы черешня яблоко ананас арбуз банан блин ветер вино вода груша домик картофель кинза котлета лимон масло молоко мороженое огурец оливки помидор рис соль торт хлеб шоколад шпинат яблоко автомобиль акула бабочка банан велосипед вертолет волк воробей ворон гиббон гора гусь гусятница дельфин ежик заяц карандаш кедр кенгуру киви клавиатура клоун книга кольцо конфета кот котлета курица лама лимон лиса луна лягушка макароны медведь медуза мишень монитор морковь мороз мороженое муха носорог обезьяна овца огонь огурец окно оливки осел пальма паук перец пицца пиццерия попугай портфель пуля радуга радуга ромашка рыба салат самолет самолет сахар свет свеча снег собака сова сок солнце стол страус сумка суши сыр торт торт туфля тюльпан утка утюг фламинго фонарь фрукты холодильник хомяк цветок чай часы шапка шоколад яблоко яйцо ящик апельсин банан груша карандаш книга кот котлета кровать машина мяч огурец пицца сок стол торт утка чашка шоколад'
    __words = __secret.split(' ')

    @classmethod
    def generate(cls, words: Optional[int] = 2) -> str:
        selected_words = []
        for i in range(words):
            selected_words.append(random.choice(cls.__words))
        return ' '.join(selected_words)