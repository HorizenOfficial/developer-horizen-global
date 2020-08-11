***************************************
Internal Representation of a Blockchain
***************************************

The sidechain software is is a distributed architecture and is meant to be delivered as a software application that will be 
compiled/installed by potentially many different independent, connected computers. In blockchain jargon, these computers are 
called “nodes,” and the term “node” is also generally used to name the blockchain software itself. 
So, the output of the sidechain SDK, when customized by a developer, is a “node” that implements core functionalities and the added logic.

A node consists of four main elements: history, state, wallet, and memory pool. 
We need to know what a “box” is before we get to know these four elements.

Concept of a Box
****************

A box generalizes the concept of Bitcoin’s UTXOs. A box is a cryptographic object that can be created with secret keys. This box can be opened (spent) by the 
owner of those secret keys. 
Once the owner of the secret keys opens it, the box may not be opened again.

Node Main Elements & Intro to a "NodeView"
******************************************

  * **History** - is a blockchain ledger that is typically a list of sidechain blocks that were received by the node, verified against consensus rules, and accepted.

  * **State** - is a snapshot of all boxes that haven’t been opened yet. It represents the state at the current chain tip.
    
  * **Wallet** - has two main functionalities:

    * It holds the secret keys that belong to that specific node.

    * It keeps track of objects that are of interest to this specific node, e.g. received coins (output boxes whose secret keys are known by the node) 
    and views of them (e.g. balances).   
  
  * **Memory Pool** - is a list of transactions that are known to the node but have not made it to a sidechain block yet.
    
Together these four objects represent a “NodeView.”

NodeViewHelper
==============

All communication between NodeView objects is controlled by NodeViewHolder, which also provides a layer of communication within the application for local data
processing of Blocks, Transactions, Secrets, etc.

In terms of customization, the History object is the only one that is fully controlled by the core and that in almost all circumstances does not need to be
extended. It contains a ready-made implementation of the Latus consensus and of the Cross-Chain Transfer Protocol.

The core logic of State, Wallet and Memory Pool can instead be extended by sidechain developers:

 * The “State” is a set of objects that are the result of processing all the previous blocks. These objects are needed to validate the next block, to allow the Node to efficiently verify, before applying a block, that all the defined rules have been respected by it. The “State” can be extended to keep track of new objects that can be useful to enforce additional rules that can be implemented in the application state interface.

 * The “Wallet” can be extended  through the ApplicationWallet interface, e.g. to change box ownership rules.

 * The logic to accept transactions in “Memory Pool” can be also extended, e.g. transaction incompatibility rules to address possible custom data conflicts.

As mentioned before, the “Box” is an important element, as it is designed as an object that contains some data, e.g. an amount of ZEN coins, or data of a custom object (such as a car’s plate as we’ll see in Section 9), associated with some conditions (called “Proposition”) that protect them from being spent other than by a party (or parties) able to satisfy that proposition. Usually, the ability to satisfy a Proposition is given by knowledge of some data (“called “Secret”), that can be used to produce a “Proof” that satisfies the Proposition and opens the Box, so that it can be spent. 

If we translate the above into bitcoin-like terminology, a UTXO is a Box, a locking script of an output is a Proposition, e.g. a P2PK unlocking script, the signature is the proof, and its associated private key is the Secret.

Box Unique ID & Transactions
============================

Each Box should have a unique id, which is deterministically determined using the box data as input. Since we may have several boxes locked by the same proposition, and representing the same data inside, we can avoid conflicts by using NoncedBox, which inherits Box and contains some Nonce data. Nonce data is a value that is deterministically assigned to the box depending on the Transaction that includes it, and the index of the Box inside the Transaction outputs list. This way we can guarantee that two boxes with the same data (proposition, amount and other custom fields) will have different nonces, so will have different unique box ids.

A Transaction is a sequence of inputs and outputs. Each input consists of a reference to the Box being opened, and a Proof that satisfies the condition of its Proposition.
Each output is a new Box instance. Block is the only chain modifier, and it’s made of header (“BlockHeader”) and data (“BlockData”), similarly to the bitcoin block structure. 






   

