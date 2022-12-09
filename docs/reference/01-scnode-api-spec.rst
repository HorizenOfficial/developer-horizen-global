Sidechain Node API spec
~~~~~~~~~~~~~~~~~~~~~~
=====
**Sidechain Block operations**
=====


.. http:post:: /block/findById

*Returns the block with the specified ID, together with its height in the blockchain*

**Parameters**

+---------+--------+----------+------------------+
| Name    | Type   | Required | Description      |
+=========+========+==========+==================+
| blockId | String | yes      | Block ID         |
+---------+--------+----------+------------------+


**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/block/findById\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"blockId\\\":\\\"0...6\\\"}\"

   |
   **Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "blockHex" : "01ed59dd9a4200a09783fe1dc9f095e7d41cbbc3cbc2c5ffb3363a150b242d7b7298e79ea00ca5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac076a9191a89fee51439600b0455db357a9899694d1cdad6a3c71bf65e6cce5328080e0ba84bf030047d0f05a139f375e238c38d0440628cbd20640ebd4739bba1bd391c6ab94033100954ea33aeb55608ff17636905d8f6874c4c57b65c543bde15386040827fbfe109ea47d7963d96146410db27b09acc5e57b3561fed39c6f1f1d8470a3b3d38a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000589128b800466a912e1571ac2ab2e952dc5d589046abad051cd5d41fce6eee6ba868d1be259691dfcafd0b440d6d87aaa54704dad753c9326bed7037596add0200000000",
	    "block" : {
	      "header" : {
		"version" : 1,
		"parentId" : "ed59dd9a4200a09783fe1dc9f095e7d41cbbc3cbc2c5ffb3363a150b242d7b72",
		"timestamp" : 1644419532,
		"forgingStakeInfo" : {
		  "blockSignPublicKey" : {
		    "publicKey" : "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
		  },
		  "vrfPublicKey" : {
		    "publicKey" : "076a9191a89fee51439600b0455db357a9899694d1cdad6a3c71bf65e6cce53280"
		  },
		  "stakeAmount" : 60000000000
		},
		"forgingStakeMerklePath" : "00",
		"vrfProof" : {
		  "vrfProof" : "47d0f05a139f375e238c38d0440628cbd20640ebd4739bba1bd391c6ab94033100954ea33aeb55608ff17636905d8f6874c4c57b65c543bde15386040827fbfe109ea47d7963d96146410db27b09acc5e57b3561fed39c6f1f1d8470a3b3d38a00"
		},
		"sidechainTransactionsMerkleRootHash" : "0000000000000000000000000000000000000000000000000000000000000000",
		"mainchainMerkleRootHash" : "0000000000000000000000000000000000000000000000000000000000000000",
		"ommersMerkleRootHash" : "0000000000000000000000000000000000000000000000000000000000000000",
		"ommersCumulativeScore" : 0,
		"feePaymentsHash" : "0000000000000000000000000000000000000000000000000000000000000000",
		"signature" : {
		  "signature" : "589128b800466a912e1571ac2ab2e952dc5d589046abad051cd5d41fce6eee6ba868d1be259691dfcafd0b440d6d87aaa54704dad753c9326bed7037596add02"
		},
		"id" : "d7f2763c95381c87fb01b6b33da46539f4ef3853e7661b6da4ae5ed26c6e59cb"
	      },
	      "sidechainTransactions" : [ ],
	      "mainchainBlockReferencesData" : [ ],
	      "mainchainHeaders" : [ ],
	      "ommers" : [ ],
	      "timestamp" : 1644419532,
	      "parentId" : "ed59dd9a4200a09783fe1dc9f095e7d41cbbc3cbc2c5ffb3363a150b242d7b72",
	      "id" : "d7f2763c95381c87fb01b6b33da46539f4ef3853e7661b6da4ae5ed26c6e59cb"
	    },
	    "height" : 4
	  }
	}

_____

   .. http:post:: /block/findLastIds
   
*Returns an array with the ids of the last x blocks*  
   
**Parameters**

+---------+--------+----------+-----------------------------------------+
| Name    | Type   | Required |          Description                    |
+=========+========+==========+=========================================+
|  number |  int   |   yes    | Retrieves the last x number of block ids|
+---------+--------+----------+-----------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/block/findLastIds\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"number\\\":10}\"
      
      
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
   
*Returns a sidechain block Id by its height in the blockchain*  
   
**Parameters**

+---------+--------+----------+----------------------------------------+
| Name    | Type   | Required |          Description                   |
+=========+========+==========+========================================+
|  height |  int   |   yes    | Retrieves block ID by its height       |
+---------+--------+----------+----------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/block/findIdByHeight\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"height\\\":100}\"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
         "result":{
            "blockId":"e8c92a6c217a7dced190b729a7815f0be6a011ea23a38e083e79298bb66620e7"
         }
      }

_____

 .. http:post:: /block/best
   
*Returns best sidechain block id and height in active chain*
   
**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/block/best\" -H \"accept: application/json\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result": {
	    "block": {
	      "header": {
		"version": 1,
		"parentId": "ed59dd9a4200a09783fe1dc9f095e7d41cbbc3cbc2c5ffb3363a150b242d7b72",
		"timestamp": 1644419532,
		"forgingStakeInfo": {
		  "blockSignPublicKey": {
		    "publicKey": "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
		  },
		  "vrfPublicKey": {
		    "publicKey": "076a9191a89fee51439600b0455db357a9899694d1cdad6a3c71bf65e6cce53280"
		  },
		  "stakeAmount": 60000000000
		},
		"forgingStakeMerklePath": "00",
		"vrfProof": {
		  "vrfProof": "47d0f05a139f375e238c38d0440628cbd20640ebd4739bba1bd391c6ab94033100954ea33aeb55608ff17636905d8f6874c4c57b65c543bde15386040827fbfe109ea47d7963d96146410db27b09acc5e57b3561fed39c6f1f1d8470a3b3d38a00"
		},
		"sidechainTransactionsMerkleRootHash": "0000000000000000000000000000000000000000000000000000000000000000",
		"mainchainMerkleRootHash": "0000000000000000000000000000000000000000000000000000000000000000",
		"ommersMerkleRootHash": "0000000000000000000000000000000000000000000000000000000000000000",
		"ommersCumulativeScore": 0,
		"feePaymentsHash": "0000000000000000000000000000000000000000000000000000000000000000",
		"signature": {
		  "signature": "589128b800466a912e1571ac2ab2e952dc5d589046abad051cd5d41fce6eee6ba868d1be259691dfcafd0b440d6d87aaa54704dad753c9326bed7037596add02"
		},
		"id": "d7f2763c95381c87fb01b6b33da46539f4ef3853e7661b6da4ae5ed26c6e59cb"
	      },
	      "sidechainTransactions": [],
	      "mainchainBlockReferencesData": [],
	      "mainchainHeaders": [],
	      "ommers": [],
	      "timestamp": 1644419532,
	      "parentId": "ed59dd9a4200a09783fe1dc9f095e7d41cbbc3cbc2c5ffb3363a150b242d7b72",
	      "id": "d7f2763c95381c87fb01b6b33da46539f4ef3853e7661b6da4ae5ed26c6e59cb"
	    },
	    "height": 4
	  }
	}

_____

 .. http:post:: /block/getFeePayments
   
*Returns the list of ZenBoxes that represents the forgers fee payments paid after the given block was applied.*
   
**Parameters**

+---------+--------+----------+----------------------------------------+
| Name    | Type   | Required |          Description                   |
+=========+========+==========+========================================+
| blockId | String | yes      | Block ID                               |
+---------+--------+----------+----------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/block/getFeePayments\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"blockId\\\":\\\"0...6\\\"}\"
      
      
**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "feePayments" : [ {
	      "nonce" : -9087003896463582454,
	      "id" : "7fe62e862d531d6598c57905754f17875a68cc7848723fa3c42fcc483e7f5a0e",
	      "isCustom" : false,
	      "value" : 941,
	      "typeName" : "ZenBox",
	      "proposition" : {
		"publicKey" : "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
	      }
	    }, {
	      "nonce" : 1359254115016647210,
	      "id" : "e23aea7695d1956530771b3f6446790c688c59e77fc41f57730888d5f04c3508",
	      "isCustom" : false,
	      "value" : 260,
	      "typeName" : "ZenBox",
	      "proposition" : {
		"publicKey" : "05e47de1dd136b1d92a65758db781e1145677865a8bb3412dcac3ab65e8d071c"
	      }
	    } ]
	}
 

_____

.. http:post:: /block/findBlockInfoById

*Returns SidechainBlockInfo for a single block and if it is in the active chain.*

**Parameters**

+---------+--------+----------+------------------+
| Name    | Type   | Required | Description      |
+=========+========+==========+==================+
| blockId | String | yes      | Block ID         |
+---------+--------+----------+------------------+


**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/block/findBlockInfoById\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"blockId\\\":\\\"0...6\\\"}\"

   |
   **Example response**:

   .. sourcecode:: http

	{
	  "result": {
	    "blockInfo": {
	      "height": 4,
	      "score": 4,
	      "parentId": "ed59dd9a4200a09783fe1dc9f095e7d41cbbc3cbc2c5ffb3363a150b242d7b72",
	      "timestamp": 1644419532,
	      "semanticValidity": "Valid",
	      "mainchainHeaderBaseInfo": [],
	      "mainchainReferenceDataHeaderHashes": [],
	      "withdrawalEpochInfo": {
		"epoch": 0,
		"lastEpochIndex": 1
	      },
	      "vrfOutputOpt": {
		"bytes": "41b2c57d834fa5a479871022c7af3992c80ddbe5c205efcc1e56219bc2cc8c33"
	      },
	      "lastBlockInPreviousConsensusEpoch": "650fe8657567b3b7779d30858177b1ba24b7bef6be250b443fca4e1bbeb9293a"
	    },
	    "isInActiveChain": true
	  }
	}

_____

.. http:post:: /block/startForging
   
*Starts forging*  
   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/block/startForging\" -H \"accept: application/json\"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {}
      }

_____

 .. http:post:: /block/stopForging
   
*Stops forging*  
   
**No Parameters**
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/block/stopForging\" -H \"accept: application/json\"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {}
      }

_____


   .. http:post:: /block/generate
   
*Tries to generate new block by epoch and slot number.*  
*Returns id of generated sidechain block.*
   
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

      curl -X POST \"http://127.0.0.1:9086/block/generate\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"epochNumber\\\":3,\\\"slotNumber\\\":45}\"
      
      
**Example response**:

   .. sourcecode:: http
   
      {
        "result": {
          "blockId": "7f25d35aadae65062033757e5049e44728128b7405ff739070e91d753b419094"
        }
      }
      
_____

   .. http:post:: /block/forgingInfo
   
*Returns forging info*
   
**No Parameters**
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/block/forgingInfo\" -H \"accept: application/json\"
      
      
**Example response**:

   .. sourcecode:: http
  
	{
	  "result" : {
	    "consensusSecondsInSlot" : 120,
	    "consensusSlotsInEpoch" : 720,
	    "bestEpochNumber" : 5,
	    "bestSlotNumber" : 4,
	    "forgingEnabled" : false
	  }
	} 
_____

=====
**Sidechain Transaction operations**
=====

.. http:post:: /transaction/allTransactions

*Returns all transactions in the memory pool.*  
   
**Parameters**

+--------+---------+----------+---------------------------------------------------------------------------------------------------------+
| Name   | Type    | Required | Description                                                                                             |
+========+=========+==========+=========================================================================================================+
| format | boolean | no       | Returns an array of transaction ids if format=false, otherwise a JSONObject for each transaction        |
+--------+---------+----------+---------------------------------------------------------------------------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9087/transaction/allTransactions\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"format\\\":true}\"
      
      
**Example response**:

   .. sourcecode:: http
  
	{
	  "result" : {
	    "transactions" : [ {
	      "modifierTypeId" : 2,
	      "id" : "c93924cbd905be02f4e4ed03aded33e8d2be77482e9566c32a8785238720ea80",
	      "newBoxes" : [ {
		"nonce" : -7274338835981510232,
		"id" : "0226207ce3de087a519ed0722eb20d16833c8bddf425b649d8de794aed3c7d9b",
		"isCustom" : false,
		"value" : 2000000000,
		"typeName" : "ZenBox",
		"proposition" : {
		  "publicKey" : "51c2d4c69602f30c8935551a076dc478eb196531996bb4dde4e345e115d3771a"
		}
	      } ],
	      "fee" : 0,
	      "version" : 1,
	      "unlockers" : [ {
		"boxKey" : {
		  "signature" : "3edf5dc31fb487d9a47f2098f873d6d6a4276acc42190edf3e308a5ba0335912a8b223fdd84bcfaccb9f66e0b77f0f0acfb3a28248656a4e2231410f1e525605"
		},
		"closedBoxId" : "a2a1f8ef8ed1d4056a32e8a588574f5d8bfa233fdd4060b231a2b8b69a5ac17c"
	      } ],
	      "isCustom" : false,
	      "typeName" : "SidechainCoreTransaction"
	    } ]
	  }
	}
   
      
_____

   .. http:post:: /transaction/findById
   
* *blockHash set -> Searches in block referenced by blockHash (do not care about txIndex parameter)*
* *blockHash not set, txIndex = true -> Searches in memory pool, if not found, search in the whole blockchain*
* *blockHash not set, txIndex = false -> Searches in memory pool*
   
**Parameters**

+------------------+---------+-------------------------------------------------------------------------------------------------+
| Name             | Type    | Description                                                                                     |
+==================+=========+=================================================================================================+
| transactionId    | String  | Finds by Transaction Id                                                                         |
+------------------+---------+-------------------------------------------------------------------------------------------------+
| blockHash        | String  | Searches in block referenced by blockHash (does not care about txIndex parameter)               |
+------------------+---------+-------------------------------------------------------------------------------------------------+
| transactionIndex | boolean | txIndex = true -> Searches in memory pool, if not found, searches in the whole blockchain       |
+------------------+---------+-------------------------------------------------------------------------------------------------+
| format           | boolean | If format =  true, retuns a JSONObject, otherwise returns the transaction as byte serialization |
+------------------+---------+-------------------------------------------------------------------------------------------------+
   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9087/transaction/findById\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"transactionId\\\":\\\"string\\\",\\\"blockHash\\\":\\\"string\\\",\\\"transactionIndex\\\":false,\\\"format\\\":true}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transaction" : {
	      "modifierTypeId" : 2,
	      "id" : "a8adda1e352f9aefa0b157bba3578c46390b13b55dcac6fa59d87d0feeb15025",
	      "newBoxes" : [ {
		"nonce" : -633504681414039135,
		"id" : "7238937c1e947a4f9d02a76bcb551dc4d366b71b3bda83947ae90136d8dd8ceb",
		"isCustom" : false,
		"value" : 1500000000,
		"typeName" : "ZenBox",
		"proposition" : {
		  "publicKey" : "76e1a22f78459ff60b6e7bba4067b05f341b1206792c1f1029e38906d809884b"
		}
	      } ],
	      "fee" : 0,
	      "version" : 1,
	      "unlockers" : [ {
		"boxKey" : {
		  "signature" : "82c634e922e2c681cd1dbb5c4cd367ce48acf3037d707cd885ad3cc25ab15dbe84c2ff88b719a164e790019e9839ce9fa9b1fe0802fae6566331024af1f42709"
		},
		"closedBoxId" : "4cf6109023f18ba1364be15071b5d62983247e37d52fa1489f158039bbde7772"
	      } ],
	      "isCustom" : false,
	      "typeName" : "SidechainCoreTransaction"
	    }
	  }
	}

_________

.. http:post:: /transaction/decodeTransactionBytes
   
*Returns a JSON representation of a transaction given its byte serialization*


   
**Parameters**

+------------------+--------+----------+----------------------------------------+
| Name             | Type   | Required |          Description                   |
+==================+========+==========+========================================+
| transactionBytes | String |   yes    |         byte String                    |
+------------------+--------+----------+----------------------------------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9087/transaction/decodeTransactionBytes\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"transactionBytes\\\":\\\"string\\\"}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transaction" : {
	      "modifierTypeId" : 2,
	      "id" : "a8adda1e352f9aefa0b157bba3578c46390b13b55dcac6fa59d87d0feeb15025",
	      "newBoxes" : [ {
		"nonce" : -633504681414039135,
		"id" : "7238937c1e947a4f9d02a76bcb551dc4d366b71b3bda83947ae90136d8dd8ceb",
		"isCustom" : false,
		"value" : 1500000000,
		"typeName" : "ZenBox",
		"proposition" : {
		  "publicKey" : "76e1a22f78459ff60b6e7bba4067b05f341b1206792c1f1029e38906d809884b"
		}
	      } ],
	      "fee" : 0,
	      "version" : 1,
	      "unlockers" : [ {
		"boxKey" : {
		  "signature" : "82c634e922e2c681cd1dbb5c4cd367ce48acf3037d707cd885ad3cc25ab15dbe84c2ff88b719a164e790019e9839ce9fa9b1fe0802fae6566331024af1f42709"
		},
		"closedBoxId" : "4cf6109023f18ba1364be15071b5d62983247e37d52fa1489f158039bbde7772"
	      } ],
	      "isCustom" : false,
	      "typeName" : "SidechainCoreTransaction"
	    }
	  }
	}
      
______


.. http:post:: /transaction/createCoreTransaction
   
*Creates and signs a Sidechain core transaction, specifying inputs and outputs. Returns the new transaction as a hex string if format = false, otherwise its JSON representation.*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
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

      curl -X POST \"http://127.0.0.1:9087/transaction/createCoreTransaction\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"transactionInputs\\\":[{\\\"boxId\\\":\\\"string\\\"}],\\\"regularOutputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"withdrawalRequests\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"forgerOutputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"blockSignPublicKey\\\":\\\"string\\\",\\\"vrfPubKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"format\\\":false}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transactionBytes" : "0101b8a6d6b9070282750e3a53818ece2c116f6978401115c394dbe1ffdc184fb9ab9a8aca968927020194ed9aa9928393fde71280023e1afcc2578cfbcb68bff90b6d2785dbbd6c7bebc8010201e631e4b978630c48afecaaefbd4141634367386fd270f70be17dc95318b685cebd50fad14d15301c6befc03db798e6b783edd9c400e088914fba201f7b4f270c"
	  }
	}
      
______


.. http:post:: /transaction/createCoreTransactionSimplified
   
*Creates and signs a Sidechain core transaction, specifying inputs and outputs. Returns the new transaction as a hex string if format = false, otherwise its JSON representation.*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

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

      curl -X POST \"http://127.0.0.1:9087/transaction/createCoreTransactionSimplified\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"regularOutputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"withdrawalRequests\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"forgerOutputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"blockSignPublicKey\\\":\\\"string\\\",\\\"vrfPubKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"fee\\\":0,\\\"format\\\":true}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transaction" : {
	      "modifierTypeId" : 2,
	      "id" : "b8a997743d5f4a7f7c43141fa5c156494ed7ddd2b52a26274a3eea0fe76aa6a6",
	      "newBoxes" : [ {
		"nonce" : 1797084183504923750,
		"id" : "f1d9b9a010e069885a3b8235b80b2249da53ce8a45dab1169d0d27911f5dc3ee",
		"isCustom" : false,
		"value" : 10,
		"typeName" : "ZenBox",
		"proposition" : {
		  "publicKey" : "94ed9aa9928393fde71280023e1afcc2578cfbcb68bff90b6d2785dbbd6c7beb"
		}
	      }, {
		"nonce" : -1293113557566329474,
		"id" : "3a9383a555ad292f2cad30ce8d2c194b97fa0a35f9e8c5baa267b8c093a5cb58",
		"isCustom" : false,
		"value" : 999999989,
		"typeName" : "ZenBox",
		"proposition" : {
		  "publicKey" : "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
		}
	      } ],
	      "fee" : 1,
	      "version" : 1,
	      "unlockers" : [ {
		"boxKey" : {
		  "signature" : "508a896275014539c77705bcf276eaf613674d11c5d2211bd9ba9e2fb85f653e6efe49d0554297667932d312aed122bd8440a05ea4355aa9279f7d4e8947cc06"
		},
		"closedBoxId" : "82750e3a53818ece2c116f6978401115c394dbe1ffdc184fb9ab9a8aca968927"
	      } ],
	      "isCustom" : false,
	      "typeName" : "SidechainCoreTransaction"
	    }
	  }
	}

______


.. http:post:: /transaction/sendCoinsToAddress
   
*Creates and signs a regular transaction, specifying outputs and fee. Then validates and sends the transaction. Returns the id of the transaction*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

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

      curl -X POST \"http://127.0.0.1:9087/transaction/sendCoinsToAddress\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"outputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"fee\\\":0}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transactionId" : "bc4cc8d2469f49f89d69f5b77f7a890e40ce3ac0e971bcabd6db6a78131fa2b5"
	  }
	}
      
____

.. http:post:: /transaction/withdrawCoins
   
*Creates and signs a regular transaction, specifying withdrawal outputs and fee. Then validates and sends the transaction. Returns the id of the transaction.*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
**Parameters**

   .. sourcecode:: http

	{
	  "outputs": [
	    {
	      "mainchainAddress": "string",
	      "value": 0
	    }
	  ],
	  "fee": 0
	}

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9087/transaction/withdrawCoins\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"outputs\\\":[{\\\"mainchainAddress\\\":\\\"string\\\",\\\"value\\\":0}],\\\"fee\\\":0}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transactionId" : "ccaa312d3eded27469a8241ccc885b19361687cadef0bdf0511a20310ef46310"
	  }
	}
      
____

.. http:post:: /transaction/makeForgerStake
   
*Creates and signs a Sidechain core transaction, specifying forger stake outputs and fee. Then validates and sends the transaction. Returns the id of the transaction*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
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

      curl -X POST \"http://127.0.0.1:9087/transaction/makeForgerStake\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"outputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"blockSignPublicKey\\\":\\\"string\\\",\\\"vrfPubKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"fee\\\":0}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transactionId" : "ccaa312d3eded27469a8241ccc885b19361687cadef0bdf0511a20310ef46310"
	  }
	}
     
_______

.. http:post:: /transaction/spendForgingStake
   
*Creates and signs sidechain core transaction, specifying inputs and outputs. Returns the new transaction as a hex string if format = false, otherwise its JSON representation.*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
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

      curl -X POST \"http://127.0.0.1:9087/transaction/spendForgingStake\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"transactionInputs\\\":[{\\\"boxId\\\":\\\"string\\\"}],\\\"regularOutputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"forgerOutputs\\\":[{\\\"publicKey\\\":\\\"string\\\",\\\"blockSignPublicKey\\\":\\\"string\\\",\\\"vrfPubKey\\\":\\\"string\\\",\\\"value\\\":0}],\\\"format\\\":false}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transaction" : {
	      "modifierTypeId" : 2,
	      "id" : "081b668f9e2e63c81be89a5e0ca4a7c9166cefde59b026072e3a89704919767b",
	      "newBoxes" : [ {
		"nonce" : -219144346324825135,
		"id" : "431d60e42c2503fdfbe9d6d530d04a75c051de32905a68d88fc86830f3d13aae",
		"isCustom" : false,
		"value" : 10,
		"typeName" : "ZenBox",
		"proposition" : {
		  "publicKey" : "94ed9aa9928393fde71280023e1afcc2578cfbcb68bff90b6d2785dbbd6c7beb"
		}
	      } ],
	      "fee" : 1,
	      "version" : 1,
	      "unlockers" : [ {
		"boxKey" : {
		  "signature" : "66c56f5a9dacfc0e4df5dbb1b4bb95fbd66b3d6e3b626d9f83f72587410495e90dfe8f310a57e8c3bd89c315a54f97b7f239e5e2fd5e656bbfe7184650eb8d0e"
		},
		"closedBoxId" : "1076fded2f91d1231247764e05ecb44c605012dbbcac95e9ce0aced3619484d3"
	      } ],
	      "isCustom" : false,
	      "typeName" : "SidechainCoreTransaction"
	    }
	  }
	}
     
______


.. http:post:: /transaction/sendTransaction
   
*Validates and sends a transaction, given its serialization as input. Then returns the id of the transaction.*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
**Parameters**

+------------------+--------+--------------------------+
| Name             | Type   | Description              |
+==================+========+==========================+
| transactionBytes | String | Signed Transaction Bytes |
+------------------+--------+--------------------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9087/transaction/sendTransaction\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"transactionBytes\\\":\\\"string\\\"}\"
      
      
**Example response**:

   .. sourcecode:: http
   
	{
	  "result" : {
	    "transactionId" : "ccaa312d3eded27469a8241ccc885b19361687cadef0bdf0511a20310ef46310"
	  }
	}

________

.. http:post:: /transaction/createKeyRotationTransaction

*Creates and signs sidechain transaction for signers or masters certificate submitter key rotation.*

**Parameters**

+---------------------+-----------+-----------------------------------------------------------------------+
| Name                | Type      |            Description                                                |
+=====================+===========+=======================================================================+
| keyType             |  int      | Key type - 0 for signers key, 1 for masters key. Min = 0. Max = 1     |
+---------------------+-----------+-----------------------------------------------------------------------+
| keyIndex            |  int      | Index of certificate submitter key                                    |
+---------------------+-----------+-----------------------------------------------------------------------+
| newKey              |  string   | Value of new key                                                      |
+---------------------+-----------+-----------------------------------------------------------------------+
| signingKeySignature |  string   | Signing key signature                                                 |
+---------------------+-----------+-----------------------------------------------------------------------+
| masterKeySignature  |  string   | Master key signature                                                  |
+---------------------+-----------+-----------------------------------------------------------------------+
| newKeySignature     |  string   | New key signature (if key type 0, then new signers key signature;     |
|                     |           | if key type 1, then master key signature). Min = 0. Max = 1.          |
+---------------------+-----------+-----------------------------------------------------------------------+
| format              |  boolean  | Optional field - true if format, false if non format                  |
+---------------------+-----------+-----------------------------------------------------------------------+
| automaticSend       |  boolean  | Optional field - true if automatic, false if not automatic            |
+---------------------+-----------+-----------------------------------------------------------------------+
| fee                 |  int      | Optional field for transaction fee                                    |
+---------------------+-----------+-----------------------------------------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/transaction/createKeyRotationTransaction\" -H \"accept: application/json\" -d \"{\\\"keyType\\\": 0, \\\"keyIndex\\\": 3, \\\"newKey\\\":\\\"string\\\", \\\"signingKeySignature\\\":\\\"string\\\", \\\"masterKeySignature\\\":\\\"string\\\", \\\"newKeySignature\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

      {
         "result": {
            "transactionId": "3c25254df2f57a524c65b5883550bb1a41130493c6440c60eb6256f4c142dbc9"
        }
      }
______

=====
**Sidechain Wallet Operations**
=====

.. http:post:: /wallet/allBoxes
   
*Returns all boxes, excluding those which ids are included in excludeBoxIds list*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
**Parameters**

+------------------+--------------+----------+-------------------------------------------------------------+
| Name             | Type         | Required | Description                                                 |
+==================+==============+==========+=============================================================+
| boxTypeClass     | String       | No       | Type of boxes. If not specified, returns all existing boxes |
+------------------+--------------+----------+-------------------------------------------------------------+
| excludeBoxIds    | String Array | No       | ID of boxes to exclude                                      |
+------------------+--------------+----------+-------------------------------------------------------------+


**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/allBoxes\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"boxTypeClass\\\":\\\"string\\\",\\\"excludeBoxIds\\\":[\\\"string\\\"]}\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result": {
	    "boxes": [
	      {
		"nonce": -673297840433871900,
		"id": "1076fded2f91d1231247764e05ecb44c605012dbbcac95e9ce0aced3619484d3",
		"vrfPubKey": {
		  "publicKey": "53db9055f6eff032310ca618c2bf8edea98927c24a472ff69d0eb0fed6285e1c00"
		},
		"blockSignProposition": {
		  "publicKey": "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
		},
		"isCustom": false,
		"value": 100000000000,
		"typeName": "ForgerBox",
		"proposition": {
		  "publicKey": "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
		}
	      },
	      {
		"nonce": -3970212005742197000,
		"id": "82750e3a53818ece2c116f6978401115c394dbe1ffdc184fb9ab9a8aca968927",
		"isCustom": false,
		"value": 1000000000,
		"typeName": "ZenBox",
		"proposition": {
		  "publicKey": "47286ba429e486767d35e79702206d1181894487f8d74550cb1eec3b0bd9b5f3"
		}
	      },
	      {
		"nonce": -8654764026769776000,
		"id": "e40ab88ee303e914de929971b81ded0fdec66f9aed48736658fe2b440014d867",
		"isCustom": false,
		"value": 2000000000,
		"typeName": "ZenBox",
		"proposition": {
		  "publicKey": "51c2d4c69602f30c8935551a076dc478eb196531996bb4dde4e345e115d3771a"
		}
	      },
	      {
		"nonce": -633504681414039200,
		"id": "7238937c1e947a4f9d02a76bcb551dc4d366b71b3bda83947ae90136d8dd8ceb",
		"isCustom": false,
		"value": 1500000000,
		"typeName": "ZenBox",
		"proposition": {
		  "publicKey": "76e1a22f78459ff60b6e7bba4067b05f341b1206792c1f1029e38906d809884b"
		}
	      }
	    ]
	  }
      
______

.. http:post:: /wallet/coinsBalance
   
*Returns the global balance for all types of boxes*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
**No Parameters**


   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/coinsBalance\" -H \"accept: application/json\" 
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "balance" : 103000000000
	  }
	}

______

.. http:post:: /wallet/balanceOfType
   
*Returns the global balance for given type of boxes*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
**Parameters**

+------------------+--------------+----------+----------------+
| Name             | Type         | Required | Description    |
+==================+==============+==========+================+
| boxType          | String       | Yes      | Type of boxes. |
+------------------+--------------+----------+----------------+


**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/balanceOfType\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"boxType\\\":\\\"string\\\"}\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "balance" : 103000000000
	  }
	}
      
______


.. http:post:: /wallet/createPrivateKey25519
   
*Creates new secret and returns corresponding address (public key)*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/createPrivateKey25519\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "proposition" : {
	      "publicKey" : "aea4154c7d88e956d480b913e5c3277db994b6d8f23240e7d49f3997d4e12c24"
	    }
	  }
	}
      
______

.. http:post:: /wallet/createVrfSecret
   
*Creates new Vrf secret and returns corresponding public key*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/createVrfSecret\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "proposition" : {
	      "publicKey" : "4439cbfd50af1b846e5ef06889d3192ef7a459bdd4640dc6da506062de43113c80"
	    }
	  }
	}

________

.. http:post:: /wallet/allPublicKeys
   
*Returns the list of all wallet’s propositions (public keys)*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)
   
**Parameters**

+------------------+--------------+----------+---------------------------------------------------------------+
| Name             | Type         | Required | Description                                                   |
+==================+==============+==========+===============================================================+
| proptype         | String       | No       | Proposition Type. If not specified, returns all propositions. |
+------------------+--------------+----------+---------------------------------------------------------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/allPublicKeys\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{}\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "propositions" : [ {
	      "publicKey" : "b78cf604e40a1a76b3e4736f6126b3a46b2ba7abf90101078fa1d9f098972a1d00"
	    }, {
	      "publicKey" : "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
	    }, {
	      "publicKey" : "accb2fbee54955df172a19506c8c35630e4146090d1e583858a025eea207583b80"
	    }, {
	      "publicKey" : "cc0161709c7589f8f6a4db76f78060ffa32861071bf8e89cace82521a42ee42e00"
	    }, {
	      "publicKey" : "a6b218079d2f476a47a849e2bb6cfd01427a631e9a1c8467e2951f4e524fa92100"
	    }, {
	      "publicKey" : "8c7538228452600d368b119015a230e5ae1a3a2eef500e02a92c55643c868c3c00"
	    }, {
	      "publicKey" : "7a3d71650ce54add0a7f773b8d37621dddc250390a09b725c66fad3ce606570d80"
	    }, {
	      "publicKey" : "9b64fc8291e238761b3262c833404268d9f4077c5f253fa177b113753832500980"
	    }, {
	      "publicKey" : "3650bcc96e3533d9352f5826efd1f5723cc2594d5aeb7efba228a8d23944492f80"
	    }, {
	      "publicKey" : "47286ba429e486767d35e79702206d1181894487f8d74550cb1eec3b0bd9b5f3"
	    }, {
	      "publicKey" : "94ed9aa9928393fde71280023e1afcc2578cfbcb68bff90b6d2785dbbd6c7beb"
	    }, {
	      "publicKey" : "51c2d4c69602f30c8935551a076dc478eb196531996bb4dde4e345e115d3771a"
	    }, {
	      "publicKey" : "aea4154c7d88e956d480b913e5c3277db994b6d8f23240e7d49f3997d4e12c24"
	    }, {
	      "publicKey" : "4439cbfd50af1b846e5ef06889d3192ef7a459bdd4640dc6da506062de43113c80"
	    } ]
	  }
	}

________

.. http:post:: /wallet/importSecret

*Import a secret into the wallet*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

**Parameters**

+------------------+--------------+----------+--------------------------------------+
| Name             | Type         | Required | Description                          |
+==================+==============+==========+======================================+
| privKey          | String       |   Yes    | Secret to import inside the wallet   |
+------------------+--------------+----------+--------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/importSecret\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"privKey\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	      "proposition" : "4439cbfd50af1b846e5ef06889d3192ef7a459bdd4640dc6da506062de43113c80"
	  }
	}

________

.. http:post:: /wallet/exportSecret

*Export a secret corresponding to a public key from the wallet*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

**Parameters**

+------------------+--------------+----------+--------------------------------------+
| Name             | Type         | Required | Description                          |
+==================+==============+==========+======================================+
| publickey        | String       |   Yes    | PublicKey to export                  |
+------------------+--------------+----------+--------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/exportSecret\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"publicKey\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	      "privKey" : "002b64a179846da0b13ed5b4354dbdeb85a500c60ccb12c01a0fded2bd5d8b58e58bb8302e2b46763c830099c6fd862da0774a7b8f1323db5bbd96d3652176e485"
	  }
	}

________

.. http:post:: /wallet/importSecrets

*Import all the secret from a file. The file must contain in each line: SECRET + " " + PUBLICKEYS*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

**Parameters**

+------------------+--------------+----------+--------------------------------------+
| Name             | Type         | Required | Description                          |
+==================+==============+==========+======================================+
| path             | String       |   Yes    | Path to the file to import           |
+------------------+--------------+----------+--------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/importSecrets\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"path\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
            "successfullyAdded" : 3,
            "failedToAdd": 1,
            "summary": [
                {
                    "lineNumber": 2,
                    "description": "string"
                }
            ]
	  }
	}

________

.. http:post:: /wallet/dumpSecrets

*Dump all the wallet secrets to a file*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

**Parameters**

+------------------+--------------+----------+--------------------------------------+
| Name             | Type         | Required | Description                          |
+==================+==============+==========+======================================+
| path             | String       |   Yes    | Path where the file will be created  |
+------------------+--------------+----------+--------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/wallet/dumpSecrets\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"path\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
            "status": "string"
	  }
	}

________

=====
**Sidechain Node operations**
=====


.. http:post:: /node/allPeers
   
*Returns the list of all sidechain node peers*

   
**No Parameters**

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/node/allPeers\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "peers" : [ {
	      "address" : "/127.0.0.1:8430",
	      "lastSeen" : 1650012289802,
	      "name" : "node1",
	      "connectionType" : "Outgoing"
	    }, {
	      "address" : "/127.0.0.1:8431",
	      "lastSeen" : 1650012291959,
	      "name" : "node2",
	      "connectionType" : "Outgoing"
	    } ]
	  }
	}
      
__________

.. http:post:: /node/connect
   
*Sends the request to connect to a sidechain node*

   
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

      curl -X POST \"http://127.0.0.1:9086/node/connect\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"host\\\":\\\"string\\\",\\\"port\\\":0}\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "connectedTo" : "/127.0.0.1:8330"
	  }
	}
 
__________

.. http:post:: /node/connectedPeers
   
*Returns the list of all connected sidechain node peers*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/node/connectedPeers\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "peers" : [ {
	      "address" : "/127.0.0.1:8430",
	      "lastSeen" : 1650012289802,
	      "name" : "node1",
	      "connectionType" : "Outgoing"
	    }, {
	      "address" : "/127.0.0.1:8431",
	      "lastSeen" : 1650012291959,
	      "name" : "node2",
	      "connectionType" : "Outgoing"
	    } ]
	  }
	}
 
_______

.. http:post:: /node/blacklistedPeers
   
*Returns the list of all blacklisted sidechain node peers*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/node/blacklistedPeers\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "addresses" : [ ]
	  }
	}
_______


.. http:post:: /node/stop
   
*Initiates a graceful stop procedure for the sidechain node. Returns an empty object*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/node/stop\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
      {
        "result": {
        },
        "error": {
          "code": "string",
          "description": "string",
          "detail": "string"
        }
      }
_______

.. http:post:: /node/storageVersions
   
*Returns the list of all node storage versions*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/node/storageVersions\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result": {
	    "listOfVersions": {
	      "additionalProp1": "string",
	      "additionalProp2": "string",
	      "additionalProp3": "string"
	    }
	  },
	  "error": {
	    "code": "string",
	    "description": "string",
	    "detail": "string"
	  }
	}
_______

.. http:post:: /node/sidechainId
   
*Returns the sidechain id*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/node/sidechainId\" -H \"accept: application/json\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "sidechainId" : "0a1c910e65d7feb6f1dd53342cc212584d24f0ce643dbba88312e5630714850b"
	  }
	}
_______

=====
**Sidechain Mainchain Operations**
=====


.. http:post:: /mainchain/bestBlockReferenceInfo
   
*Returns the best MC block header which has already been included in a SC block. Returns:*

   * *Mainchain block reference hash with the most height;*
   * *Its height in mainchain;*
   * *Sidechain block ID which contains this MC block reference.*

   
**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/mainchain/bestBlockReferenceInfo\" -H \"accept: application/json\"
      
      
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

      curl -X POST \"http://127.0.0.1:9086/mainchain/genesisBlockReferenceInfo\" -H \"accept: application/json\"
      
      
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
   
*Finds Mainchain Block reference by its hash or by its height*
   
**Parameters**

+--------+---------+-------------------------------------------------------------------------+
| Name   | Type    | Description                                                             |
+========+=========+=========================================================================+
| hash   | String  | Block hash                                                              |
+--------+---------+-------------------------------------------------------------------------+
| height | int     | Block height                                                            |
+--------+---------+-------------------------------------------------------------------------+
| format | boolean | If false, returns block hex format, otherwise returns JSONObject format |
+--------+---------+-------------------------------------------------------------------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/mainchain/blockReferenceInfoBy\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"hash\\\":\\\"string\\\",\\\"height\\\":0,\\\"format\\\":false}\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "blockReferenceInfo" : {
	      "mainchainHeaderSidechainBlockId" : "650fe8657567b3b7779d30858177b1ba24b7bef6be250b443fca4e1bbeb9293a",
	      "mainchainReferenceDataSidechainBlockId" : "650fe8657567b3b7779d30858177b1ba24b7bef6be250b443fca4e1bbeb9293a",
	      "hash" : "09eddf0dbf848a6e866afd0d5dff4b2d7da6641250fcf8424b8077dab39eded2",
	      "parentHash" : "0c4a3c40b60a96874720ff48798c3d2ff62840cc46b6401e5973fa78a294e61e",
	      "height" : 420
	    }
	  }
	}


____________


.. http:post:: /mainchain/blockReferenceByHash

*Reference block by hash*
   
   
**Parameters**

+--------+---------+-------------------------------------------------------------------------+
| Name   | Type    | Description                                                             |
+========+=========+=========================================================================+
| hash   | String  | Block hash                                                              |
+--------+---------+-------------------------------------------------------------------------+
| format | boolean | If false, returns block hex format, otherwise returns JSONObject format |
+--------+---------+-------------------------------------------------------------------------+

   
**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9086/mainchain/blockReferenceByHash\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"hash\\\":\\\"string\\\",\\\"format\\\":false}\"
      
      
**Example response**:
   
   .. sourcecode:: http
      
	{
	  "result" : {
	    "blockReference" : {
	      "header" : {
		"version" : 3,
		"hashPrevBlock" : "0c4a3c40b60a96874720ff48798c3d2ff62840cc46b6401e5973fa78a294e61e",
		"hashMerkleRoot" : "fb83cf64532ae6f32197456ecad508b9970ae81aac5b8163911e44ebfa298525",
		"hashScTxsCommitment" : "29a5a7b37890d5f5b5e5b17c709edff5d624988b3396048390ad8d067f9e6130",
		"time" : 1644418188,
		"bits" : 537857783,
		"nonce" : "00004a6e2b6bfef30470d239aef5f10fbd474670f733f710c4907abc5a00002c",
		"solution" : "1a33713b030af4cf1f2da118b1641401af7422166515838d14fbb73fa6d4f9393f4aa977",
		"hash" : "09eddf0dbf848a6e866afd0d5dff4b2d7da6641250fcf8424b8077dab39eded2"
	      },
	      "data" : {
		"headerHash" : "09eddf0dbf848a6e866afd0d5dff4b2d7da6641250fcf8424b8077dab39eded2",
		"sidechainRelatedAggregatedTransaction" : {
		  "modifierTypeId" : 2,
		  "id" : "ceee25a97f6c6d232a7237567c534fa9344113f22a6d6358ae75921605220865",
		  "newBoxes" : [ {
		    "nonce" : 4237164552941399434,
		    "id" : "85a29f2ed2095fc5c8fc764061ce6c7ac85a26e42235ed12b99b5e323106e040",
		    "vrfPubKey" : {
		      "publicKey" : "076a9191a89fee51439600b0455db357a9899694d1cdad6a3c71bf65e6cce53280"
		    },
		    "blockSignProposition" : {
		      "publicKey" : "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
		    },
		    "isCustom" : false,
		    "value" : 60000000000,
		    "typeName" : "ForgerBox",
		    "proposition" : {
		      "publicKey" : "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
		    }
		  } ],
		  "version" : 1,
		  "isCustom" : false,
		  "unlockers" : [ ],
		  "fee" : 0,
		  "mc2scTransactionsMerkleRootHash" : "ceee25a97f6c6d232a7237567c534fa9344113f22a6d6358ae75921605220865",
		  "typeName" : "MC2SCAggregatedTransaction"
		},
		"existenceProof" : "0c000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000e5898923c5501dbecd48456555cf9225aa44bf3a4e84bc20ec069b4a4dcf972a00000000000000000100000000000000139b3ecbc5a42fb4f3e4ae8cb3f263dc68c4c24e514b44262baf847e0635b22d00000000000000000100000000000000cf4c9401843fc0e2b017d334787fc7cf38a6b1f04d3fa6abd12ba18cc7a9e8170000000000000000010000000000000075ebe544ca04c7aed3c225003514b6a85c07cdea695d42fa7e78d25d2bb62e380000000000000000010000000000000012cf31c4504a3e4135a8a1ef06973ed061e9cc659813ebded719c9f1ca20943a000000000000000001000000000000001cef6ce7dfc27c10d8e2b1612340fcc67dfe2909649c34b6d94379c678235520000000000000000001000000000000009722c66b0e766e57ce97cb7ab82ad27cbad4294061c5b3ddb76331307c90602300000000000000000100000000000000c1f94c50887bb99f6eed3cb27adcac769b8b6cebf24ae6e3199e996c1b534e0b000000000000000001000000000000009ef35bc5fecf5ec5ebee699fb9674c6ac47cae618b76e60f32bdfc4c3fe3073800000000000000000100000000000000cae22c26168c9275bfa5ad7aa496e94450367a19be9a142e2c6a8d3f5afaaf26000000000000000001000000000000003c411e863e54f7a1897b899027feed299445573ad779bda4c4c038b76f7499090000000000000000",
		"lowerCertificateLeaves" : [ ]
	      }
	    }
	  }
	}
_______


=====
**Certificate Submitter operations**
=====


.. http:post:: /submitter/isCertGenerationActive

*Returns if certificate generation is in progress*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/isCertGenerationActive\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "state" : false
	  }
	}

________


.. http:post:: /submitter/isCertificateSubmitterEnabled

*Returns if certificate submitter is enabled*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/isCertificateSubmitterEnabled\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "enabled" : false
	  }
	}

________


.. http:post:: /submitter/enableCertificateSubmitter

*Enables automatic certificate submission*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/enableCertificateSubmitter\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

      {
         "result": { }
      }

________

.. http:post:: /submitter/disableCertificateSubmitter

*Disables automatic certificate submission*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/disableCertificateSubmitter\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

      {
         "result": { }
      }

________

.. http:post:: /submitter/isCertificateSignerEnabled

*Returns if certificate signing option is enabled*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/isCertificateSignerEnabled\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

      {
         "result":{
            "enabled" : false
         }
      }

________


.. http:post:: /submitter/enableCertificateSigner

*Enables automatic certificate signing*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/enableCertificateSigner\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

      {
         "result": { }
      }

________


.. http:post:: /submitter/disableCertificateSigner

*Disables automatic certificate signing*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/disableCertificateSigner\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

      {
         "result": { }
      }

________

.. http:post:: /submitter/getSchnorrPublicKeyHash

*Accepts public key and returns hash of the public key.*

**Parameters**

+---------------------+---------+-----------------------------------------------------------------------+
| Name                | Type    |            Description                                                |
+=====================+=========+=======================================================================+
| schnorrPublicKey    |  string | Public key of certificate signer                                      |
+---------------------+---------+-----------------------------------------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/getSchnorrPublicKeyHash\" -H \"accept: application/json\" -d \"{\\\"schnorrPublicKey\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

      {
         "result":{
            "schnorrPublicKeyHash" : "4a2cbb9ff049b2a973c02e23f5cba3e1ac46d8bc030b75868b6510c764f0fc01"
         }
      }

________

.. http:post:: /submitter/getCertifiersKeys

*Accepts number of withdrawal epoch and returns signer keys of certificate signers.*

**Parameters**

+---------------------+---------+-----------------------------------------------------------------------+
| Name                | Type    |            Description                                                |
+=====================+=========+=======================================================================+
| withdrawalEpoch     |  int    | Withdrawal epoch of certificate signer keys                           |
+---------------------+---------+-----------------------------------------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/getCertifiersKeys\" -H \"accept: application/json\" -d \"{\\\"withdrawalEpoch\\\": 100}\"


**Example response**:

   .. sourcecode:: http

      {
         "result": {
            "certifiersKeys": {
                "signingKeys": [{
                    "publicKey": "ec4166e9225e97e90dde76089dd4edbb5ab60fb5ea60230a256ca3d2e4c2162c80"
                }, {
                    "publicKey": "3fd1d98e4d4331f31d28a4b652ac9c7b3ea5ac1b35e0ef113434307b79cd590c80"
                }, {
                    "publicKey": 'b2130ed9458ff6f917b717b4765b185e40f6139ee7546830ba8ddd1f73b37b2400"
                }, {
                    "publicKey": "ce0b8c7c4345a7fec79424cfa519d732d68aef16c7c0e5146c5efc2d9454601980"
                }, {
                    "publicKey": "08be76211383c6cd3bfa7c72d49d5a79c79efd04d297535cf0004e5cf1ba7e0b00"
                }, {
                    "publicKey": "606efe3b31cdab05fee935f58da6c88f7554f9bc55f0c6c3c577889a168aad3480"
                }, {
                    "publicKey": "f9b41abe48c176f928b39ad66520969fd66be40c47dad5964b622f2b6620590580"
                }],
                "masterKeys": [{
                    "publicKey": "9b59d065c3373a70eab20263f6511a29d4af3aa20b3d9600295dcd985381bd2580"
                }, {
                    "publicKey": "6edd6574af4d49474b981a89c8ff783b1bf3db63b2c818459ea130b4fab6bc0c80"
                }, {
                    "publicKey": "39077d62d10ca0a9639908d0e7b3d37787d84d1a6c81624371015064383da02000"
                }, {
                    "publicKey": "efd7e4f58e039f23bad6b7b5dc06c8c7a3c8f90a9f94ce6ae4164bc6ecb8f10980"
                }, {
                    "publicKey": "a62b704bcc08e4c2fc4dd2ae51e6812dfa6519fc57db77812a3123639b5e4a3380"
                }, {
                    "publicKey': "b46172f71951fe8a421ac77847821ac9f65105962f1cd2761ed9b0cf9400561500"
                }, {
                    "publicKey": "a477534cac7bad0c77f81f8b5da7aec9582cebcf95de57aa6fafbc3cd7deca2480"
                }]
            }
         }
      }

________

.. http:post:: /submitter/getKeyRotationProof

*Returns key rotation proof (key type, index of key, new key value and 2 signatures proving key rotation) if type of circuit is NaiveThresholdSignatureCircuitWithKeyRotation.*

**Parameters**

+---------------------+---------+-----------------------------------------------------------------------+
| Name                | Type    |            Description                                                |
+=====================+=========+=======================================================================+
| withdrawalEpoch     |  int    | Number of withdrawal epoch                                            |
+---------------------+---------+-----------------------------------------------------------------------+
| indexOfKey          |  int    | Index of certificate submitter key. Min = 0                           |
+---------------------+---------+-----------------------------------------------------------------------+
| keyType             |  int    | Key type - 0 for signers key, 1 for masters key. Min = 0. Max = 1     |
+---------------------+---------+-----------------------------------------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/submitter/getKeyRotationProof\" -H \"accept: application/json\" -d \"{\\\"withdrawalEpoch\\\": 100, \\\"indexOfKey\\\": 2, \\\"keyType\\\": 0}\"


**Example response**:

   .. sourcecode:: http

      {
        "result": {
          "keyType" : 0,
          "index" : 0,
          "newKey" : "2cddac0f51b4329ab6ee85ccaf4e3bbc1b80639a96e41239de978bd99d245f0a00",
          "signingKeySignature" : "1d39072beb8480edeee6dabf16ee15526bfd2170680dcc4a23d656bbb9740d1d0977f58009c19943d7964314aafc9aa0776f253ac479c708cf6ec0a51d9a9e1b",
          "masterKeySignature" : "1d39072beb8480edeee6dabf16ee15526bfd2170680dcc4a23d656bbb9740d1d0977f58009c19943d7964314aafc9aa0776f253ac479c708cf6ec0a51d9a9e1b"
        }
      }

_______


=====
**Ceased Sidechain Withdrawal operations**
=====


.. http:post:: /csw/hasCeased

*Returns current status of the Sidechain*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/csw/hasCeased\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

      {
         "result":{
            "state":true
         }
      }

________

.. http:post:: /csw/isCSWEnabled

*Returns if the Ceased Sidechain Withdrawal is enabled in the Sidechain*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/csw/isCSWEnabled\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "cswEnabled" : true
	  }
	}

________

.. http:post:: /csw/generateCswProof

*Tries to generate csw proof and returns current status of this operation.*
*Possible statuses are:*
   * *SidechainIsAlive - Sidechain is still alive;*
   * *InvalidAddress - Receiver address has invalid value: MC toaddress expected;*
   * *NoProofData - Information for given box id is missed;*
   * *ProofGenerationStarted - Started proof generation, was not started of present before;*
   * *ProofGenerationInProcess - Proof generation was started before, still in process;*
   * *ProofCreationFinished - Proof is ready.*

**This endpoint needs authentication** (See :ref:`api_authentication-label`)

**Parameters**

+-----------------+---------+---------------------+
| Name            | Type    | Description         |
+=================+=========+=====================+
| boxId           | String  | Coin box id in hex  |
+-----------------+---------+---------------------+
| receiverAddress | String  | Horizen address     |
+-----------------+---------+---------------------+


**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/csw/generateCswProof\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"boxId\\\":\\\"string\\\",\\\"receiverAddress\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "state" : "ProofCreationFinished",
	    "description" : "CSW proof generation is finished"
	  }
	}

________


.. http:post:: /csw/cswInfo

*Returns information about csw proof for given box id*


**Parameters**

+-----------------+---------+---------------------+
| Name            | Type    | Description         |
+=================+=========+=====================+
| boxId           | String  | Coin box id in hex  |
+-----------------+---------+---------------------+



**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/csw/cwsInfo\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"boxId\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "cswInfo" : {
	      "cswType" : "UtxoCswData",
	      "amount" : 1000000000,
	      "scId" : "1b22519c38b6415a96a3cf73e1227bae06a2a2cf73a935685e19c9a1a9480da7",
	      "nullifier" : "e93952c5eab52b9648b5b711c11c134f05710a5e9de86c23608f690d31b7c300",
	      "proofInfo" : {
		"status" : "Generated",
		"scProof" : "0201a5711a4337d74df34e3a44278a2b77bee9b56a1277afc8451cbed2c0e5ad7a39000002dc3816c9c0dace2dd52ebcfe0e7da2bb4af6f9f7a27d6dd0e57f0b9cbe9f6e318021f25cdb09ea7e004c73c9a285ca36441bcde71174a278d99359ef7ddef6fa250000020e541c347b4641bd96b3baa408479e946666f62d28546ac5a3e2c2e371e5653d806a438f5cc8a5669861d4571cd34da22ceb1bd7177a009884ce3c3c4b37ce04340000015cdf657893a62ca75e5e83da568eaed84cd62d0d2257fdfcbeb8e7289b5eca2980000275ce4f810239b7aec55805731801cc14754c624d38907e35ac6bcdfc77bcae1300aee9f94b0f7bccd4016d47d7ebe75c607080cdaca3d1a0135e2b3cb22c2f6e0980000348eddb6955705605c599d1ca522f76098a9b42238b170a0e8f84609784cab10c808097bb3177a9cf7f94259f36e524951a84f49b26126cc8400c7bd60e7032021580a2cdc8d047062f40e407d516bf1ee1d4e0f9d52ac174d1294ab135168e1d761880000277d303c954d49165916d67502a4e8b62ff1737e133c9c33b12c9cfb3f80610328033a9b31e82a3c4ab8c28e244199710a13ce40beb1860b44466a567532a42d20e80000632b8a3a89d73cea667924dad0c1af412c5ae3a9bd85915acd0a2612616bbe7270046971cf9757a34a03737b32c3c84bb8d8acdc55e6dd2ce612c24d67469c1713300d30dc66f7fb5658445598715768c3c49dc5d95ab002d93137035e47b4113390d809a6085edc4bdd00809c106e63dc1c1a49d150faea210336538fc78e01bb8672100c56ea0ab3d162eaae92abac7f21cc1645ba3adde032c2db139a8553779b8680a002a98112ad8193aa9e8874b5682772585233025e79b6962ac515c44ac6f2c52338000f902b5e14b1be67b1020dad5bcd5cace37dc841a24d1cec9b61afa7191ea371dae6188c26ba0cc9deba28db82b5938ba6efd6ae69e6e5fb1f12e62ca4fba4f034b2c574694a6bd1159c94f25cd5df76c5dab3dfeb1c85feae7cba504cf39dd0820955d249b630df10307118c38e27c9e5f419d7136d43d9d44e1360733426f209b7127e80b414788af6d4e7d6ec0784396f261ffad08103bc6627e02897bb532d417a790ea53595d96199ad83b0e05dd4c9e7651d77a5662564d9556826dc608f7841d43e263c5aa769ed1b1dab98cde0edc7f16208016081d5ef9d7cbf5e10a89b5c05c68a4c8789ef655f94285abfb5b4b8e4ea3826dec05b566c0642e5a051df4a536c394440a0bee3682be5ff53674395b7af416f18d73e6ffcbd42ff535599a09e6757ce58692ed1180545e7919b8bb7aeb403a9bba5f19f62250f2640fb47cae8a049e8cb389d482de8a2d1f206ba26c44c4709a02c0adf0205d632e1200da4977335856f89f23771f01fa9aa34885a4b99c805543e76f033644df291386a95b16149ba145db5fcf9d7ca8adab1db7e646303e78480bf2983ca500cd305d7233800ae7f78fb2d1e98615a28f9fe35e5f3d53a9c9c4679d61b56f10b70bbb330f3d17e812cf1abc332538788d50db0681ea3a196f00cdcae20f1872a32ca9dfcde979c1b558f6f318d7a8f40e8f72939162aababe5fc0db624d332d6c269b9fdd6aff89c31009f36f025da3912b11d1115752d0bc9cde2d9b9ef549cd25b68f11f5fdda09d5070d1e1592d4598002ad18c1d0f43e0ceea524ba606dcf19b6436ce92645ac3b833a7437ff1f1af153ecbd21d973f7b57387c2a76e9d6706b6f3ce3d65a0356c2e924ad1bc4f2b6f99fcd8ae28881cf0094926d7364e54243c9893282c0bef0ae31dd91da551855a23bb6e7e490d2b5e233f28282084b011c2e0962f89c45f694031a3bafe2f7c08425a4620c9d5b4f2249b6ab0f495e40512c6d1d0582edc5a9937d313ab900d20f7c5e86a2d61c992409b4860ff57a69109805a2b4c90f8ec8bcd24df417123ad078a71b789b40439180228d9098bfbfc262b00b9f6c0588d3c4152098aca588af705ea1370491ee00500d89fed0db3c3e4ce1c801d699bc8bab9aa4c52ba562dda06b94aae1f24c7a2b1d947f50ec725fdae8e1000d582957d61e5f22b998b78c17dbf9734916c22ee8c698c9e6bddb942bb430d3d80142eb1c5246aa122293b3e194c8eaecc276a0b19cd212d3ec629dc1cebaf2a36806df240ba892b550943e9def88cd805223e0447b3aa9cf99eb1e2a4af298c733c00bf0e3a1237a8c49dfe1d229e228b6b7fcbc0777d1ef72022f7b15ec2fd9e300600894af057629ec1126db2308c7f7af5e2c4e848fd9d86759791938ee5f1f58937004504b178973d3ba6a472bdbccb61e01a1140148ae61a4688129fbaa772bf261100ab42cdec3621d611bbb6be002776cff103a1e81a6c9a7013d0f61f7e9221b3168020e1cc8f0baadc159d30a6ff4095a96518f03972906893793ee37f67e119d83e80148cdd10eb07bf04a8ba4f5048ec399a3d167ca84f5aaae3beb1a2ac9e32671f807c3f14afb718dd5ba218eed6e7861cfa6383e69817789e32a2646559245f3c29001aee4c85cc369d887f1eca700e9079156e1b739d56b5cd1eb2df712bffd3373400deb21c1095bff2b3d20afee8fdafe8a8e9bfc00721cfd893a5ae36c92e29363e00a4266daffbd9e944a0390d74fd5dddde2febc94ed03d823c58370372dfa3c700000a9f0ae80813a5b849660fcaec755d8c6e23ed9b8f3875c5f32f91721b7d131b00bf370a5d9f954fddf6dd5f25654f26c22cb749e200a97358168c48a1bd6bbb37803fbbc61d4dc22a035952b540a9571805ff60a9d5501bda5045d3bfd025e81e3700765f39fb4cef272784d18a8308bc19af31a504628cff6ef498292e6144c01b3000028633c714479b6ec9082c6d815bb871cc90167bb286104762c5e745d387390f005c911b540470420ff1f5c232bbe4d2d52ace0f7e5ff932a97fc0e4ce3dcf400b806460f73d5987183a5fbb81ec05ded8b14fc258d3e29071e5f28d6acf6516aa3780b0cddd4576cdc339c89b1c3fa337a8631c943e916a3dc9b7de9c8814a98a7c27800702df82bcc957ed67ceb25b65d22e40e16150f254aec3fc8b213118671ad81780e1362f6bd84e28f74048e58b907c2dbf960770314d8aeb9cc30b7c88e0e31e2a8051b3273820aaa95f7ec8421e1fa0cfc2ff0a74dd333e53da3710c9e59b00f7018095d2b414f1d72914c7d39cb25524a8dae4d3e2d53526c055bf2ed7d66d0e182c004a118c6beffb59d4054d79b95da0646fb0c0d50c139df320ebf23a147e4a962b800b600193c35eb6e25e5cc7ea0b8a24f4de39b64df566ac1ffa1843bc33e91d0b00bfc3e0e4783ddf45aeb8074ca0f505f9359b586664dc22a461bcde428b57773f8059330030353fe67a5a734b6a76679f707fd0cabf9a70079cf10d84cb00a8232900e2c1327b65bf98fd46ada4683d9787d01bbd303aa4f075154c7d65a5ad1a31010094794a1cd820f5ae044ce82741d7aed12d59630e95df4e195dfb3138a09273060032b7273687cf77ffa1d24b04f33725842addb92afc5433db0284475f1415460c80902575e8deb68703e84c24acc922c5194e30c80780b33bb9ffb6278b00a55d3380731768070bd4961ca6cd512589db5aa6b71b836b76d74e5d934830ec64b3d53801ae97ae79eeeab47aef53ee47a1debb3d9ccc556735476301912d40141b7529190001bac3f92047a9b8324c36debec018604eecfba2c56310f3621d88c9f340c38b25069c562ad2d0ba6833cb8177a837874d1c37f69dfd8782536faa504fcf56792604800f72395087364fe6365afb2a9e62ea04146481b8df1428740d74609b4624100600bb5d9653cf88e2be425c0c1445bf10b83f50271a0410b7ed34021c92616def2980a151e0b59dd9b6b2566130b39229ed27124d37f4029e7a1f57f107a4614e423b80e5a6cf225cd9c3bb21a15cd5c1a63324ebd43bc15d4cfee5e7c0707aee9dd2378075d6d089192a766ee5213b5bda55b18b85356333e902e240e03361bfd692d12a00",
		"receiverAddress" : "ztZd886uGxthiBhwSsQEmi72uDA6GNPeHua"
	      },
	      "activeCertData" : "5e17042bbba41298dc5c057176ce24d018552b6435d63d88a44740bbc767d833",
	      "ceasingCumScTxCommTree" : "bcb01e73e4256d436ed404f196de7d923c46a89d351f27056fe757a144a4601b"
	    }
	  }
	}

________


.. http:post:: /csw/cswBoxIds

*Returns list of available box ids for csw*


**No Parameters**


**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/csw/cswBoxIds\" -H \"accept: application/json\"

**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "cswBoxIds" : [ "e814e033de45a7d7770180ee0de8a5bef0ac83edc69b8665f496ef04e728a83c", "6dc9f828a5351c655e313307f118539abd496068d80d9e31d3dcf20fc48d11c7", "439a69030d1db3d1cd8c4d2a2badd02fdd9030066ba1d9df946ebbef95606d4b", "2630250338195552e9154ce051dc764c3bb5db24d1f3fffe3975b5105e07fd58", "3f244c0dc44bbe48262327f4dc88b913d232bc134957dd2c739d08dd1ae69a43", "28b2a31d7e46a0e7978e6e55ffbec9f270da8d2734d9dc87cdd6fe3eb910a727", "ee17566ffd58d10c6d4b99ee66baed18090a11f37b99ec288caedd3c19ba69c6", "6ee25cfe5fcec8f858b6c74a4fa37ff05d768caa1988aebfcbd945bc0696ef70", "c78775169ebb30b80862c2daa90bce7637d2b15c282a713ff33d376007b62a57" ]
	  }
	}

________


.. http:post:: /csw/nullifier

*Returns nullifier for given box id*


**Parameters**

+-----------------+---------+---------------------+
| Name            | Type    | Description         |
+=================+=========+=====================+
| boxId           | String  | Coin box id in hex  |
+-----------------+---------+---------------------+



**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/csw/nullifier\" -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{\\\"boxId\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

	{
	  "result" : {
	    "nullifier" : "e93952c5eab52b9648b5b711c11c134f05710a5e9de86c23608f690d31b7c300"
	  }
	}
_______

=====
**Sidechain Backup operations**
=====

.. http:post:: /backup/getSidechainBlockIdForBackup

*Returns the sidechain block id to use in the backup procedure.*

*The block id is calculated using the following formula:*

* *Genesis_MC_block_height + (current_epch - 2) * withdrawalEpochLength - 1*
*This endpoint returns an error in case the sidechain current epoch is less than 3.*

**No Parameters**

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/backup/getSidechainBlockIdForBackup\" -H \"accept: application/json\"


**Example response**:

   .. sourcecode:: http

      {
         "result":{
            "blockId":"7f25d35aadae65062033757e5049e44728128b7405ff739070e91d753b419094"
         }
      }

________

.. http:post:: /backup/getRestoredBoxes

*Returns the non-coin boxes restored by the restore procedure in a paginated way.*

**Parameters**

+---------------------+---------+-----------------------------------------------------------------------+
| Name                | Type    |            Description                                                |
+=====================+=========+=======================================================================+
| numberOfElements    |  int    | Number of boxes to return. Max = 100                                  |
+---------------------+---------+-----------------------------------------------------------------------+
| lastBoxId           |  string | Last box id received. It's optional and in case of empty or non value |
|                     |         | the endpoint starts to answer with the first box found.               |
+---------------------+---------+-----------------------------------------------------------------------+

**Example request**:

.. tabs::

   .. tab:: Bash

      curl -X POST \"http://127.0.0.1:9085/backup/getRestoredBoxes\" -H \"accept: application/json\" -d \"{\\\"numberOfElements\\\": 100, ,\\\"lastBoxId\\\":\\\"string\\\"}\"


**Example response**:

   .. sourcecode:: http

      {
         "result":{
            "boxes" : [ {
              "customUuid" : "71723462d695198c31e65136c9cc42c50b23c478f165c8957cb0509fd123cbb8",
              "customValue" : 866000000,
              "nonce" : 3509023985616518242,
              "id" : "84e2dd2f114a829422345fb0f27dfd836a803235f3e82418185aa68a0ba2f3b8",
              "typeName" : "CustomBox",
              "proposition" : {
                "publicKey" : "46630ae9f76aa3359a3007566aa83e661cdd0d024b484b85a6d9e0d2e4d51fb5"
              },
              "isCustom" : true
            }, {
              "customUuid" : "71723462d695198c31e65136c9cc42c50b23c478f165c8957cb0509fd123cbb8",
              "customValue" : 3561000000,
              "nonce" : 6626025734618418495,
              "id" : "8e5757b44d0199ee75ecd6a7cfb7c7deb8f675e14670f976abfe59f3521eae97",
              "typeName" : "CustomBox",
              "proposition" : {
                "publicKey" : "52ba271cc2d786c8197901679f1f7d47112c9dbee0dde082387a2295d7a8e074"
              },
              "isCustom" : true
            }, {
              "customUuid" : "71723462d695198c31e65136c9cc42c50b23c478f165c8957cb0509fd123cbb8",
              "customValue" : 4165000000,
              "nonce" : -7600613233944287562,
              "id" : "54f3d032494cbc4bccedc9a64d181b0e7e8ddd3d69f960db52b677995b6ecc2e",
              "typeName" : "CustomBox",
              "proposition" : {
                "publicKey" : "7377afd5a3d6d134a0748e7f0f3d9b11b67295a98384ee364bb464bafebf5dc9"
              },
              "isCustom" : true
            } ],
            "startingBoxId" : "e49866604b904546b7a83b04ff0fa131528de045bff8199af8cc47b9516cb512"
         }
      }

________

