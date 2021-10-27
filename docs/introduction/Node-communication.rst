==================
Node communication
==================

Communication  between a user and a sidechain node is supported out of the box via HTTP POST requests API methods. Custom applications could extend them to add new, remove existing and/or replace core behaviours.

The API configuration can be found in the sidechain node's configuration file.

For example, review the restApi section of the following file for the SimpleApp:

.. code:: bash

   examples/simpleapp/src/main/resources/sc_settings.conf 

The available options are:

bindAddress -- "IP:port" address for sending HTTP request, e.g. "127.0.0.1:9085"

api-key-hash -- Authentication header must be a string that hashes to the field "api-key-hash" specified in each sidechain node's .conf file. The authentication header could be empty if no api-key-hash is specified

timeout -- Timeout in seconds on API requests 

..  note:: There are many ways to send API requests to a sidechain node (in fact any REST client could be used):

* `Postman <https://www.postman.com/>`__ Collaboration Platform for API Development

* Embedded `swagger <https://swagger.io/>`_ client: Sending HTTP requests via a  swagger client which is already embedded in the sidechain node. So, you could run  “IP:port”, as defined in your configuration file, in your browser and select any of the commands shown there. For example: 
  
  .. image:: /images/swagger.png
   :alt: Swagger


 Default standard API
====================

`Base API <../reference/01-scnode-api-spec.html>`_ is organized into the following 5 groups:

 * `Block <../reference/01-scnode-api-spec.html#sidechain-block-operations>`_ -- Sidechain block operations, e.g. find a block by its blockId, find a blockId by block height, etc. Also here you could find forging-related commands like the ones to automatically start/stop forging, get information about forging like last epoch and slot index. Automatic forging gets current time and converts it into appropriate slot/epoch index. Thus, if for some reason a sidechain node skips the correct timeslot for an entire consensus epoch when forging in automatic mode, it will always fail. A sidechain where this occurs will be considered deceased, and communication between the sidechain and mainchain is no longer possible. However, forging a block with a manually set epoch/slot index is possible by API call /block/generate, which could be useful if the sidechain is run in isolated mode.

 * `Transaction <../reference/01-scnode-api-spec.html#sidechain-transaction-operations>`_ -- Sidechain transaction operations like find all transactions, create a transaction without sending it into the memory pool, send transaction into memory pool, etc.

 * `Wallet <../reference/01-scnode-api-spec.html#sidechain-wallet-operations>`_ -- Sidechain wallet operations. Wallet operations could take boxType as an optional parameter, for example in /wallet/balance API request. Box type could take as parameter RegularBox, ForgerBox etc., i.e. you could type here class name for required box type (in case of custom box type you are required to use the fully-qualified class name ). If box type is not relevant, you can simply omit that parameter, i.e. in case of /wallet/balance just use an empty body.
  
 * `Node <../reference/01-scnode-api-spec.html#sidechain-node-operations>`_ --Sidechain node operations like connect to the node, see all connections, etc.
  
 * `Mainchain <../reference/01-scnode-api-spec.html#sidechain-mainchain-operations>`_-- Sidechain mainchain operations like get the best mainchain header included in sidechain.

 * `Ssubmitter`_ -- Certificate submitter operation like current status of certificate generation, managing operation of submitting and signing of certificate.
