***************************************
Internal representation of a Blockchain
***************************************

Being a distributed architecture, the sidechain software is delivered as an application that will be compiled/installed on potentially many different independent, networked computers. In blockchain jargon, these computers are called “nodes,” and the term “node” is also generally used to name the blockchain software itself.
So, the output of the Sidechain SDK, when customized by a developer, is a “node” that implements core functionalities and the added sidechain logic.

A node consists of 4 main elements: “**History**,” “**State**,” “**Wallet**,” and “**Memory pool**.” Before we get to know these 4 elements we need to know what a “box” is.

Concept of a BOX
****************

A box generalizes the concept of Bitcoin’s UTXOs.
A box is a cryptographic object that can be created with one or more secret keys. This box can be opened ("spent") by the owner/owners of those secret keys. Once opened, the box may not be opened again.

Node Main elements & intro to a "NodeView"
******************************************

  * **History**
    * “History” is a blockchain ledger, typically a list of sidechain blocks that were received by the node, have been verified against Consensus rules, and accepted.
    
  * **State**
    * “State” is a snapshot of all boxes that haven’t been opened yet. It represents the state at the current chain tip.
    
  * **Wallet**
    * The “Wallet” has two main functionalities:
      1. It holds the secret keys that belong to that specific node.
      2. It keeps track of objects that are of interest to this specific node, e.g. received coins (output boxes whose secret keys are known by the node) and views of them (e.g. balances).      
  * **Memory Pool**
    * The “Memory pool” is a list of transactions that are known to the node but have not made it to a sidechain block yet.
    
Altogether these 4 objects represent a “NodeView.”

NodeViewHelper
==============

All communication between NodeView objects is controlled by NodeViewHolder, which also provides a layer of communication within the application for local data processing of blocks, transactions, secrets, etc.

In terms of customization, the History object is the only one that is fully controlled by the core and that in almost all circumstances does not need to be extended. It contains a ready-made implementation of the Latus consensus and of the Cross-Chain Transfer Protocol.

The core logic of State, Wallet and Memory Pool objects can be extended by sidechain developers:

 * The “state” is the set of objects that result from processing all the previous blocks. These objects are needed to validate the next block to allow the node to efficiently verify before applying a block that all the defined rules have been respected by it. The “state” can be extended to keep track of new objects that can be useful to enforce additional rules that can be implemented in the application state interface.

 * The “wallet” can be extended through the ApplicationWallet interface, e.g. to change box ownership rules.

 * The logic to accept transactions in “Memory Pool” can be also extended, e.g. transaction incompatibility rules to address possible custom data conflicts.

As mentioned before, the “box” is an object that contains some data, e.g. an amount of ZEN, or data of a custom object (such as a car’s plate as we’ll see in Section 9), associated with some conditions (called a “proposition”) that protects it from being spent by anyone other than by a party (or parties) able to satisfy that proposition. Usually, the ability to satisfy a proposition is given by knowledge of some data (called a “secret”), that can be used to produce a “proof” that satisfies the proposition and opens the box, so that it can be spent. 

If we translate the above into bitcoin-like terminology, a UTXO is a Box, a locking script of an output is a Proposition, e.g. a P2PK unlocking script, the signature is the proof, and its associated private key is the Secret.

Box Unique ID & Transactions
============================

Each Box should have a unique id, which is deterministically determined using the box data as input. Since we may have several boxes locked by the same proposition, and representing the same data inside, we can avoid conflicts by using NoncedBox, which inherits Box and contains some Nonce data. Nonce data is a value that is deterministically assigned to the box depending on the Transaction that includes it, and the index of the Box inside the Transaction outputs list. This way we can guarantee that two boxes with the same data (proposition, amount and other custom fields) will have different nonces, so will have different unique box ids.

A Transaction is a sequence of inputs and outputs. Each input consists of a reference to the Box being opened, and a Proof that satisfies the condition of its Proposition.
Each output is a new Box instance. Block is the only chain modifier, and it’s made of header (“BlockHeader”) and data (“BlockData”), similarly to the bitcoin block structure. 






   

