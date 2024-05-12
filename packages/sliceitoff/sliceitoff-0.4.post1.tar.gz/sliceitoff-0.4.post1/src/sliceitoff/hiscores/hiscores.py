""" hiscores.hiscores - high socres: loading, saving, converting to string """

from sliceitoff.settings import settings
from .static import MAX_HIGHSCORES

class HiScores:
    """ Keeps track of high scores """
    def __init__(self):
        """ On creation load high scores from config file """
        self.table=[]
        for value in settings.get_values("hiscore"):
            try:
                score, name = value.split('!')
                self.add(int(score.strip()),name.strip())
            except ValueError:
                pass
        if len(self.table)<MAX_HIGHSCORES:
            self.table+=[(0,"") for _ in range(MAX_HIGHSCORES-len(self.table))]

    def add(self, score, initials):
        """ Add new high score and reranks top """
        self.table.append( (score, initials) )
        self.table.sort(reverse=True)
        self.table = self.table[:MAX_HIGHSCORES]

    def high_enough(self, score):
        """ Score is enough to make high scores """
        return self.table[-1][0] < score

    def save(self):
        """ Save current high scores """
        settings.replace_values(
                "hiscore",
                [f"{score}!{name}" for score, name in self.table])

    def __str__(self):
        text = (
                "      "
                "\xeeH\xecI\xedG\xe9H "
                "\xeaS\xedC\xeeO\xebR\xe9E\xecS\xeb!\xed!\n\n")
        half = len(self.table) // 2
        for i in range(half):
            text += (
                    f"\xed{self.table[i][1]:<3s} "
                    f"\xef{self.table[i][0]:07}  "
                    f"\xed{self.table[i+half][1]:<3s} "
                    f"\xef{self.table[i+half][0]:07}\n")
        return text


# Initialize only one time
try:
    # pylint: disable = used-before-assignment
    # This is intented behaviour
    hi_scores
except NameError:
    hi_scores = HiScores()
