*********************************
The Cross-Chain Transfer Protocol
*********************************

The Cross-Chain Transfer Protocol (“CCTP”) defines the rules of communication between the mainchain and sidechain(s). It is a 2-way peg protocol that allows sending coins from the mainchain to a sidechain, and vice versa.

At a high level, it defines three basic operations:
   
   * **Forward Transfer**
   * **Backward Transfer**
   * **Ceased Sidechain Withdrawal**
   
While all sidechains know and follow the mainchain, which is an established and stable reality, the mainchain needs to be made aware of the existence of every sidechain. So, sidechains first must be declared to the mainchain.

We can declare a new sidechain by using the following RPC command:

.. code:: Bash

    sc_create {
         "version": version,
         "withdrawalEpochLength": withdrawalEpochLength, 
         "fromaddress": mc_address, 
         "changeaddress": mc_address, 
         "toaddress": sc_address, 
         "amount": creation_amount, 
         "minconf": conf, 
         "fee": fee, 
         "wCertVk": vk, 
         'customData': custom_data, 
         "constant": constant, 
         'wCeasedVk': cswVk, 
         'vFieldElementCertificateFieldConfig': feCfg,
         'vBitVectorCertificateFieldConfig': bvCfg, 
         'forwardTransferScFee': ftScFee, 
         'mainchainBackwardTransferScFee': mbtrScFee, 
         'mainchainBackwardTransferRequestDataLength': mbtrRequestDataLength
    }
	
Parameters to the command must be passed in JSON format. 
The command must specify the destination address where the first forward transfer coins are sent ("toaddress"), its amount ("amount"), as well as the epoch length ("withdrawalEpochLength"). 
It is the epoch length that defines the frequency, in blocks, of the backward transfers' submissions (see the “backward transfers” paragraph below). Otherwise sidechain can be declared as non ceasing. In this case sidechain not oblige to send certificates in determined period of time, but can decide itself when to submit it.
The sc_create command also includes the cryptographic key to receive coins back from the sidechain ("wCertVk").
The verification key guarantees that the received coins were processed according to a matching proving system. 
Besides these parameters, sc_create has some optional ones, here is the complete set of parameters:

 - **version**                                    - (numeric, required) The version of the sidechain. Recommended to use version 1. For non ceasing sidechain should be 2.
 - **withdrawalEpochLength**                      - (numeric, optional, default=100) length of the withdrawal epochs. The minimum valid value in regtest is: 2, the maximum (for any network type) is: 4032. For non ceasing sidechain should be 0.
 - **fromaddress**                                - (string, optional) The MC taddr to send the funds from. If omitted funds are taken from all available UTXO.
 - **changeaddress**                              - (string, optional) The MC taddr to send the change to, if any. If not set, "fromaddress" is used. If the latter is not set too, a newly generated address will be used.
 - **toaddress**                                  - (string, required) The receiver PublicKey25519Proposition in the SC.
 - **amount**                                     - (numeric, required) Funds to be sent to the newly created Sidechain. Value expressed in ZEN.
 - **minconf**                                    - (numeric, optional, default=1) Only use funds confirmed at least this many times.
 - **fee**                                        - (numeric, optional) The fee amount to attach to this transaction in ZEN. If not specified it is automatically computed using a fixed fee rate (default is 1zat per byte).
 - **wCertVk**                                    - (string, required) It is an arbitrary byte string of even length expressed in hexadecimal format. Required to verify a WCert SC proof. Its size must be 9216 bytes max.
 - **customData**                                 - (string, optional) An arbitrary byte string of even length expressed in hexadecimal format. A max limit of 1024 bytes will be checked.
 - **constant**                                   - (string, optional) It is an arbitrary byte string of even length expressed in hexadecimal format. Used as public input for WCert proof verification. Its size must be 32 bytes.
 - **wCeasedVk**                                  - (string, optional) It is an arbitrary byte string of even length expressed in hexadecimal format. Used to verify a Ceased sidechain withdrawal proof for given SC. Its size must be 9216 bytes max. Not used in non ceasing sidechains.
 - **vFieldElementCertificateFieldConfig**        - (array, optional) An array whose entries are sizes (in bits). Any certificate should have as many custom FieldElements with the corresponding size.
 - **vBitVectorCertificateFieldConfig**           - (array, optional) An array whose entries are bitVectorSizeBits and maxCompressedSizeBytes pairs. Any certificate should have as many custom BitVectorCertificateField with the corresponding sizes.
 - **forwardTransferScFee**                       - (numeric, optional, default=0) The amount of fee in ZEN due to sidechain actors when creating a FT
 - **mainchainBackwardTransferScFee**             - (numeric, optional, default=0) The amount of fee in ZEN due to sidechain actors when creating a MBTR
 - **mainchainBackwardTransferRequestDataLength** - (numeric, optional, default=0) The expected size (max=16) of the request data vector (made of field elements) in a MBTR



As a consequence of the sidechain declaration command, a unique sidechain id will be assigned to that sidechain, and from that moment on that id can be used for every operation related to that specific sidechain:

.. code:: json
   
   {
      "txid": "9e4676274f1ff9b3164de6e0d6492c4dfc1d564b0243a36208c6b7fe848f9d21",
      "scid": "2f7ed2e07ad78e52f43aafb85e242497f5a1da3539ecf37832a0a31ed54072c3",
   }


Forward Transfer
================

A forward transfer sends coins from the mainchain to a sidechain. The Horizen Mainchain supports a “Forward Transfer” transaction type that specifies the sidechain destination (*sidechain id* and *receiver address*) and the amount of ZEN to be sent.
Forward Transfer can be done by using following RPC command:

.. code:: Bash

   sc_send <outputs> [params]

The input arguments have the following structure:

 - **1. outputs**                     - (string, required) A json array of json objects representing the amounts to send:

.. code:: Bash

  [{
    "scid": id,
    "toaddress":sc_addr,
    "amount":amount,
    "mcReturnAddress":mc_addr
    },...,]

Where: 

     - **scid**            - (string, required) The uint256 side chain ID
     - **toaddress**       - (string, required) The receiver PublicKey25519Proposition in the SC
     - **amount**          - (numeric, required) Value expressed in ZEN
     - **mcReturnAddress** - (string, required) The Horizen mainchain address where to send the backward transfer in case Forward Transfer is rejected by the sidechain

And:

 - **2. params**                       - (string, optional) A json object with the command parameters:

.. code:: Bash

  {
     "fromaddress":taddr   
     "changeaddress":taddr 
     "minconf":conf        
     "fee":fee             
  }

Where:

      - **fromaddress**   - (string, optional) The taddr to send the funds from. If omitted funds are taken from all available UTXO
      - **changeaddress** - (string, optional) The taddr to send the change to, if any. If not set, "fromaddress" is used. If the latter is not set too, a newly generated address will be used
      - **minconf**       - (numeric, optional, default=1) Only use funds confirmed at least this many times.
      - **fee**           - (numeric, optional) The fee amount to attach to this transaction in ZEN. If not specified it is automatically computed using a fixed fee rate (default is 1zat per byte)


This command specifies the SC destination where the forward transfer coins are sent ("toaddress"), the amount ("amount") and the MC address where to send a backward transfer in case Forward Transfer is rejected by the sidechai ("mcReturnAddress").

From the mainchain's perspective, the transferred coins are destroyed; they are only represented in the total balance of that particular sidechain.
On the sidechain side, the SDK provides all the functionalities that support Forward Transfers, so that a transferred amount is “converted” into a new Sidechain Box.

Backward Transfer
=================

A backward transfer moves coins back from a sidechain to the mainchain destination.
A Backward Transfer is initiated by a **Withdrawal Request** which is a sidechain transaction issued by the coin's owner. The request specifies the mainchain destination address and the amount. More precisely, the withdrawal request owner will create a WithdrawalRequestBox that destroys the specified amount of coins in the sidechain. This is not enough to move those coins back to the mainchain though: we need to wait until the end of the withdrawal epoch, when all the coins specified in that epoch’s Withdrawal Requests are listed in a single certificate, that is then propagated to the mainchain.
The certificate includes a succinct cryptographic proof that the rules associated with the declared verifying key have been respected. Certificates are processed by the mainchain consensus, which recreates the coins as specified by the certificate, only checking that the proof verifies, and that the coins received by a sidechain match the amount that was sent to it.

As an optional step, on MC side it is possible to explicitly request a Backward Transfer from the SC which should be included in one of the next certificates via the following RPC command:

.. code:: Bash
 
    sc_request_transfer <outputs> [params]

The input arguments have the following structure:

 - **1. outputs**                     - (string, required) A json array of json objects representing the request to send:

.. code:: Bash

  [{
    "scid": id,
    "vScRequestData":req_data,
    "mcDestinationAddress":mc_addr,
    "scFee":amount,
    },...,]

Where: 

     - **scid**                 - (string, required) The uint256 side chain ID
     - **vScRequestData**       - (array, required) It is an arbitrary array of byte strings of even length expressed in hexadecimal format representing a SC reference (for instance an Utxo ID) for which a backward transfer is being requested. The size of each string must be 32 bytes.
     - **mcDestinationAddress** - (string, required) The Horizen mainchain address where to send the backward transfer
     - **scFee**                - (numeric, required) The amount in ZEN representing the value spent by the sender that will be gained by a SC forger

And:

 - **2. params**                       - (string, optional) A json object with the command parameters:

.. code:: Bash

  {
     "fromaddress":taddr   
     "changeaddress":taddr 
     "minconf":conf        
     "fee":fee             
  }

Where:

      - **fromaddress**   - (string, optional) The taddr to send the funds from. If omitted funds are taken from all available UTXO
      - **changeaddress** - (string, optional) The taddr to send the change to, if any. If not set, "fromaddress" is used. If the latter is not set too, a newly generated address will be used
      - **minconf**       - (numeric, optional, default=1) Only use funds confirmed at least this many times.
      - **fee**           - (numeric, optional) The fee amount to attach to this transaction in ZEN. If not specified it is automatically computed using a fixed fee rate (default is 1zat per byte)


Ceased Sidechain Withdrawal
===========================

The funds of a ceased sidechain can be withdrawn back to the mainchain with a Ceased Sidechain Withdrawal request. This request can be performed right after the sidechain ceasing.

This feature is optional. In order to enable the CSW for a sidechain, it is necessary to provide a specific key to be used by the mainchain to verify the validity of a Ceased Sidechain Withdrawal. This key should be provided using the *wCeasedVk* parameter in *sc_create* command. In addition, the CSW requires 2 custom FieldElementCertificateField of 255 bits size, so the parameter *vFieldElementCertificateFieldConfig* in *sc_create* command should be set to [255, 255].

To create a CSW request, a nullifier and a Ceased Sidechain Withdrawal proof should be generated on the sidechain side. Nullifier can be generated by API command *nullifier* (CSW API group). Proof generation can be done with *generateCswProof* command.
Command *cswInfo* shows csw related data for specified box id.

Mainchain request can be performed through a raw transaction with the following structure:


.. code:: json

       sc_csws = [{
            "amount": sc_csw_amount,
            "senderAddress": csw_mc_address,
            "scId": scid,
            "epoch": 0,
            "nullifier": nullifier,
            "activeCertData": actCertData,
            "ceasingCumScTxCommTree": ceasingCumScTxCommTree,
            "scProof": sc_proof1
        }]


Summary
=======

The Cross-Chain Transfer Protocol assumes that proofs are generated with a specific proving system, but does not limit the logic of the computation that is proven by the proving system (the “circuit”). So, sidechain developers could implement any proving system to prove the legitimacy of backward transfers. The examples provided with the SDK implement a sample proving system that proves that the certificate was signed by a minimum number of certifiers, whose key identities were declared at sidechain creation time. This is just a demo circuit; production sidechains require robust circuits 
(see the Latus recursive model in the (`Zendoo paper <https://www.horizen.global/assets/files/Horizen-Sidechain-Zendoo-A_zk-SNARK-Verifiable-Cross-Chain-Transfer-Protocol.pdf>`_).
