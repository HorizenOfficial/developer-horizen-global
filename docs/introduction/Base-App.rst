========
Base App
========

Sidechain SDK provides to the developers an out of the box implementation of the Latus Consensus Protocol and the Crosschain Transfer Protocol.
Additionally to this, the SDK provides basic transactions, network layer, data storage and node configuration, as well as entry points for any custom extension.


Secret / Proof / Proposition
****************************

* **Sidechain SDK** uses its own terms for secret key / public key / signed message and provides various types of them.
* **Secret** -  Private key 
* **Proposition** - Public key, used in boxes as a locker
* **Proof** -  Signed message

* SDK provides the following implementations for Secret / Proof / Proposition

  * `Curve 25519 <https://en.wikipedia.org/wiki/Curve25519>`_
	- PrivateKey25519
	- PublicKey25519Proposition
	- Signature25519
  
  * VRF based on  `ginger-lib <https://github.com/HorizenOfficial/ginger-lib>`_ 
  	- VrfSecretKey
	- VrfPublicKey 
	- VrfProof
  
  * Schnorr based on `ginger-lib <https://github.com/HorizenOfficial/ginger-lib>`_ 
  	- SchnorrSecret 
	- SchnorrPropostion
	- SchnorrProof


Boxes
*****

Data in a sidechain is meant to be represented as a Box, that we can see as data kept “closed” by a Proposition, that can be open only with the Proposition’s Secret(s).
The Sidechain SDK offers two different Box types: Coin Box and non-Coin Box. 
A Non-Coin box represents a unique entity that can be transferred between different owners. A Coin box is a box that contains ZEN, examples of a Coin box are RegularBox and ForgingBox. A Coin Box can add custom data to an object that represents some coins, i.e., that it holds an intrinsic defined value. For example, a developer would extend a Coin Box to manage a time lock on a UTXO, e.g., to implement smart contract logic.
In particular, any box can be split into two parts: Box and BoxData (box data is included in the Box). 
The Box itself represents the entity in the blockchain, 
i.e., all operations such as create/open are performed on boxes. Box data contains information about the entity like value, proposition address, and any custom data.

Every Box has its unique boxId (not be confused with box type id, which is used for serialization). That box id is calculated for each Box by the following function in the SDK core:

::

	public final byte[] id() {
	   if(id == null) {
	       id = Blake2b256.hash(Bytes.concat(
		       this instanceof CoinsBox ? coinsBoxFlag : nonCoinsBoxFlag,
		       Longs.toByteArray(value()),
		       proposition().bytes(),
		       Longs.toByteArray(nonce()),
		       boxData.customFieldsHash()));
	   }
	   return id;
	}

.. note::
	The id is used during transaction verification, so it is important to add custom data  into customFieldsHash()  function.

The following Coin-Box types are provided by SDK:
  * **RegularBox** -- contains ZEN coins
  * **ForgerBox** -- contains ZEN coins are used for forging 
  * **WithdrawalRequestBox** -- contain ZEN coins are used to backward transfer, i.e. move coins back to the mainchain.

An SDK developer can declare custom Boxes, please refer to SDK extension section.

Transactions
************

There are two basic transactions: `MC2SCAggregatedTransaction
<https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/transaction/MC2SCAggregatedTransaction.java>`_ and `SidechainCoreTransaction
<https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/transaction/SidechainCoreTransaction.java>`_.
An MC2SCAggregatedTransaction is the implementation of Forward Transfer and can only be added as a part of the mainchain block reference data during synchronization with the mainchain.
When a Forger is going to produce a sidechain block, and a new mainchain block appears, the forger will recreate that mainchain block as a reference that will contain sidechain related data. If a Forward Transfer exists in the mainchain block, it will be included into the MC2SCAggregatedTransaction and added as a part of the reference.
The SidechainCoreTransaction is the transaction, which can be created by anyone to send coins inside a sidechain, create forging stakes or perform withdrawal requests (send coins back to the MC). 
The SidechainCoreTransaction can be extended to support custom logic operations. For example, if we think about real-estate sidechain, we can tokenize some private property as a specific Box using SidechainCoreTransaction. Please refer to SDK extensions for more details.

Serialization
*************

Because the SDK is based on Scorex we implement the Scorex way of data serialization. 
  * Any serialized data like Box/BoxData/Secret/Proof/Transaction implements Scorex `BytesSerializable <https://github.com/ScorexFoundation/Scorex/blob/master/src/main/scala/scorex/core/serialization/BytesSerializable.scala>`_ interface/trait.
  * `BytesSerializable <https://github.com/ScorexFoundation/Scorex/blob/master/src/main/scala/scorex/core/serialization/BytesSerializable.scala>`_ declare functions byte[] bytes() and Serializer serializer(). 
  * Serializer itself works with Reader/Writer, which are wrappers on byte stream. 
  * Scorex Reader and Writer also implements functionality like reading/parsing data of integer/long/string etc. 
  * Serialization and parsing itself implemented in data class by implementation ``byte[] bytes()`` (required by BytesSerializable interface) and implementation static function for parsing bytes ``public static Data parseBytes(byte[] bytes)``
  * Also, for correct parse purposes, special bytes such as a **unique id** of data type are put at the beginning of the byte stream (it is done automatically). Thus any serialized data shall provide a unique id. Specific serializers shall be set for those unique ids during the dependency injection setting as well as custom Serializer shall be put into Custom Serializers Map, which are defined at AppModule. Please refer to the SDK extension section for more information

SidechainNodeView
*****************

SidechainNodeView is a provider to current Node state including NodeWallet, NodeHistory, NodeState, NodememoryPool and application data as well. SidechainNodeView is accessible during custom API implementation.  

Memory Pool
***********

A mempool is a node's mechanism for storing information on unconfirmed transactions. It acts as a sort of waiting room for transactions that have not yet been included in a block

Node wallet
***********

Contains available private keys, required for generating correct proofs

State
*****

Contains information about current node state

History
*******

Provide access to history, i.e. blocks not only from active chain but from forks as well.
 
Network layer
*************

The network layer can be divided into communication between Nodes and communication between the node and user.
Node interconnection is organized as a peer-to-peer network. Over the network, the SDK handles the handshake, blockchain synchronization, and transaction transmission.

Physical storage
****************

Physical storage. The SDK introduces the unified physical storage interface, this default implementation is based on the `LevelDB library <https://github.com/google/leveldb>`_. Sidechain developers can decide to use the default solution or to provide the custom one. For example, the developer could decide to use encrypted storage, a Key Value store, a relational database or even a cloud solution. In case of your own implementation, please make sure that `Storage <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/test/java/com/horizen/storage/StorageTest.java>`_ test passes for your custom storage.

User specific settings
**********************

The user can define custom configuration options, such as a specific path to the node data storage, wallet seed, node name and API server address/port. To do this, he should write into the configuration file in a `HOCON notation
<https://github.com/lightbend/config/blob/master/HOCON.md/>`_. The configuration file consists of the SDK required fields and application custom fields 
if needed. Sidechain developers can use `com.horizen.settings.SettingsReader <https://github.com/ZencashOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/settings/SettingsReader.java>`_ utility class to extract Sidechain specific data and Config object itself to get custom parts.

::

	class SettingsReader {
	    public SettingsReader (String userConfigPath, Optional<String> applicationConfigPath)

	    public SidechainSettings getSidechainSettings()

	    public Config getConfig()
	}

Moreover, if a specific sidechain contains general application settings that should be controlled only by the developer, it is possible to define basic application 
config that can be passed as an argument to SettingsReader.


SidechainApp class
******************

The starting point of the SDK for each sidechain is the `SidechainApp class <https://github.com/ZencashOfficial/Sidechains-SDK/blob/master/sdk/src/main/scala/com/horizen/SidechainApp.scala>`_. Every sidechain application should create an instance of SidechainApp with passing all required parameters and then execute the sidechain node flow:

::

	class SidechainApp {
		public SidechainApp(
			// Settings:
			SidechainSettings sidechainSettings,

			// Custom objects serializers:
			HashMap<> customBoxSerializers,
			HashMap<> customBoxDataSerializers,
			HashMap<> customSecretSerializers,
			HashMap<> customTransactionSerializers,

			// Application Node logic extensions:
			ApplicationWallet applicationWallet,
			ApplicationState applicationState,

			// Physical storages:
			Storage secretStorage,
			Storage walletBoxStorage,
			Storage walletTransactionStorage,
			Storage stateStorage,
			Storage historyStorage,
			Storage walletForgingBoxesInfoStorage,
			Storage consensusStorage,

			// Custom API calls and Core API endpoints to disable:
			List<ApplicationApiGroup> customApiGroups,
			List<Pair<String, String>> rejectedApiPaths
		)

		public void run()
	}


The SidechainApp instance can be instantiated directly or through `Guice DI library <https://github.com/google/guice>`_.
Binding by Guice could be done in the following ways:

::
	
	bind(injected_classType)
		.annotatedWith(Names.named("Injected_parameter_name"))
		.toInstance(injected_variable_name);
		
**or**

::

	bind(new TypeLiteral<injected_classType>() {})
	       .annotatedWith(Names.named("Injected_parameter_name"))
	       .toInstance(injected_variable_name);
	       
In the following table, we describe used injections and their description. While injected injected_classType and "Injected_parameter_name" shall be used as it described in table, 
injected_variable_name could be differrent 	       

+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| bind(SidechainSettings.class)                                                                                          | File with sidechain settings,variable could be defined by SidechainSettings                                                                                                                                                                                                                   |
+========================================================================================================================+===============================================================================================================================================================================================================================================================================================+
|                                                                                                                        | ``sidechainSettings = this.settingsReader.getSidechainSettings();``                                                                                                                                                                                                                           |
|        .annotatedWith(Names.named("SidechainSettings"))                                                                |                                                                                                                                                                                                                                                                                               |
|          .toInstance(sidechainSettings);                                                                               |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(new TypeLiteral<HashMap<Byte, BoxSerializer<Box<Proposition>>>>() {})                                           | Serializer for custom boxes in the form ``HashMap<CustomboxId, BoxSerializer>``. Use just ``HashMap<Byte, BoxSerializer<Box<Proposition>>> customBoxSerializers = new HashMap<>();``                                                                                                          |
|        .annotatedWith(Names.named("CustomBoxSerializers"))                                                             | If no custom serializers are required                                                                                                                                                                                                                                                         |
|        .toInstance(customBoxSerializers);                                                                              |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(new TypeLiteral<HashMap<Byte,NoncedBoxDataSerializer<NoncedBoxData<Proposition, NoncedBox<Proposition>>>>>(){}) | Serializer for custom boxes in the form ``HashMap<CustomBoxDataId, NoncedBoxDataSerializer>``. Use ``HashMap<Byte, NoncedBoxDataSerializer<NoncedBoxData<Proposition, NoncedBox<Proposition>>>> customBoxDataSerializers = new HashMap<>();``                                                 |
|        .annotatedWith(Names.named("CustomBoxDataSerializers"))                                                         | If no custom serializers are required                                                                                                                                                                                                                                                         |
|        .toInstance(customBoxDataSerializers);                                                                          |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(new TypeLiteral<HashMap<Byte, SecretSerializer<Secret>>>() {})                                                  | Serializer for custom secrets in the form ``HashMap<SecretId, Secret>``. Use ``HashMap<Byte, SecretSerializer<Secret>> customSecretSerializers = new HashMap<>();``                                                                                                                           |
|        .annotatedWith(Names.named("CustomSecretSerializers"))                                                          | If no custom serializer is required                                                                                                                                                                                                                                                           |
|        .toInstance(customSecretSerializers);                                                                           |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(new TypeLiteral<HashMap<Byte, ProofSerializer<Proof<Proposition>>>>() {})                                       | Serializer for custom Proof in form ``HashMap<CustomProofId, ProofSerializer>``. Use ``HashMap<Byte, ProofSerializer<Proof<Proposition>>> customProofSerializers = new HashMap<>();``                                                                                                         |
|        .annotatedWith(Names.named("CustomProofSerializers"))                                                           | If no custom serializer is requried                                                                                                                                                                                                                                                           |
|        .toInstance(customProofSerializers);                                                                          |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(new TypeLiteral<HashMap<Byte, TransactionSerializer<BoxTransaction<Proposition, Box<Proposition>>>>>() {})      | Serializer for custom transaction as Hashmap where key is transaction Id in byte form and kye is transaction serializer for that type of transaction. Use ``HashMap<Byte, TransactionSerializer<BoxTransaction<Proposition,                                                                   |
|															 |  Box<Proposition>>>> customTransactionSerializers = new HashMap<>();``                                                                                                                                                                                                                        |                 
|        .annotatedWith(Names.named("CustomTransactionSerializers"))                                                     | If no custom transaction serializer is requried                                                                                                                                                                                                                                               |
|        .toInstance(customTransactionSerializers);``                                                                    |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(ApplicationWallet.class)                                                                                        | Class for defining ApplicationWallet                                                                                                                                                                                                                                                          |
|        .annotatedWith(Names.named("ApplicationWallet"))                                                                |                                                                                                                                                                                                                                                                                               |
|        .toInstance(defaultApplicationWallet);                                                                          |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``bind(ApplicationState.class)                                                                                         | Class for defining ApplicationState                                                                                                                                                                                                                                                           |
|        .annotatedWith(Names.named("ApplicationState"))                                                                 |                                                                                                                                                                                                                                                                                               |
|        .toInstance(defaultApplicationState);``                                                                         |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(Storage.class)                                                                                                  | Class for defining Secret storage, i.e. place where all secret keys are stored.                                                                                                                                                                                                               |
|        .annotatedWith(Names.named("SecretStorage"))                                                                    |                                                                                                                                                                                                                                                                                               |
|        .toInstance(IODBStorageUtil.getStorage(secretStore));                                                           |                                                                                                                                                                                                                                                                                               |
| bind(Storage.class)                                                                                                    |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|          .annotatedWith(Names.named("WalletBoxStorage"))                                                               | Internal storage for wallet                                                                                                                                                                                                                                                                   |
|        .toInstance(IODBStorageUtil.getStorage(walletBoxStore));                                                        |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(Storage.class)                                                                                                  | Internal storage for wallet                                                                                                                                                                                                                                                                   |
|        .annotatedWith(Names.named("WalletTransactionStorage"))                                                         |                                                                                                                                                                                                                                                                                               |
|        .toInstance(IODBStorageUtil.getStorage(walletTransactionStore));                                                |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(Storage.class)                                                                                                  | Internal storage for wallet                                                                                                                                                                                                                                                                   |
|        .annotatedWith(Names.named("WalletForgingBoxesInfoStorage"))                                                    |                                                                                                                                                                                                                                                                                               |
|        .toInstance(IODBStorageUtil.getStorage(walletForgingBoxesInfoStorage));                                         |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(Storage.class)                                                                                                  | Storage for saving current State state, i.e. store information about currently closed boxes, perform often rollbacks in case of forks, etc.                                                                                                                                                   |
|        .annotatedWith(Names.named("StateStorage"))                                                                     |                                                                                                                                                                                                                                                                                               |
|        .toInstance(IODBStorageUtil.getStorage(stateStore));                                                            |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(Storage.class)                                                                                                  | Storage for storing all information about Sidechain, including block storage for all forks.                                                                                                                                                                                                   |
|        .annotatedWith(Names.named("HistoryStorage"))                                                                   |                                                                                                                                                                                                                                                                                               |
|        .toInstance(IODBStorageUtil.getStorage(historyStore));                                                          |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(Storage.class)                                                                                                  | Internal History storage                                                                                                                                                                                                                                                                      |
|        .annotatedWith(Names.named("ConsensusStorage"))                                                                 |                                                                                                                                                                                                                                                                                               |
|        .toInstance(IODBStorageUtil.getStorage(consensusStore));                                                        |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(new TypeLiteral<List<ApplicationApiGroup>> () {})                                                               | Used for custom API extension                                                                                                                                                                                                                                                                 |
|        .annotatedWith(Names.named("CustomApiGroups"))                                                                  |                                                                                                                                                                                                                                                                                               |
|        .toInstance(customApiGroups);                                                                                   |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|   bind(new TypeLiteral<List<Pair<String, String>>> () {})                                                              | Used for defining forbidden standard API group                                                                                                                                                                                                                                                |
|        .annotatedWith(Names.named("RejectedApiPaths"))                                                                 |                                                                                                                                                                                                                                                                                               |
|        .toInstance(rejectedApiPaths);                                                                                  |                                                                                                                                                                                                                                                                                               |
+------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

We can split SidechainApp arguments into 4 groups:
	1. Settings
		* The instance of SidechainSettings is retrieved by custom application via SettingsReader, as was described above.
	2. Custom objects serializers
		* Developers will want to add their custom business logic. For example, tokenization of real-estate properties will
		  be required to create custom Box and BoxData types. These custom objects must be somehow managed by SDK to be sent through the network 
		  or stored to the disk. In both cases, SDK should know how to serialize a custom object to bytes and how to restore it.
		  To maintain this, sidechain developers should specify custom objects serializers and add them to 
		  custom...Serializer map following the specific rules (`Data Serialization Section </Sidechain-SDK-extension.html#data-serialization>`_)
	3. Application node extension of State and Wallet logic
		* As was said above, State is a snapshot of all closed boxes of the blockchain at some moment. So when the next block arrives, the ApplicationState validates the block to prevent the spending of non-existing boxes or transaction inputs and outputs coin balances inconsistency. Developers can extend State by introducing additional logic in ApplicationState and ApplicationWallet. See appropriate sections.
	4. **API extension** - `link </Node-communication.html>`_
	5. **Node communication** `link </Sidechain-SDK-extension.html#custom-api-creation>`_
	
	
Inside the SDK, we implemented a SimpleApp example designed to demonstrate the basic SDK functionalities. It is the fastest way to get started with our SDK.
SimpleApp has no custom logic: no custom boxes and transactions, no custom API, and an empty ApplicationState and ApplicationWallet.

The SimpleApp requires a single argument to start: the path to the user configuration file.
Under the hood, it has to parse its config file using SettingsReader, and then initialize and run SidechainApp.

	



















