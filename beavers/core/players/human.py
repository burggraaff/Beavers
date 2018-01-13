from .player import Player


class Human(Player):
    def play(self, r):
        do = input(f"{self.name}, what do you want to do? (D: {r.stack.disc_top()})\n")
        if do == "new":
            new_card = r.stack.give()
            do_new = input(f"Replace card with {new_card}? 'no' if not\n")
            if do_new == "no" or do_new == "":
                r.stack.discard(new_card)
            else:
                index = int(do_new) - 1
                to_discard = self.hand[index]
                self.hand[index] = new_card
                r.stack.discard(to_discard)
        elif do == "open":
            index = int(input("Replace which card?\n")) - 1
            to_discard = self.hand[index]
            self.hand[index] = r.stack.give_from_discard()
            r.stack.discard(to_discard)
        else:
            pass
        if r.ender is None:
            end = bool(input("End round?\n"))
            if end:
                r.ender = self
                print(f"{self.name} is ending the round!")
        print(self.hand, r.stack)
