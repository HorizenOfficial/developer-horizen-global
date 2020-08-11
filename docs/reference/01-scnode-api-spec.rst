Sidechain Node API spec
~~~~~~~~~~~~~~~~~~~~~~
=====
**Sidechain Block operations**
=====


.. http:post:: /block/findById

*Find Block by ID*

**Parameters**

+---------+--------+----------+------------------+
| Name    | Type   | Required | Description      |
+=========+========+==========+==================+
| blockId | String | yes      | Find block by ID |
+---------+--------+----------+------------------+

   :query boolean active: return only active versions
   :query boolean built: return only built versions

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9085/block/findById" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"blockId\":\"0...6\"}"

   |
   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
         "result":{
            "blockHex":"string",
            "block":{
               "id":"string",
               "parentId":"string",
               "timestamp":0,
               "mainchainBlocks":[
                  {
                     "header":{
                        "mainchainHeaderBytes":"string",
                        "version":0,
                        "hashPrevBlock":"string",
                        "hashMerkleRoot":"string",
                        "hashReserved":"string",
                        "hashSCMerkleRootsMap":"string",
                        "time":0,
                        "bits":0,
                        "nonce":"string",
                        "solution":"string"
                     },
                     "sidechainRelatedAggregatedTransaction":{
                        "id":"string",
                        "fee":0,
                        "timestamp":0,
                        "mc2scTransactionsMerkleRootHash":"string",
                        "newBoxes":[
                           {
                              "id":"string",
                              "proposition":{
                                 "publicKey":"string"
                              },
                              "value":0,
                              "nonce":0,
                              "activeFromWithdrawalEpoch":0,
                              "typeId":0
                           }
                        ]
                     },
                     "merkleRoots":[
                        {
                           "key":"string",
                           "value":"string"
                        }
                     ]
                  }
               ],
               "sidechainTransactions":[
                  {

                  }
               ],
               "forgerPublicKey":{
                  "publicKey":"string"
               },
               "signature":{
                  "signature":"string"
               }
            }
         },
         "error":{
            "code":"string",
            "description":"string",
            "detail":"string"
         }
      }      

_____

   .. http:post:: /block/findLastIds
   
*Returns an array with the ids of the last x blocks*  
   
**Parameters**

+---------+--------+----------+----------------------------------------+
| Name    | Type   | Required |          Description                   |
+=========+========+==========+========================================+
|  number |  int   |   yes    | Retrieves the last x number of blocks  |
+---------+--------+----------+----------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9085/block/findLastIds" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"number\":10}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
         "result":{
            "lastBlockIds":[
               "055c15d9a6c9ae299493d241705a2bcfdfbc72a19f04394a26aa53b39f6ee2a6",
               "ae6bcf104b7a7cccf83dfa23494760fb8d9a4d5cc3de82443de8b82bb86669d1",
               "9120b0f8518d1944d4b0e8fac8990acc7dcb792ea660414906a03f346407160c",
               "e5b0e97df9502c9510e4862041754b62931c9dc0a4fa873b3a0d75561dcbe712",
               "6a080e3ee665980bf647b450749b04177fe272537808bb4aec70417f9994bd04",
               "97d1956ecb1199fe03171b0923dff4031850e33db56dd1afc3b5384350315d80",
               "2c3a4a91989110218a827f8baefa3a8e5baf33e7e16d32b2bdace94553478dde",
               "cf82fba3e75ac89ca7e8d1c29458b2d5eff9d807407d3265c14251da2c70b3b1",
               "d61da61b2c877f717fa50563a42cbad4420486bfa3b1f05d888528d69d8258d8",
               "921f9406d8edd03d2f5b65aa6f89e452720c7ef07244ee06f3ad19d2c49e45d8"
            ]
         }
      }

_____

 .. http:post:: /block/findIdByHeight
   
*Return a sidechain block Id by its height in a blockchain*  
   
**Parameters**

+---------+--------+----------+----------------------------------------+
| Name    | Type   | Required |          Description                   |
+=========+========+==========+========================================+
|  height |  int   |   yes    | Retrieves block ID by it´s height      |
+---------+--------+----------+----------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/block/findIdByHeight" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"height\":100}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
         "result":{
            "blockId":"e8c92a6c217a7dced190b729a7815f0be6a011ea23a38e083e79298bb66620e7"
         }
      }

_____

 .. http:post:: /block/best
   
Return here best sidechain block id and height in active chain
   
**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/block/best" -H "accept: application/json"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "block": {
            "header": {
              "version": 1,
              "parentId": "ae6bcf104b7a7cccf83dfa23494760fb8d9a4d5cc3de82443de8b82bb86669d1",
              "timestamp": 1595475730,
              "forgerBox": {
                "nonce": -8596034112114319000,
                "id": "f290e648415642b051cf6075b5fcaa7609eddd9a919d144cc2062db632918d9e",
                "typeId": 3,
                "vrfPubKey": {
                  "valid": true,
                  "publicKey": "d984ea8909760cb69d0a1a13848bd534e9ac28ec0ac20c3b05d557fa6512405185d799d1bab96068ad903a8f72e08329f29b45747a9ab1e66841b9a8440140e507457168d07bf6032875a6112dba9e6cb728d1a37e47c196aa9045136dd3000098a74b639a0bd495b3a19facd5c7b2811257a45476fb369c282002ec4f3aad4324b73e6555290b35db447705375824a5c5805a94c0438125f38b138e6842bb48bef94da30b4c5b121ce368544c86351ccdc8197d9f2334d2e52a44620381000000"
                },
                "blockSignProposition": {
                  "publicKey": "153623a54522cc0336068a305ac13f530f4fdc95ee105a7ee85939326b9996fb"
                },
                "value": 10000000000,
                "proposition": {
                  "publicKey": "153623a54522cc0336068a305ac13f530f4fdc95ee105a7ee85939326b9996fb"
                }
              },
              "forgerBoxMerklePath": "00000000",
              "vrfProof": {
                "vrfProof": "6be4253461faa494c5b79befbd12a39d73bf80c8c0d4b004bb72b49d0203fee1880057100dec12d4fbaf49e304798726ae07fe3acca2250376e93c3d7315ae45ecc99f70b36e21154026d035fa52cb584f2477ad5b677b199d4b5801e6b70100f8be8238b793179259207f1f372d796bd00223c46126316e9833965adabd3d21f2c11d0bc15e583ecbe4e00232082eb88dc78af8e9be5b68f6f7571dcd45ba6c563427a3f4f529a33edad6a79e1c9ecf9bc0e1ad54009ac1899cbf4d9b7a0000009a34323da1dc589a82cbe0eaad05bcebeea9b215c1128e2179402da8f4d556c5231a94f88170638199ddfe45fedebd1456796a47bc4c8cf583c004451a824bcae2ce1b88fdb1fa991b850e31847ecc8fa3f66de17e170ee478e2e7cd4b8b00009b232901e99f7da9c747d72a32579ff19d076b68434f2438e24230db15c1af7f0e31fcc7e8c2b90ce9206a05feed010e5f2dccb89030f6fd3a582901a9451a2fc232a816c48af827d1e98120cd191152ccfe81ccfa8db563aaaaeb3d36600000"
              },
              "sidechainTransactionsMerkleRootHash": "0000000000000000000000000000000000000000000000000000000000000000",
              "mainchainMerkleRootHash": "0000000000000000000000000000000000000000000000000000000000000000",
              "ommersMerkleRootHash": "0000000000000000000000000000000000000000000000000000000000000000",
              "ommersCumulativeScore": 0,
              "signature": {
                "signature": "2c5e2d784bdb46ab07a9958152605a363931fa2794c714169e054667ef615f176be20a8db5a8dc40f02daca3d66842b85289be2ec4e11d9151f235f13a8a0105",
                "typeId": 1
              },
              "id": "055c15d9a6c9ae299493d241705a2bcfdfbc72a19f04394a26aa53b39f6ee2a6"
            },
            "sidechainTransactions": [],
            "mainchainBlockReferencesData": [],
            "mainchainHeaders": [],
            "ommers": [],
            "timestamp": 1595475730,
            "parentId": "ae6bcf104b7a7cccf83dfa23494760fb8d9a4d5cc3de82443de8b82bb86669d1",
            "id": "055c15d9a6c9ae299493d241705a2bcfdfbc72a19f04394a26aa53b39f6ee2a6"
          },
          "height": 371
        }
      }

_____

.. http:post:: /block/startForging
   
*Start forging*  
   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/block/startForging" -H "accept: application/json"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "result": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }

_____

 .. http:post:: /block/stopForging
   
*Stop forging*  
   
**No Parameters**
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/block/stopForging" -H "accept: application/json"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "result": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }

_____


   .. http:post:: /block/generate
   
*Try to generate new block by epoch and slot number*  
*Returns id of generated sidechain block*
   
**Parameters**

+-------------+--------+----------+----------------------------------------+
| Name        | Type   | Required |          Description                   |
+=============+========+==========+========================================+
| epochNumber |  int   |   yes    |         Epoch Number                   |
+-------------+--------+----------+----------------------------------------+
|  slotNumber |  int   |   yes    |         Slot Number                    |
+-------------+--------+----------+----------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/block/generate" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"epochNumber\":3,\"slotNumber\":45}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "blockId": "7f25d35aadae65062033757e5049e44728128b7405ff739070e91d753b419094"
        }
      }
      
_____

   .. http:post:: /block/forgingInfo
   
*Get forging info*
   
**No Parameters**
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/block/forgingInfo" -H "accept: application/json"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "consensusSecondsInSlot": 120,
          "consensusSlotsInEpoch": 720,
          "bestEpochNumber": 3,
          "bestSlotNumber": 45
        }
      }

_____

=====
**Sidechain Transaction operations**
=====

.. http:post:: /transaction/allTransactions

*Find all transactions in the memory pool*  
   
**Parameters**

+--------+---------+----------+---------------------------------------------------------------------------------------------------------+
| Name   | Type    | Required | Description                                                                                             |
+========+=========+==========+=========================================================================================================+
| format | boolean | no       | Returns an array of transaction ids if formatMemPool=false, otherwise a JSONObject for each transaction |
+--------+---------+----------+---------------------------------------------------------------------------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/allTransactions" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"format\":true}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transactions": []
        }
      }
      
_____

   .. http:post:: /transaction/findById
   
* *blockHash set -> Search in block referenced by blockHash (do not care about txIndex parameter)*
* *blockHash not set, txIndex = true -> Search in memory pool, if not found, search in the whole blockchain*
* *blockHash not set, txIndex = false -> Search in memory pool*
   
**Parameters**

+------------------+---------+---------------------------------------------------------------------------------------+
| Name             | Type    | Description                                                                           |
+==================+=========+=======================================================================================+
| transactionId    | String  | Find by Transaction Id                                                                |
+------------------+---------+---------------------------------------------------------------------------------------+
| blockHash        | String  | Search in block referenced by blockHash (do not care about txIndex parameter)         |
+------------------+---------+---------------------------------------------------------------------------------------+
| transactionIndex | boolean | txIndex = true -> Search in memory pool, if not found, search in the whole blockchain |
+------------------+---------+---------------------------------------------------------------------------------------+
| format           | boolean |                                                                                       |
+------------------+---------+---------------------------------------------------------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/findById" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"transactionId\":\"string\",\"blockHash\":\"string\",\"transactionIndex\":false,\"format\":false}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transaction": {},
          "transactionBytes": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }

_________

.. http:post:: /transaction/decodeTransactionBytes
   
*Return a JSON representation of a transaction given its byte serialization*


   
**Parameters**

+------------------+--------+----------+----------------------------------------+
| Name             | Type   | Required |          Description                   |
+==================+========+==========+========================================+
| transactionBytes | String |   yes    |         byte String                    |
+------------------+--------+----------+----------------------------------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/decodeTransactionBytes" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"transactionBytes\":\"string\"}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transaction": {}
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
      
______


.. http:post:: /transaction/createCoreTransaction
   
*Create and sign a Sidechain core transaction, specifying inputs and outputs. Return the new transaction as a hex string if format = false, otherwise its JSON representation.*


   
**Parameters**

Example Value

   .. sourcecode:: http

      {
        "transactionInputs": [
          {
            "boxId": "string"
          }
        ],
        "regularOutputs": [
          {
            "publicKey": "string",
            "value": 0
          }
        ],
        "withdrawalRequests": [
          {
            "publicKey": "string",
            "value": 0
          }
        ],
        "forgerOutputs": [
          {
            "publicKey": "string",
            "blockSignPublicKey": "string",
            "vrfPubKey": "string",
            "value": 0
          }
        ],
        "format": false
      }

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/createCoreTransaction" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"transactionInputs\":[{\"boxId\":\"string\"}],\"regularOutputs\":[{\"publicKey\":\"string\",\"value\":0}],\"withdrawalRequests\":[{\"publicKey\":\"string\",\"value\":0}],\"forgerOutputs\":[{\"publicKey\":\"string\",\"blockSignPublicKey\":\"string\",\"vrfPubKey\":\"string\",\"value\":0}],\"format\":false}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transaction": {},
          "transactionBytes": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      } 
      
______


.. http:post:: /transaction/createCoreTransactionSimplified
   
*Create and sign a Sidechain core transaction, specifying inputs and outputs. Return the new transaction as a hex string if format = false, otherwise its JSON representation.*

   
**Parameters**

Example Value 

   .. sourcecode:: http
   
      {
        "regularOutputs": [
          {
            "publicKey": "string",
            "value": 0
          }
        ],
        "withdrawalRequests": [
          {
            "publicKey": "string",
            "value": 0
          }
        ],
        "forgerOutputs": [
          {
            "publicKey": "string",
            "blockSignPublicKey": "string",
            "vrfPubKey": "string",
            "value": 0
          }
        ],
        "fee": 0,
        "format": true
      }

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/createCoreTransactionSimplified" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"regularOutputs\":[{\"publicKey\":\"string\",\"value\":0}],\"withdrawalRequests\":[{\"publicKey\":\"string\",\"value\":0}],\"forgerOutputs\":[{\"publicKey\":\"string\",\"blockSignPublicKey\":\"string\",\"vrfPubKey\":\"string\",\"value\":0}],\"fee\":0,\"format\":true}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transaction": {},
          "transactionBytes": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }

______


.. http:post:: /transaction/sendCoinsToAddress
   
*Create and sign a regular transaction, specifying outputs and fee. Then validate and send the transaction. Then return the id of the transaction*

   
**Parameters**

Example Value

   .. sourcecode:: http

      {
        "outputs": [
          {
            "publicKey": "string",
            "value": 0
          }
        ],
        "fee": 0
      }

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/sendCoinsToAddress" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"outputs\":[{\"publicKey\":\"string\",\"value\":0}],\"fee\":0}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transactionId": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
      
____

.. http:post:: /transaction/withdrawCoins
   
*Create and sign a regular transaction, specifying withdrawal outputs and fee. Then validate and send the transaction. Then return the id of the transaction*

   
**Parameters**

   .. sourcecode:: http

      {
        "outputs": [
          {
            "publicKey": "string",
            "value": 0
          }
        ],
        "fee": 0
      }      

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/withdrawCoins" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"outputs\":[{\"publicKey\":\"string\",\"value\":0}],\"fee\":0}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "code": 0,
        "reason": "string",
        "detail": "string"
      }
      
____

.. http:post:: /transaction/makeForgerStake
   
*Create and sign a Sidechain core transaction, specifying forger stake outputs and fee. Then validate and send the transaction. Then return the id of the transaction*

   
**Parameters**

Example Value

   .. sourcecode:: http

      {
        "outputs": [
          {
            "publicKey": "string",
            "blockSignPublicKey": "string",
            "vrfPubKey": "string",
            "value": 0
          }
        ],
        "fee": 0
      }

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/makeForgerStake" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"outputs\":[{\"publicKey\":\"string\",\"blockSignPublicKey\":\"string\",\"vrfPubKey\":\"string\",\"value\":0}],\"fee\":0}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transactionId": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
     
_______

.. http:post:: /transaction/spendForgingStake
   
*Create and sign sidechain core transaction, specifying inputs and outputs. Return the new transaction as a hex string if format = false, otherwise its JSON representation.*

   
**Parameters**

Example Value

   .. sourcecode:: http

      {
        "transactionInputs": [
          {
            "boxId": "string"
          }
        ],
        "regularOutputs": [
          {
            "publicKey": "string",
            "value": 0
          }
        ],
        "forgerOutputs": [
          {
            "publicKey": "string",
            "blockSignPublicKey": "string",
            "vrfPubKey": "string",
            "value": 0
          }
        ],
        "format": false
      }

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/spendForgingStake" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"transactionInputs\":[{\"boxId\":\"string\"}],\"regularOutputs\":[{\"publicKey\":\"string\",\"value\":0}],\"forgerOutputs\":[{\"publicKey\":\"string\",\"blockSignPublicKey\":\"string\",\"vrfPubKey\":\"string\",\"value\":0}],\"format\":false}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transaction": {},
          "transactionBytes": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
     
______


.. http:post:: /transaction/sendTransaction
   
*Validate and send a transaction, given its serialization as input. Then return the id of the transaction*

   
**Parameters**

+------------------+--------+--------------------------+
| Name             | Type   | Description              |
+==================+========+==========================+
| transactionBytes | String | Signed Transaction Bytes |
+------------------+--------+--------------------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9087/transaction/sendTransaction" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"transactionBytes\":\"string\"}"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "transactionId": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
   
______

=====
**Sidechain Wallet Operations**
=====

.. http:post:: /wallet/allBoxes
   
*Return all boxes, excluding those which ids are included in excludeBoxIds list*

   
**Parameters**

Example Value

   .. sourcecode:: http

      {
        "boxTypeClass": "string",
        "excludeBoxIds": [
          "string"
        ]
      }

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/wallet/allBoxes" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"boxTypeClass\":\"string\",\"excludeBoxIds\":[\"string\"]}"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "boxes": [
            {
              "id": "string",
              "proposition": {
                "publicKey": "string"
              },
              "value": 0,
              "nonce": 0,
              "activeFromWithdrawalEpoch": 0,
              "typeId": 0
            }
          ]
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
      
______

.. http:post:: /wallet/balance
   
*Return the global balance for all types of boxes*

   
**Parameters**

+---------+--------+----------+-------------+
| Name    | Type   | Required | Description |
+=========+========+==========+=============+
| boxType | String | No       |  Box type   |
+---------+--------+----------+-------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/wallet/balance" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"boxType\":\"string\"}"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "balance": 0
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }

______


.. http:post:: /wallet/createPrivateKey25519
   
*Create new secret and return corresponding address (public key)*

   
**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/wallet/createPrivateKey25519" -H "accept: application/json"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "proposition": {
            "publicKey": "string"
          }
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
      
______

.. http:post:: /wallet/createVrfSecret
   
*Create new Vrf secret and return corresponding public key*

   
**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/wallet/createVrfSecret" -H "accept: application/json"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "proposition": {
            "valid": true,
            "publicKey": "ef3df0e2ca6f34dc89c2c14e23aecd37370ec4739230a6ec640a1fc87857ee5e7f55f3784e5ddd3c8e733bcdefb6795fda1d1228013c1968639bfd8888a48a07bbf978bec536412338eefd96e8d980e667f2d78a8e284bc3c9e8f7e4697400008ab41ebebb96464c0d4a77c6ac059e8265095faede25bf2e22a4d2dc82e6631dce2a61c2c5fb8e77160cee81fe84de136225ac1853f4b971eb3ecfadee7993bbb9cf7af75bb6523b248debb2a2173a8bcfba90ee5e2c55f7edb89f182e1f010000"
          }
        }
      }

________

.. http:post:: /wallet/allPublicKeys
   
*Returns the list of all wallet’s propositions (public keys)*

   
**Parameters**

+----------+--------+-------------+
| Name     | Type   | Description |
+==========+========+=============+
| protoype | String |             |
+----------+--------+-------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/wallet/allPublicKeys" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "propositions": [
            {
              "publicKey": "string"
            }
          ]
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }

________


=====
**Sidechain node operations**
=====


.. http:post:: /node/allPeers
   
*Returns the list of all sidechain node peers*

   
**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/node/allPeers" -H "accept: application/json"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "peers": [
            {
              "address": "string",
              "lastSeen": 0,
              "name": "string",
              "connectionType": "string"
            }
          ]
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
      
__________

.. http:post:: /node/connect
   
*Send the request to connect to a sidechain node*

   
**Parameters**

+------+--------+--------------+
| Name | Type   | Description  |
+======+========+==============+
| host | String | Node hostname|
+------+--------+--------------+
| port | int    | Node Port    |
+------+--------+--------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/node/connect" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"host\":\"string\",\"port\":0}"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "connectedTo": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
 
__________

.. http:post:: /node/connectedPeers
   
*Returns the list of all connected sidechain node peers*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/node/connectedPeers" -H "accept: application/json"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "peers": [
            {
              "address": "string",
              "lastSeen": 0,
              "name": "string",
              "connectionType": "string"
            }
          ]
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
 
_______


.. http:post:: /node/blacklistedPeers
   
*Returns the list of all blacklisted sidechain node peers*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/node/blacklistedPeers" -H "accept: application/json"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "addresses": [
            "string"
          ]
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }


=====
**Sidechain Mainchain Operations**
=====


.. http:post:: /mainchain/bestBlockReferenceInfo
   
*Returns the best MC block header which has already been included in a SC block. Returns:*

   * Mainchain block reference hash with the most height;
   * Its height in mainchain;
   * Sidechain block ID which contains this MC block reference.

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/mainchain/bestBlockReferenceInfo" -H "accept: application/json"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "blockReferenceInfo": {
            "mainchainHeaderSidechainBlockId": "a9fd0eee294ee95daad3b72e1f307b52d6b34591dc0c211e49238634c68ecac2",
            "mainchainReferenceDataSidechainBlockId": "a9fd0eee294ee95daad3b72e1f307b52d6b34591dc0c211e49238634c68ecac2",
            "hash": "0e9329f275d8e5081cb10b605a767841eed9d6b4a49e550114bde0ca96fd375c",
            "parentHash": "00ecbbcb1beb5c262f4638d8ac9c9dd5f1e5474f8d97114a426f53d856eccd7a",
            "height": 255
          }
        }
      }

_______


.. http:post:: /mainchain/genesisBlockReferenceInfo
   
*Reference to Genesis Block*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/mainchain/genesisBlockReferenceInfo" -H "accept: application/json"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "blockReferenceInfo": {
            "mainchainHeaderSidechainBlockId": "5392e4e8f0f02b00600604d9e65d606418e9e4788552eb0a02629ea9bf6d2a74",
            "mainchainReferenceDataSidechainBlockId": "5392e4e8f0f02b00600604d9e65d606418e9e4788552eb0a02629ea9bf6d2a74",
            "hash": "0536ec69de7f5ec3c8161bc34a014ffe7cae112cab03770972e45fd15da2de82",
            "parentHash": "06660749307d87444d627c3c8b7d795706ce42a62f2b1858043dd9892f8a20d5",
            "height": 221
          }
        }
      }

______________

.. http:post:: /mainchain/blockReferenceInfoBy
   
   
**Parameters**

+--------+---------+--------------+
| Name   | Type    | Description  |
+========+=========+==============+
| hash   | String  | Block hash   |
+--------+---------+--------------+
| height | int     | Block height |
+--------+---------+--------------+
| format | boolean |              |
+--------+---------+--------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/mainchain/blockReferenceInfoBy" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"hash\":\"string\",\"height\":0,\"format\":false}"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "blocReferencekInfo": {
            "hash": "string",
            "parentHash": "string",
            "height": 0,
            "sidechainBlockId": "string"
          },
          "blockHex": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }


____________


.. http:post:: /mainchain/blockReferenceByHash

*Reference block by hash*
   
   
**Parameters**

+--------+---------+-------------+
| Name   | Type    | Description |
+========+=========+=============+
| hash   | String  | Block hash  |
+--------+---------+-------------+
| format | boolean |             |
+--------+---------+-------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST "http://127.0.0.1:9086/mainchain/blockReferenceByHash" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"hash\":\"string\",\"format\":false}"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
          "blockReference": {
            "header": {
              "mainchainHeaderBytes": "string",
              "version": 0,
              "hashPrevBlock": "string",
              "hashMerkleRoot": "string",
              "hashReserved": "string",
              "hashSCMerkleRootsMap": "string",
              "time": 0,
              "bits": 0,
              "nonce": "string",
              "solution": "string"
            },
            "sidechainRelatedAggregatedTransaction": {
              "id": "string",
              "fee": 0,
              "timestamp": 0,
              "mc2scTransactionsMerkleRootHash": "string",
              "newBoxes": [
                {
                  "id": "string",
                  "proposition": {
                    "publicKey": "string"
                  },
                  "value": 0,
                  "nonce": 0,
                  "activeFromWithdrawalEpoch": 0,
                  "typeId": 0
                }
              ]
            },
            "merkleRoots": [
              {
                "key": "string",
                "value": "string"
              }
            ]
          },
          "blockHex": "string"
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }


