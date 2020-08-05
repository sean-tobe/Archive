# SEAN TOBE
# 05/15/2018
# VIS141A P1
# source code from smallsurething, updated by sean tobe
import re
import random
import socket
import time
import sqlite3

server_address = ('localhost', 9999)
max_size = 4096

orders = dict()					# pair customer name and order string
substep = dict()				# pair customer name and number of steps through the sandwich-making process (size, bread, proteins, veggies, toppings)
sales = 0						# 

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}
 
psychobabble = [
    [r'(.*)\b(?:order|want|get|have|need|add|select|choose|like)\b (.*)',
     ['Which bread do you want?',
      'What proteins should I add?',
      'What veggies would you like?',
      'Choose any toppings or condiments you can think of!',
      'Please confirm your custom sub.']],

    [r'(.*)\b(?:begin|start|go|yes)\b(.*)',
     ['What size sandwich?',
      'Would you like to make that a mini or extra large size?',
      'Please choose a sub size.']],
    
    [r'(.*)\b(?:confirm|no)\b(.*)',
     ['Goodbye! and Eat Fresh!',
      'Another great person, please come back again!',
      'Thanks for choosing MiPik Subs!']],
    
    [r'(.*)',
     ['What would you like on your perfect sub?',
      "I'm the best sandwich artist.",
      'Is {0} a type of sandwich?',
      'Can I start a sub order for you?']]
]

#REFLECTIONS
def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)
 
#TRANSLATIONS
def talk(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))                                                               # strips of extraneous (!)
        if match:
            response = random.choice(responses)                                                                         # select random resp
            print('not an order..')
            return response.format(*[reflect(g) for g in match.groups()])    

def order(statement, name):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))                                                               # strips of extraneous (!)
        if match:
            response = responses[substep[name]]
            #print(substep[name])
            #response = random.choice(responses)    # select random resp
            return response.format(*[reflect(g) for g in match.groups()])    

def updateOrders(t_name, s_msg):
    if t_name not in orders:                                                                    # if customer is not in the database, register their name and order message in the dictionary
        orderup = {t_name: s_msg}                                                               # initialize dictionary entry and update orders
        orders.update(orderup)
        substep.update({t_name: int(0)})                                                        # update substep of customer, to progress MiPik's conversation as the order moves down the sub-line
        print('dicts init')
    elif t_name in orders:  
        orderold = str(orders[t_name])                                                          # if customer is adding to their order, join their last order message with the new one and update orders
        orderup = {t_name: ''.join((orderold,",",s_msg))}
        orders.update(orderup)
        if substep[t_name] <= 3:                                                                # maximum of 5 (0-4) substeps (size, bread, protein, veggie, topping)
            subup = substep[t_name] + 1                                                         # increment substep through the sub designing process and update dictionary
            subnew = {t_name: subup}
            substep.update(subnew)

def closeOrder(t_name):          																 		# this means the customer has gone through the sandwich-making process 
    try:                                                                                                # and deletes the entry, so the employee can start on a new customer's order.
        del orders[t_name]
        del substep[t_name]
        print('confirmed sale!') 
        sales + 1   
    except KeyError:
        pass
        print('could not close the transaction')                                                              
    

def main():
    print("MAKE SANDWICHES!")
    print(orders)
    print(substep)
    while True:                                                                                                         # loop forever every time.sleep(7)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                       # initialize socket
        if len(orders) == 0:                                                                                                            
            client.sendto(("MiPik|everyone|Here at MiPik Subs, we make all your sandwich dreams come true! %d total sales so far!" % (sales)).encode(), server_address)   # if no orders are in the dict,
            time.sleep(21)																																				   #  advertise in chat every sleep(30)
        data, server = client.recvfrom(max_size)                                                                        # collect data from chat
        for line in data.decode().split('\n'):                                                                          # iterate through each line while decode() and split('\n')
            print()
            print(line)
            match = re.search(r'(.*)\|MiPik\|(.*)', line)                                                               # match if line matches *|MiPik|* [a user is talking to MiPik bot]
            if match:																									#
                t_name = match.expand(match.group(1))                                                                   ##t_name = from customername, t_msg = message
                t_msg = match.expand(match.group(2))                                                                    
                s_order = re.match(r'(.*)\b(?:order|want|get|have|need|add|select|choose|like)\b(.*)', t_msg.rstrip('.!'))   ##s_order: check if message is an order command, words like (I want, Let me get,)    
                s_confirm = re.match(r'(.*)\b(?:confirm|done|finish|end|exit|quit)\b(.*)', t_msg.rstrip('.!'))               ##s_confirm: check if message is a confirm command
                if s_confirm:																							# if message is a confirm command,
                    closeOrder(t_name)
                    continue																							# skip to next customer [not an order or talk]
                if s_order:                                                                                             	 
                    print('order UP!')
                    s_msg = s_order.expand(s_order.group(2))                                                            ##s_msg = order command message
                    updateOrders(t_name, s_msg)
                    time.sleep(5)                                                                                       # sleep(5) to mimik applying sandwich updates
                    client.sendto(("MiPik|%s|I've got your%s custom sub..%s" %  (t_name,orders[t_name],order(t_msg,t_name))).encode(), server_address)  # send to server: mimik the customer's order of the sub 
                    																																	#  by dictionary lookup and respond with order()

                    #client.sendto(("MiPik|%s|%s" % (t_name,order(t_msg,t_name))).encode(), server_address)                 		 # also respond to order commands and progress through the conversation
                    print(orders)
                    #print(substep)
                else:                                                                                  					# if customer doesn't use order commands, translate for normal talk
                    t_name = match.expand(match.group(1))                                                               ##t_name = from customer name, t_msg = stranger talking [not a registered customer yet
                    t_msg = talk(match.expand(match.group(2)))  
                    time.sleep(7)                                                                                       # sleep(5), employees are working but they'll still respond in time
                    client.sendto(('MiPik|%s|%s' % (t_name,t_msg)).encode(), server_address)                            # send to server: MiPik's Eliza-like 'psychobabble' reflections
                                                                                       # increment total sales
        client.close()
        time.sleep(10)                                                                                                  # sleep(10)

 
if __name__ == "__main__":
    main()
