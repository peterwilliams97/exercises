'''
Scenario:
Period Home Builders (PHB) are a large organization involved in building new homes. They have registered suppliers who supply 
building materials such as cement, bricks, timber, etc. These suppliers are located in different cities of the state. More 
than one supplier is located in a given city. PHB require building materials delivered to construction sites, located in 
different cities of the state.
Currently, when a certain item is required, PHB employees use phone calls to contact several suppliers inquiring about the 
availability of the item. To reduce the complexity of the ordering process, PHB decided to use an Agent Driven Ordering System.
Approach
In the ordering system, each supplier is represented by a Supplier Agent. Each Supplier Agent maintains a catalogue of 
available items, the number of each item in stock and their prices. Each PHB employee is represented by a Personal Agent. 
When a PHB employee requires an item delivered, he/she invokes a Personal Agent specifying the item and quantity required. 
The Personal Agent makes a request providing the item name and quantity to all the Supplier Agents.
If a sufficient number of the item is available in their catalogue, each Supplier Agent replies to the Personal Agent 
specifying the item cost. The Personal Agent then compares the item price of each replying Supplier Agent and chooses the s
upplier who offers the best price. Finally the Personal Agent presents the user with the selected supplier along with the 
item and the price, or alternatively notifies the user that supplier has sufficient stocks of the item.
For simplicity we assume that only one item is ordered at a time.
You are supposed to implement the above system using the JADE Agent Programming Toolkit to demonstrate the behaviours of 
personal agents and supplier agents.
Personal Agent
In order to obtain a supplier, a user (PHB employee) logs into the Ordering System and informs their respective Personal 
Agent about the required item and quantity. The Personal Agent sends an item request to all known Supplier Agents. If more 
than one Supplier Agent accepts the order, the one with the lowest price is selected. If more than one Supplier Agent offered 
the same lowest price, then only one Supplier Agent is selected using feedback from the user.
Finally, Personal Agent notifies the selected Supplier Agent (via an acceptance message) and presents the selection to the 
user. The details displayed to the user are as follows:
1. The selected Supplier Agent’s name
2. Item name, quantity, unit price and total price.
Having completed the job the Personal Agent terminates.
Supplier Agent
Each Supplier Agent maintains a local catalogue that contains the available items, the quantity of each item in stock, and 
the unit price of each item. Any item can be available with more than one Supplier agent. Supplier Agents continuously wait 
for requests from Personal Agents. Once they receive a request, if sufficient numbers of the requested item are available in 
their catalogue, they reply specifying the sales price (per unit). Otherwise they refuse. If they receive an acceptance message 
from the Personal Agent, a confirmation message is sent and the requested quantity of the ordered item is removed from their 
catalogue.
You can include any enhancements you deem appropriate as long as the basic requirements specification is met. You will get 
bonus marks for enhancements.

Created on 17/05/2010

@author: peter
'''

class Material: 
    _type
    _amount
    _price

class Supplier:
    _location
    _materials  # array of Material
    
class Order:
    _materials

class User
    _material
    storePreference()
if __name__ == '__main__':
    pass