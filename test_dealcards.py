import socket
import sys
import pickle
from card_vars import ranks, suits, card, deck, deck_dealing, decl_values, card_vals, hierarchy_
from random import choice, shuffle 
from itertools import chain
import threading
import time
import re

def dealCards(clients):
    
    """
    Messages are separated by b'|'
    """
    
    all_data = b''    
    
    # stage 1. deal cards and pick trump suit 
    trump = ''
    
    #rand_trump = choice(deck_dealing)
    rand_trump = card(Rank='A', Suit='Hearts')
    print(f'rand_trump is {rand_trump}')
       
    first_hand = [[card(Rank='7', Suit='Hearts'), card(Rank='8', Suit='Hearts')]]
    
    client_hand_dict = {}
    
    for client, hand in zip(clients, first_hand):
        client_hand_dict[client] = hand
        client.sendall(pickle.dumps(['hand 1', hand]) + b'|')
        print('sent hand')
        client.sendall(pickle.dumps(['rand_trump', rand_trump]) + b'|')
        print('sent rand_trump')       
    
    # # players chose whether to play randomly chosen trump suit                   
    # for client in clients:
    #     client.sendall(pickle.dumps({'pick_trump': 1}) + b'|')
    #     print(f'client {client}\'s turn to pick trump')
        
    #     while 1:
    #         data = client.recv(1024)
    #         all_data += data
            
    #         if data and b'|' in all_data:
    #             to_analyse = pickle.loads(all_data[:all_data.index(b'|')])
    #             print(to_analyse)
    #             all_data = all_data[all_data.index(b'|') + 1:]
                
    #             if to_analyse == 'play' or to_analyse == rand_trump[1]:
    #                 trump = rand_trump[1]
    #                 trump_client = client 
    #                 print(f'{client} picked trump suite: {trump}')
    #                 for i in clients:
    #                     i.sendall(pickle.dumps(f'client {client} has picked trump suit {trump}') + b'|')
    #                     i.sendall(pickle.dumps({'trump': trump}) + b'|')

    #                 # if trump suit is picked deal the second round of cards (3 cards to each player)
                    
    #                 #second_hand = secondRoundHand()
                    
    #                 secondee = [[card(Rank='Q', Suit='Diamonds'), card(Rank='K', Suit='Diamonds'), card(Rank='A', Suit='Diamonds')],
    #                            [card(Rank='Q', Suit='Spades'), card(Rank='K', Suit='Spades'), card(Rank='A', Suit='Spades')],
    #                            [card(Rank='Q', Suit='Clubs'), card(Rank='K', Suit='Clubs'), card(Rank='A', Suit='Clubs')]]
    #                 second_hand = secondee, [card(Rank='Q', Suit='Hearts'), card(Rank='K', Suit='Hearts')]
                    
    #                 client_hand_dict[client] += second_hand[1] + [rand_trump]
    #                 client.send(pickle.dumps({'hand 2': client_hand_dict[client]}) + b'|')
                    
                      
    #                 for j, k in zip([l for l in clients if l != client], second_hand[0]):
    #                     client_hand_dict[j] += k
    #                     # send the cards to each player
    #                     j.send(pickle.dumps({'hand 2': client_hand_dict[j]}) + b'|')
                            
    #                 return tricks(clients, trump, trump_client, client_hand_dict)
    #                 #return declInput(clients, trump, trump_client, client_hand_dict)
    #             else: 
    #                 break

    
    # # if all players pass on the random trump suit, free for all 
    # if not trump:
    #     for client in clients:
    #         client.send(pickle.dumps({'pick_trump': 2}) + b'|')
    #         [i.send(pickle.dumps(f'client {client} turn to declare') + b'|') for i in clients if i != client]
    #         while 1:
    #             data = client.recv(1024)
    #             all_data += data
            
    #             if data and b'|' in all_data:
    #                 to_analyse = pickle.loads(all_data[:all_data.index(b'|')])
    #                 print(to_analyse)
    #                 all_data = all_data[all_data.index(b'|') + 1:]
    #                 if pickle.loads(data) in suits:
    #                     trump = pickle.loads(data)
    #                     trump_client = client
    #                     for i in clients:
    #                         i.sendall(pickle.dumps(f'client {client} has picked trump suit {trump}') + b'|')
    #                         i.sendall(pickle.dumps({'trump': trump}) + b'|')
                        
    #                     break                     
                    
    #                 # when all players pass on picking a trump suit deal the cards again. **** Next player needs to deal ****
    #                 elif client == clients[-1]:
    #                     return deal_cards(clients)
                               
    #             else:
    #                 break
 
    # second_hand = secondRoundHand()
       
        
    # client_hand_dict[trump_client] += second_hand[1] + [rand_trump]    
    # trump_client.send(pickle.dumps({'hand 2': client_hand_dict[trump_client]}) + b'|')

    # for j, k in zip([l for l in clients if l != client], second_hand[0]):
    #     client_hand_dict[j] += k
    #     # send the cards to each player
    #     j.send(pickle.dumps({'hand 2': client_hand_dict[j]}) + b'|')

    return None
    #return declInput(clients, trump, trump_client, client_hand_dict)

host = ''
port = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('socket created')

try:
    s.bind((host, port))
except socket.error:
    sys.exit()
    
print('Socket has been bound')

s.listen(5)
print('socket is ready')

clients = []
    
while 1:
    conn, addr = s.accept()
    clients.append(conn)

    # clients[conn] = id(conn)
    print('connected to client {} {}:{}'.format(id(conn), addr[0], addr[1]))
    
    if len(clients) > 0:
        print('\n****starting session****\n')
        
        shuffle(clients) # shuffle players around
        dealer = choice(clients) # pick the player who will deal the cards
        
        dealCards(clients) 