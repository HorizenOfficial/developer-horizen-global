***************
Latus Consensus
***************

As we have just seen, the Cross-Chain Transfer Protocol does not impose any requirements on the sidechain's architecture other than conforming to the protocol itself. Having said that, the Horizen Sidechain SDK does offer a ready made implementation of the Latus consensus, which is a Proof of Stake (“PoS”)  consensus based on the `Ouroboros Praos <https://eprint.iacr.org/2017/573.pdf>`_ protocol.

Consensus Epochs & Forging
===========================

In Latus, the chain is split into “consensus epochs”, where each epoch comprises a predefined number of time slots. Each slot is assigned to slot leaders, which are then authorized to generate (“forge”) a block during that slot. So the protocol operates in a synchronous environment where each slot spans over a specific amount of time (e.g. 20 seconds).
Slot leaders of a particular consensus epoch are chosen randomly before the epoch begins from the set of all sidechain forging stakeholders. The forging stake is a subset of all the coins managed by a sidechain. In fact each sidechain participant who wants to be a Forger must have some forging stake - i.e. a set of “ForgerBoxes” assigned to him. ForgerBox is a particular kind of Box that contains an amount of coins locked for forging, and some specific data used by the forger to prove its block-producing eligibility associated with that stake amount. The total amount of coins staked in ForgerBoxes is the total Forging Stake amount.
The possibility of being a slot leader increases with the percentage of forging stake owned. It's possible to have more than one slot leader per slot. If more than one block is propagated, only one will be accepted by each node; the consensus rules will make sure that conflicting chains will eventually converge to a winning chain. Conversely, a consensus epoch could have empty slots if their slot leader (or leaders) have not created and propagated blocks for them.

Forger Stake can be delegated to another node with makeForgerStake command. This command contains a list of transactions, each of them specifies the publicKey of a sender, blockSignPublicKey and vrfPubKey of receiving node and coin amount.
Also, Forger Stake can be delegated by spendForgingStake command. In this case, Forger Stake coins must be specified in forgerOutputs, coins specified in regularOutputs section will be moved from Forger Stakes and can be used as regular coins.
Creation Forger Stakes from regular coins can be done with createCoreTransaction. As with spendForgingStake, Forger coins must be specified in forgerOutputs section.

A slot leader eligible for a certain slot that creates and propagates a new sidechain block for that slot, is called a “forger”. A forger proves its eligibility for a slot by including in the block a cryptographic proof, in such a way that any node can validate, besides the validity of each transaction, also that the "slot leader" selection rule for that specific slot and consensus epoch was respected.

Forgers are also entitled and incentivized to include sidechain transactions and mainchain synchronization data into their sidechain blocks.
A limited amount of mainchain block data is added to sidechain blocks, in such a way that all the mainchain transactions that refer to a particular sidechain are included in that sidechain, that a reference to each mainchain block is present in all sidechains, and that information is stored in a sidechain so that any sidechain node is able to validate the mainchain block references without the need for a direct connection to the mainchain itself. Please note, the forger will need its own direct connection to mainchain nodes, to have a source of mainchain blocks data.
The connection between the mainchain and sidechain nodes is established via a websocket interface provided by the mainchain node. 


The Latus consensus, including mainchain block synchronization, forging logic and functionality, is implemented out-of-the-box by the core SDK, and developers do not need to make any changes to this. The forging process can be fully managed through the API interface provided by the SDK, see 
(`“the api reference” <../reference/01-scnode-api-spec.html#sidechain-block-operations>`_) .

.. _latus_params:
Default Latus consensus parameters
==================================

  * Seconds in one slot - 120, i.e. one block could be generated in two minutes
  * Number of slots in one consensus Epoch - 720, i.e. new nonce is generated (and thus forging stake holder could check slot leader possibility) every 720 * 120 =  86400 seconds, i.e. 24 hours.
  * BlockSize Limit 5MB

Seconds in one slot value must be specified in SidechainApp arguments. The minimum valid value is 10, the maximum is 430. Please note, that in case seconds in one slot has value 10, consensus epoch length shorten to 2 hours. At least one block of epoch must be generated during that time.

Fee redistribution
==================

At the end of the epoch, all fees are redistributed between all forgers. Each forger receives defined percentage of fee of each block it generated. All others fees of all blocks of the Withdrawal epoch must be spreaded equally between block forgers of the epoch. The remaining coins (after fee spreading) will be sent to first forgers of the epoch (the number of forgers is equal to the remained Satoshi), one Satoshi for each forger.


Pretty Good Decentralization
===

Pretty Good Decentralization (PGD) - mechanism to spread certificate signing between different nodes in the sidechain. It unloads submitter moving particular certificate signing calculation to other nodes. Each node can posses one or more schnorr key for signing. Keys must be specified in the configuration file.
