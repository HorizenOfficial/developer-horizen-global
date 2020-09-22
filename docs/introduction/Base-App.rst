========
Base App
========

The Sidechain SDK provides developers with an out-of-the-box implementation of the Latus Consensus Protocol and the Cross-Chain Transfer Protocol.
Additionally, the SDK provides basic transactions, network layer, data storage and node configuration, as well as entry points for any custom extension.


Secret / Proof / Proposition
****************************

The SDK uses its own terminology for private key / public key / signed message:

* **Secret** -  Private key 
* **Proposition** - Public key, used in boxes as a locker
* **Proof** -  Signed message

The SDK ships with the following implementations for Secret / Proof / Proposition

  * `Curve 25519 <https://en.wikipedia.org/wiki/Curve25519>`_, currently used for Sidechain signing needs, e.g. to sign a transaction. This technology will not be used in the production release of the SDK, replaced by Schnorr signature (for higher efficiency in the SNARK-based proving system).
	- PrivateKey25519
	- PublicKey25519Proposition
	- Signature25519
  
  * Verifiable Random Function based on `ginger-lib <https://github.com/HorizenOfficial/ginger-lib>`_, used to assign and prove eligibility of block forgers.
  	- VrfSecretKey
	- VrfPublicKey 
	- VrfProof
  
  * Schnorr based on `ginger-lib <https://github.com/HorizenOfficial/ginger-lib>`_.
  	- SchnorrSecret 
	- SchnorrProposition
	- SchnorrProof


Boxes
*****

Data in a sidechain is meant to be represented as a Box. That data is kept “closed” by a Proposition, and can be opened (i.e. "spent") only with the Proposition’s Secret(s).
The Sidechain SDK offers two different Box types: Coin Box and non-Coin Box.

A Coin Box contains ZEN. A Non-Coin box does not contain ZEN, and represents a unique entity that can be transferred between different owners. Examples of a Coin box are RegularBox and ForgingBox. A Coin Box can add custom data to an object that represents coins, i.e. an object that holds an intrinsic, defined value. For example, a developer would extend a Coin Box to manage a time lock on a UTXO, e.g. to implement smart contract logic.

A Box represents an entity in the blockchain,  and all operations, such as create/open, are performed on it. Any Box contains a BoxData, which holds all the properties of that specific entity, such as value, proposition address, and any custom data.

Every Box has its own unique boxId (not be confused with box type id, which is used for serialization). That boxId is calculated for each Box by the following function in the SDK core:

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
	The id is used during transaction verification, so it is important to add the custom data into the customFieldsHash() function.

The following Coin-Box types are provided by the SDK:

  * **RegularBox** -- contains ZEN coins
  * **ForgerBox** -- contains ZEN coins that are staked for forging eligibility. A higher amount of ZEN in a ForgerBox offers higher chances of being selected to forge blocks (please check "Proof of Stake" consensus for more information on this).
  * **WithdrawalRequestBox** -- contain ZEN coins ready to be transferred back to mainchain. The actual transfer will be finalized by backward transfers that will be included in a certificate posted to the mainchain, after the end of the epoch.

An SDK developer can declare custom Boxes; please refer to the SDK extension section for details.

Transactions
************

There are two basic transactions: `MC2SCAggregatedTransaction
<https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/transaction/MC2SCAggregatedTransaction.java>`_ and `SidechainCoreTransaction
<https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/transaction/SidechainCoreTransaction.java>`_.

An MC2SCAggregatedTransaction is the implementation in a sidechain of Forward Transfers to that specific sidechain, i.e. mainchain transactions that send coins to addresses of that specific sidechain. When a Forger is going to produce a sidechain block, and a new mainchain block appears, the forger will mention that mainchain block as a reference that contains that sidechain related data. If a Forward Transfer exists in the mainchain block, it will be included into the MC2SCAggregatedTransaction and added as a part of the reference.

The SidechainCoreTransaction is the transaction which can send coins inside a sidechain, create forging stakes, or perform withdrawal requests (i.e. send coins back to the mainchain). The SidechainCoreTransaction can be extended to support custom logic operations. For example, if we think about a real-estate sidechain, we can tokenize some private property as a specific Box using SidechainCoreTransaction. Please refer to the SDK extensions for more details.

Serialization
*************

Because the SDK is based on Scorex, it implements the Scorex pattern for data serialization: any application custom object that needs to be serialized, like Box, BoxData, Secret, Proof, Transaction, must implement the  `Scorex BytesSerializable interface <https://github.com/ScorexFoundation/Scorex/blob/master/src/main/scala/scorex/core/serialization/BytesSerializable.scala>`_.

This interface defines two methods:

- ```byte[] bytes()``` - returns a bytearray representing the object
- ```Serializer serializer()``` - returns the class responsible to parse and write the object through Scorex Reader and Writer, which are wrappers on byte streams

The SDK provides basic serializer interfaces for its objects (for example `BoxDataSerializer <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/box/BoxSerializer.java>`_ for BoxData, `TransactionSerializer <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/transaction/TransactionSerializer.java>`_ for Transactions), ready to be extended when writing specific custom serializers.

We also need to instruct the dependency injection system on what appropriate serializer must be used for each object: this must be performed inside the AppModule configure() method, by adding key-value maps: the key is the specific type-id of each object (each object type must declare a unique type id), and the value is the serializer instance to be used for that object.
There are separate maps for each class of object (one for Boxes, one for BoxDatas, one for Transactions and so on). Please refer to the SDK extension section for more information.


SidechainNodeView
*****************

SidechainNodeView is the access point to the current node state; that includes NodeWallet, NodeHistory, NodeState, NodememoryPool, as well as application data. When defining custom API end points, you can extend a specific class and have access to SidechainNodeView.

Memory Pool
***********

The Memory Pool is the node's mechanism for storing transactions that haven't been included in a block yet. It acts as a sort of transactions' "waiting room".

Node wallet
***********

It contains the private keys known to the node.

State
*****

It contains information about the node's current state, i.e. the information that the node stores and updates to be able to operate. As an example, to validate transactions a node needs to know which are the outputs that haven't been spent yet.

History
*******

Provide access to history, i.e. to the previous blocks (on the active chain, and on forked ones).
 
Network layer
*************

The network layer is made of two distinct parts: communication between nodes and communication between the node and node users.
The interconnection among nodes is structured as a peer-to-peer network. Over the network, the SDK handles the handshake, blockchain synchronization, and transaction transmission.
The communication between a node and its users is available through http end points.

Physical storage
****************

The SDK introduces the unified physical storage interface, and this default implementation is based on the `IODB Library <https://github.com/input-output-hk/iodb>`_. Sidechain developers can decide to use the default solution or provide a custom implementation. For example, the developer could decide to use encrypted storage, a Key Value store, a relational database or even a cloud solution. When using a custom implementation, please make sure that the `Storage <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/test/java/com/horizen/storage/StorageTest.java>`_ test passes.

User-specific settings
**********************

A user can define custom configuration options, such as a specific path to the node data storage, wallet seed, node name and API server address/port, by modifying the configuration file. The file is written in `HOCON notation <https://github.com/lightbend/config/blob/master/HOCON.md/>`_, that is JSON made more human-editable. The configuration file consists of the SDK's required fields and the application's custom fields, if needed. Sidechain developers can use the `com.horizen.settings.SettingsReader <https://github.com/ZencashOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/settings/SettingsReader.java>`_ utility class to extract sidechain-specific data and the config object itself to get custom parts.

::

	class SettingsReader {
	    public SettingsReader (String userConfigPath, Optional<String> applicationConfigPath)

	    public SidechainSettings getSidechainSettings()

	    public Config getConfig()
	}

In the above class, userConfigPath is the path to the user defined configuration file. The optional parameter applicationConfigPath is a path to a configuration file that can be defined by the developer to set default values or values that are not meant to be modified by the user. The two getters (getSidechainSettings and getConfig) return the two merged configurations.


SidechainApp class
******************

The starting point of the SDK for each sidechain is the `SidechainApp class <https://github.com/ZencashOfficial/Sidechains-SDK/blob/master/sdk/src/main/scala/com/horizen/SidechainApp.scala>`_. Every sidechain application should create an instance of SidechainApp, passing all the required parameters, and then call its run() method to start the sidechain node:

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


The SidechainApp instance can be instantiated directly or through the `Guice DI library <https://github.com/google/guice>`_.


**Direct instantiation:**

All the required dependencies are passed inside the constructor:

::
	
	SidechainApp app = new SidechainApp(.....);
	app.run();
		
**Guice instantiation:**

You can define a Guice module which declares all the bindings, then use that module to create a guice injector, and call its getInstance() method to obtain the app instance:

::
	
	Injector injector = Guice.createInjector(new MyAppModule());
	SidechainApp app = injector.getInstance(SidechainApp.class);
	sidechainApp.run();

	
The Guice module class (MyAppModule in the example above) must extend the class com.google.inject.AbstractModule, and define the bindings inside its config() method. A binding definition could be done in the following ways:

::
    
    bind( <injected_classType> )
        .annotatedWith(Names.named( <identifier>))
        .toInstance(<custom class instance>);


injected_classType and identifier must belong to the binding types defined in the SDK. In the following list, you can find all the bindings that can be declared, with a brief description and example of binding declaration code:


-  SideChain settings
Must be an instance of com.horizen.SidechainSettings, defining the sidechain configuration parameters.

::

	bind(SidechainSettings.class)                                                                      
   		.annotatedWith(Names.named("SidechainSettings"))
   		.toInstance(..);  

- Custom box serializers
Serializers to be used for custom boxes, in the form ``HashMap<CustomboxId, BoxSerializer>``. 
Use ``new HashMap<>();`` if no custom serializers are required.         

::

	bind(new TypeLiteral<HashMap<Byte, BoxSerializer<Box<Proposition>>>>() {})
   		.annotatedWith(Names.named("CustomBoxSerializers"))
   		.toInstance(..); 

- Custom box data serializers
Serializers to be used for custom data boxes, in the form ``HashMap<CustomBoxDataId, NoncedBoxDataSerializer>``. 
Use ``new HashMap<>();`` if no custom serializers are required.         

::

	bind(new TypeLiteral<HashMap<Byte,NoncedBoxDataSerializer<NoncedBoxData<Proposition, NoncedBox<Proposition>>>>>(){}) 
    	.annotatedWith(Names.named("CustomBoxDataSerializers"))   
    	.toInstance(..);       

- Custom secrets serializers
Serializers to be used for custom secrets, in the form ``HashMap<SecretId, SecretSerializer>``. 
Use ``new HashMap<>();`` if no custom serializers are required.          

::

	bind(new TypeLiteral<HashMap<Byte, SecretSerializer<Secret>>>() {})                
		.annotatedWith(Names.named("CustomSecretSerializers"))    
		.toInstance(..);       

- Custom proposition serializers
Serializers to be used for custom Proof, in the form ``HashMap<CustomProofId, ProofSerializer>``. 
Use ``new HashMap<>();`` if no custom serializers are required          

::

	bind(new TypeLiteral<HashMap<Byte, ProofSerializer<Proof<Proposition>>>>() {})  
    	.annotatedWith(Names.named("CustomProofSerializers"))      
    	.toInstance(..);        

- Custom transaction serializers
Serializers to be used for custom transaction, in the form ``HashMap<CustomTransactionId, TransactionSerializer>``. 
Use ``new HashMap<>();`` if no custom serializers are required.

::

	bind(new TypeLiteral<HashMap<Byte, TransactionSerializer<BoxTransaction<Proposition, Box<Proposition>>>>>() {})
    	.annotatedWith(Names.named("CustomTransactionSerializers"))
    	.toInstance(..);

- Application Wallet
Class defining custom application wallet logic.
Must be an instance of a class implementing the com.horizen.wallet.ApplicationWallet interface.

::

	bind(ApplicationWallet.class)
    	.annotatedWith(Names.named("ApplicationWallet")
    	.toInstance(..);    

- Application state
Class defining custom application state logic.
Must be an instance of a class implementing the com.horizen.state.ApplicationState interface.

::

	bind(ApplicationState.class)
    	.annotatedWith(Names.named("ApplicationState"))
    	.toInstance(..);

- Secret storage
Class for defining Secret storage, i.e. a place where secret keys are stored.   
Must be an instance of a class implementing the com.horizen.storage.Storage interface.

::

	bind(Storage.class)                                                                                        
    	.annotatedWith(Names.named("SecretStorage"))
    	.toInstance(..);
       
-  WalletBoxStorage
Internal storage used for the wallet.
Must be an instance of a class implementing the com.horizen.storage.Storage interface.

::

	bind(Storage.class)                                                                                        
    	.annotatedWith(Names.named("WalletBoxStorage"))
    	.toInstance(..);     

-  WalletTransactionStorage
Internal storage used for transactions.
Must be an instance of a class implementing this interface: com.horizen.storage.Storage

bind(Storage.class)                                                                                        
    .annotatedWith(Names.named("WalletTransactionStorage"))
    .toInstance(..);      


-  WalletForgingBoxesInfoStorage
Internal storage used for forging boxes.
Must be an instance of a class implementing the com.horizen.storage.Storage interface.

::

	bind(Storage.class)                                                                                        
    	.annotatedWith(Names.named("WalletForgingBoxesInfoStorage"))
    	.toInstance(..);    

-  StateStorage
Internal storage used to save the current State, e.g. store information about boxes currently still closed, perform rollbacks in case of forks, etc.
Must be an instance of a class implementing the com.horizen.storage.Storage interface.

::

	bind(Storage.class)                                                                                        
    	.annotatedWith(Names.named("StateStorage"))
    	.toInstance(..);   

-  HistoryStorage
Internal storage used to store all the History data, including blocks of all forks.
Must be an instance of a class implementing the com.horizen.storage.Storage interface.

::

	bind(Storage.class)                                                                                        
    	.annotatedWith(Names.named("HistoryStorage"))
    	.toInstance(..);   

-  ConsensusStorage
Internal storage to save consensus data.
Must be an instance of a class implementing the com.horizen.storage.Storage interface.

::

	bind(Storage.class)                                                                                        
    	.annotatedWith(Names.named("ConsensusStorage"))
    	.toInstance(..);   

- Custom API extensions   
Used to add new custom endpoints to the http API.

::

	bind(new TypeLiteral<List<ApplicationApiGroup>> () {})
    	.annotatedWith(Names.named("CustomApiGroups"))
    	.toInstance(...);      

- Forbidden standard API     
Used to disable some of the standard http API endpoints.     
Each pair on the passed list represents a path to be disabled (the key is the basepath, the value the subpath).  

::

bind(new TypeLiteral<List<Pair<String, String>>> () {})
    .annotatedWith(Names.named("RejectedApiPaths"))
    .toInstance(...); 




SidechainApp arguments can be split into 4 groups:
	1. Settings
		* An instance of SidechainSettings can be retrieved by a custom application via SettingsReader, as seen above.
	2. Custom objects serializers
		* Developers will most likely want to add their custom data and business logic. For example, an application for tokenization of real-estate properties will want to create custom Box and BoxData types. These custom objects will have to be managed by the SDK, so that they can be sent through the network or stored on the disk. The SDK then need to know how to serialize them to bytes and how to deserialize them. This information is coded be the Sidechain developers, who must specify custom objects serializers and add them to the Serializer map. This will be better described in chapter 8.1, "Sidechain SDK extension, Data serialization".
	3. Application node extension of State and Wallet logic
		* As seen above, the state is a snapshot of all unspent boxes on the blockchain at a given moment. So when a new block arrives, the ApplicationState validates the block, e.g. to prevent the spending of non-existing boxes, or to discard transactions with inconsistencies in their input/output balance. Developers can extend this validation process by introducing additional logic in ApplicationState and ApplicationWallet.
	4. **API extension** - `link <../Node-communication.html>`_
	5. **Node communication** `link <../Sidechain-SDK-extension.html#custom-api-creation>`_
	
	
The SDK repository includes in its "examples" folder, the "SimpleApp" sidechain;  it's an application that does not introduce any custom logic: no custom boxes or transactions, no custom API, an empty ApplicationState and ApplicationWallet. "SimpleApp" shows the basic SDK functionalities, that are immediately available to the developer, and it's the fastest way to get started with our SDK.
