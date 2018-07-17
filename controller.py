#!/usr/bin/env python3

import time
import model
import view


def game_loop():
    user_input = view.main_menu()
    buy_inputs = ['b', 'buy']
    sell_inputs = ['s', 'sell']
    lookup_inputs = ['l', 'lookup']
    quote_inputs = ['q', 'quote']
    exit_inputs = ['e', 'exit']
    view_inputs = ['v', 'view']
    pl_inputs = ['p', 'p']
    acceptable_inputs = buy_inputs      \
        + sell_inputs   \
        + lookup_inputs \
        + quote_inputs  \
        + exit_inputs   \
        + view_inputs   \
        + pl_inputs
    on_off_switch = True
    while on_off_switch:
        if user_input.lower() in acceptable_inputs:
            if user_input.lower() in buy_inputs:
                (ticker_symbol, trade_volume) = view.buy_menu()
                x = model.buy(ticker_symbol, trade_volume)
                return x

            elif user_input.lower() in sell_inputs:
                (ticker_symbol, trade_volume) = view.sell_menu()
                x = model.sell(ticker_symbol, trade_volume)
                return x

            elif user_input.lower() in lookup_inputs:
                company_name = view.lookup_menu()
                x = model.lookup(company_name)
                return x

            elif user_input.lower() in quote_inputs:
                ticker_symbol = view.quote_menu()
                x = model.quote(ticker_symbol)
                return x

            elif user_input.lower() in view_inputs:
                balance = view.portfolio_menu()
                x = model.portfolio(balance)
                return x

            elif user_input.lower() in pl_inputs:
                p = view.pl_menu()
                x = model.pl(p)
                return x

            elif user_input.lower() in exit_inputs:
                break
                #on_off_switch = False
            else:
                print('Bad input. Restarting game in five seconds...')
                time.sleep(5)
                game_loop()
        else:
            return 'Plese Start Over'


if __name__ == '__main__':
    from pprint import pprint
    pprint(game_loop())
