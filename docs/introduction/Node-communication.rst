==================
Node communication
==================

Communication  between a user and a sidechain node is supported out of the box via HTTP POST requests API methods. Custom applications could extend them to add new, remove existing and and/or replace core behaviours.

The API configuration can be found in the sidechain configuration file.

For example see the restApi section of the following file for the SimpleApp:

.. code:: bash

   examples/simpleapp/src/main/resources/sc_settings.conf 
   

The available options are:

bindAddress -- “IP:port” address for sending HTTP request, e.g. "127.0.0.1:9085"

api-key-hash -- Authentication header must be a string that hashes to the field "api-key-hash" specified in each SC node conf file. Auth header could be empty If no api-key-hash is specified

timeout -- Timeout on API requests in seconds

..  note:: There are many ways to send API requests to a Sidechain node (in fact any REST client could be used):

* `Postman <https://www.postman.com/>`__ Collaboration Platform for API Development

* Embedded `swagger <https://swagger.io/>`_ client: Sending HTTP requests via a  swagger client which is already embedded in the Sidechain Node. So you could run in your browser “IP:port” as defined in your configuration file, and select any of the commands shown there. For example: 
  
  .. image:: /images/swagger.png
   :alt: Swagger


 
Default standard API
====================

`Base API <../reference/01-scnode-api-spec.html>`_ is organized in the following 5 groups:

 * `Block <../reference/01-scnode-api-spec.html#sidechain-block-operations>`_ -- Sidechain block operations like find best blockId, find blockId by block height etc. Also here you could find forging related commands like starting/stopping automatically forging, get information about forging like last epoch and slot index. Automatic forging gets current time to convert it into appropriate slot/epoch index, thus if by some reason a Sidechain node skip's the correct timeslot for whole consensus epoch when forging in automatic mode will always fail. Also, a Sidechain will be considered as deceased, as described before, i.e. communication between Sidechain and mainchain is no longer possible. However forging a block with manual set epoch/slot index is possible by API call /block/generate, it could be useful in case if Sidechain is run in isolated mode.


 * `Transaction <../reference/01-scnode-api-spec.html#sidechain-transaction-operations>`_ -- Sidechain transaction operations like find all transactions, create a transaction, without sending into memory pool, send transaction into memory pool, etc.


 * `Wallet <../reference/01-scnode-api-spec.html#sidechain-wallet-operations>`_ -- Sidechain wallet operations. Wallet operation could take optional parameter boxType for example in /wallet/balance API request. Box type could take as parameter RegularBox, ForgerBox etc., i.e. you could type here class name for required box type (in case of custom box type you oblige to use fully qualified class name ). If box type is not matter then just omit that parameter, i.e. in case of  /wallet/balance just use an empty body.
 
 
 * `Node <../reference/01-scnode-api-spec.html#sidechain-node-operations>`_ --Sidechain node operations like connect to the node, see all connections, etc.
 
 
 * `Mainchain <../reference/01-scnode-api-spec.html#sidechain-mainchain-operations>`_-- Sidechain mainchain operations like get the best MC header included in Sidechain.
