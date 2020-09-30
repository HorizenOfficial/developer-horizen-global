========================
Sidechains SDK extension
========================

To build a distributed, blockchain application, a developer typically needs to do more than just receive, transfer, and send coins back to the mainchain, as you can do with the basic components provided out-of-the-box by the SDK. Usually, there is the need is to to define some custom data, that the sidechain users can process and exchange according to some defined logic. In this chapter, we'll see what are the steps that should be taken to code a sidechain which implements custom data and logic. In the next one, we'll look in detail at a specific, customized sidechain example.

Custom box creation
###################

The first step of the development process of a distributed app implemented as a sidechain, is the representation of the needed data. In the SDK, application data are modeled as "Boxes". 

Every custom box should at least implement the ``com.horizen.box.NoncedBox`` interface. 
The methods defined in the interface are the following:

- ``long nonce()``
  The nonce guarantees that two boxes having the same properties and values, produce different and unique ids.
- ``long value()``
  If the box type is a Coin-Box,  this value is required and will contain the coin value of the Box. 
  In the case of a Non-Coin box, this value is still required, and could have a customized meaning chosen by the developer, or no meaning, i.e. not used. In the latter case, by convention is generally set to 1.
- ``Proposition proposition()``  
  should return the proposition that locks this box.
  The proposition that is used in the SDK examples is `com.horizen.proposition.PublicKey25519Proposition <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/proposition/PublicKey25519Proposition.java>`_; it's based on `Curve 25519 <https://en.wikipedia.org/wiki/Curve25519>`_, a fast and secure elliptic curve used by Horizen mainchain. A developer may want to define and use custom propositions.
- ``byte[] id()``
  should return a unique identifier of each box instance.
- ``byte[] bytes()``
  should return the byte representation of this box.
- ``BoxSerializer serializer()``
  should return the serializer of the box (see below).
- ``byte boxTypeId()``
  should return the unique identifier of the box type: each box type must have a unique identifier inside the whole sidechain application.

As a common design rule, you usually do not implement the NoncedBox interface directly, but extend instead the abstract class `com.horizen.box.AbstractNoncedBox <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/box/AbstractNoncedBox.java>`_, which already provides default implementations of 
some useful methods like ``id()``, ``equals()`` and ``hashCode()``.
This class requires the definition of another object: a class extending `com.horizen.box.AbstractNoncedBox <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/box/AbstractNoncedBox.java>`_, where you should put all the properties of the box, including the proposition. You can think of the AbstractNoncedBoxData as an inner container of all the fields of your box.
This data object must be passed in the constructor of AbstractNoncedBox, along with the nonce.
The important methods of AbstractNoncedBoxData that need to be implemented are:

- ``byte[] customFieldsHash()``
  Must return a hash of all custom data values, otherwise those data will not be "protected," i.e., some malicious actor can change custom data during transaction creation. 
- ``Box getBox(long nonce)`` 
  creates a new Box containing this BoxData for a given nonce.
- ``NoncedBoxDataSerializer serializer()``
  should return the serializer of this box data (see below)

BoxSerializer and NoncedBoxDataSerializer
#########################################

Each box must define its own serializer and return it from the ``serializer()`` method.
The serializer is responsible to convert the box into bytes, and parse it back later. It should implement the `com.horizen.box.BoxSerializer <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/box/BoxSerializer.java>`_ interface, which defines two methods:

- void ``serialize(Box box, scorex.util.serialization.Writer writer)``
  writes the box content into a Scorex writer  
- Box ``parse(scorex.util.serialization.Reader reader)``
  perform the opposite operation (reads a Scorex reader and re-create the Box)

Also any instance of AbstractNoncedBoxData need's to have its own serializer: if you declare a boxData, you should define one in a similar way. In this case the interface to be implemented is `com.horizen.box.data.NoncedBoxDataSerializer <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/box/data/NoncedBoxDataSerializer.java>`_

      
Specific actions for extension of Coin-box
###########################################

A Coin Box is a Box that has a value in ZEN. The creation process is the same just described, with only one extra action: a *Coin box class* needs to implement the ``CoinsBox<P extends PublicKey25519Proposition>`` interface, without the implementation of any additional function (i.e. it's a mixin interface).


Transaction extension
#####################

A transaction is the basic way to implement the application logic, by processing input Boxes that get unlocked and opened (or "spent"), and create new ones. To define a new custom transaction, you have to extend the `com.horizen.transaction.BoxTransaction <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/transaction/BoxTransaction.java>`_ class.
The most relevant methods of this class are detailed below:

- ``public List<BoxUnlocker<Proposition>> unlockers()``

  Defines the list of Boxes that are opened when the transaction is executed, together with the information (Proof) needed to open them.
  Each element of the returned list is an instance of BoxUnlocker, which is an interface with two methods:

  ::

    public interface BoxUnlocker<P extends Proposition>
    {
      byte[] closedBoxId();
      Proof<P> boxKey();
    }

  The two methods define the id of the closed box to be opened and the proof that unlocks the proposition for that box. When a box is unlocked and opened, it is spent or "burnt", i.e. it stops existing; as such, it will be removed from the wallet and the blockchain state. As a reminder, a value inside a box cannot be "updated": the the process requires to spend the box and create a new one with the updated values.

- ``public List<NoncedBox<Proposition>> newBoxes()``

  This function returns the list of new boxes which will be created by the current transaction. 
  As a good practice, you should use the ``Collections.unmodifiableList()`` method to wrap the returned list into a not updatable Collection:

  ::

    @Override
    public List<NoncedBox<Proposition>> newBoxes() {
      List<NoncedBox<Proposition>> newBoxes =  .....  //new boxes are created here  
      //....
      return Collections.unmodifiableList(newBoxes);
    }   

- ``public long fee()``
  Returns the fee to be paid to execute this transaction.

- ``public long timestamp()``
  Returns the timestamp of the transaction creation.
  As a good practice, timestamp should be created outside transaction, passed in the transaction's constructor, and returned here.

- ``public byte transactionTypeId()``
  Returns the type of this transaction. Each custom transaction must have its own unique type.

- ``public boolean transactionSemanticValidity()``
  Confirms if a transaction is semantically valid, e.g. check that fee > 0, timestamp > 0, etc.
  This function is not aware of the state of the sidechain, so it can't check, for instance, if the input is a valid Box.

Apart from the semantic check, the Sidechain will need to make also sure that all transactions are compliant with the application logic and syntax. Such checks need to be implemented in the ``validate()`` method of the ``custom ApplicationState`` class.

Transactions that process Coins
-------------------------------

| A key element of sidechains is the ability to trade ZEN. 
| ZEN are represented as Coin boxes, that can be spent and created. 
Transactions handling coin boxes will generally perform some basic, standard operations, such as: 

- select and collect a list of coin boxes in input which sum up to a value that is equal or higher than the amount to be spent plus fee

- create a coin box with the change

- check that the sum of the input boxes + fee is equal to the sum of the output coin boxes. 

Inside the Lambo-registry demo application, you can find an example of implementation of a transaction that handles regular coin boxes and implements the basic operations just mentioned: `io.horizen.lambo.car.transaction.AbstractRegularTransaction <https://github.com/HorizenOfficial/lambo-registry/blob/master/src/main/java/io/horizen/lambo/car/transaction/AbstractRegularTransaction.java>`_. 
Please note that, in a decentralized environment, transactions generally require the payment of a fee, so that their inclusion in a block can be rewarded and so incentivised. So, even if a transaction is not meant to process coin boxes, it still needs to handle coins to pay its fee.


Custom Proof / Proposition creation
###################################

A proposition is a locker for a box, and a proof is an unlocker for a box. How a box is locked and unlocked can be changed by the developer. For example, a custom box might require to be opened by two or more independent private keys. This kind of customization is achieved by defining custom Proposition and Proof.

* Creating custom Proposition
  You can create a custom proposition by implementing the ``ProofOfKnowledgeProposition<S extends Secret>`` interface. The generic parameter S represents the kind of private key used to unlock the proposition, e.g. you could use *PrivateKey25519*. 
  Let's see how you could declare a new kind of Proposition that accepts two different public keys, and that can be opened by just one of two corresponding private keys:

  public final class MultiProposition implements ProofOfKnowledgeProposition<PrivateKey25519> {
    
    // Specify json attribute name for the firstPublicKeyBytes field.
    @JsonProperty("firstPublicKey")
    private final byte[] firstPublicKeyBytes;

    // Specify json attribute name for the secondPublicKeyBytes field.
    @JsonProperty("secondPublicKey")
    private final byte[] secondPublicKeyBytes;

    public MultiProposition(byte[] firstPublicKeyBytes, byte[] secondPublicKeyBytes) {
        if(firstPublicKeyBytes.length != KEY_LENGTH)
            throw new IllegalArgumentException(String.format("Incorrect firstPublicKeyBytes length, %d expected, %d found", KEY_LENGTH, firstPublicKeyBytes.length));

        if(secondPublicKeyBytes.length != KEY_LENGTH)
            throw new IllegalArgumentException(String.format("Incorrect secondPublicKeyBytes length, %d expected, %d found", KEY_LENGTH, secondPublicKeyBytes.length));

        this.firstPublicKeyBytes = Arrays.copyOf(firstPublicKeyBytes, KEY_LENGTH);
        this.secondPublicKeyBytes = Arrays.copyOf(secondPublicKeyBytes, KEY_LENGTH);
    }

    public  byte[] getFirstPublicKeyBytes() { return firstPublicKeyBytes;}
    public  byte[] getScondPublicKeyBytes() { return secondPublicKeyBytes;}

    //other required methods for serialization omitted here:
    //byte[] bytes()
    //PropositionSerializer serializer();

  }

* Creating custom Proof interface 
  You can create a custom proof by implementing ``Proof<P extends Proposition>``, where *P* is the Proposition class that this Proof can open.
  You also need to implement the ``boolean isValid(P proposition, byte[] messageToVerify);`` function; it checks and states whether Proof is valid for a given Proposition or not. For example, the Proof to open the "two public keys" Proposition shown above could be coded this way:


  public class MultiSpendingProof extends Proof<MultiProposition> {

        protected final byte[] signatureBytes;

        public MultiSpendingProof(byte[] signatureBytes) {
            this.signatureBytes = Arrays.copyOf(signatureBytes, signatureBytes.length);
        }

        @Override
        public boolean isValid(MultiProposition proposition, byte[] message) {
            return (
              Ed25519.verify(signatureBytes, message, proposition.getFirstPublicKeyBytes()) || 
              Ed25519.verify(signatureBytes, message, proposition.getSecondPublicKeyBytes()
              );
        }

        //other required methods for serialization omitted here:
        //byte[] bytes();
        //ProofSerializer serializer();
        //byte proofTypeId();
  }


Application State
###########################

If we consider the representation of a blockchain in a node as a finite state machine, then the application state can be seen as the state of all the "registers" of the machine at the present moment. The present moment starts when the most recent block is received (or forged!) by the node, and ends when a new one is received/forged. A new block updates the state, so it needs to be checked for both semantic and contextual validity; if ok, the state needs to be updated according to what is in the block.
A customized blockchain will likely include custom data and transactions. The ApplicationState interface needs to be extended to code the rules that state validity of blocks and transactions, and the actions to be performed when a block modifies the state ("onApplyChanges"), and when it is removed ("onRollback", blocks can be reverted!):

ApplicationState:
::
  interface ApplicationState {
  boolean validate(SidechainStateReader stateReader, SidechainBlock block);

  boolean validate(SidechainStateReader stateReader, BoxTransaction<Proposition, Box<Proposition>> transaction);

  Try<ApplicationState> onApplyChanges(SidechainStateReader stateReader, byte[] version, List<Box<Proposition>> newBoxes, List<byte[]> boxIdsToRemove);

  Try<ApplicationState> onRollback(byte[] version);
  }

An example might help to understand the purpose of these methods. Let's assume, as we'll see in the next chapter, that our sidechain can represent a physical car as a token, that is coded as a "CarBox". Each CarBox token should represent a unique car, and that will mean having a unique VIN (Vehicle Identification Number): the sidechain developer will make ApplicationState store the list of all seen VINs, and reject transactions that create CarBox tokens with any preexisting VINs.

Then, the developer could implement the needed custom state checks in the following way:
    ::

      public boolean validate(SidechainStateReader stateReader, BoxTransaction<Proposition, Box<Proposition>> transaction) 

  * Custom checks on transactions should be performed here. If the function returns false, then the transaction is considered invalid. This method is called either before including a transaction inside the memory pool or before accepting a new block from the network.
    ::

      public boolean validate(SidechainStateReader stateReader, SidechainBlock block)  
    
  
  * Custom block validation should happen here. If the function returns false, then the block will not be accepted by the sidechain node. Note that each transaction contained in the block had been already validated by the previous method, so here you should include only block-related checks (e.g. check that two different transactions in the same block don't declare the same VIN car)
    ::

      public boolean validate(SidechainStateReader stateReader, BoxTransaction<Proposition, Box<Proposition>> transaction)

  * Any specific action to be performed after applying the block to the State should be defined here.

    ::

      public Try<ApplicationState> onApplyChanges(SidechainStateReader stateReader, byte[] version, List<Box<Proposition>> newBoxes, List<byte[]> boxIdsToRemove)
    
  
  * Any specific action after a rollback of the state (for example, in case of fork/reverted block) should be defined here.
    ::

      public Try<ApplicationState> onRollback(byte[] version)
    
  

Application Wallet 
##################

Every sidechain node has a local wallet associated to it, in a similar way as the mainchain Zend node wallet.
The wallet stores the user secret info and related balances. It is initialized with the genesis account key and the ZEN amount transferred by the sidechain creation transaction.
New private keys can be added by calling the http endpoint /wallet/createPrivateKey25519.
The local wallet data is updated when a new block is added to the sidechain, and when blocks are reverted. 

Developers can extend Wallet logic by defining a class that implements the interface `ApplicationWallet <https://github.com/ZencashOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/wallet/ApplicationWallet.java>`_
The interface methods are listed below:

::

  interface ApplicationWallet {
    void onAddSecret(Secret secret);
    void onRemoveSecret(Proposition proposition);
    void onChangeBoxes(byte[] version, List<Box<Proposition>> boxesToBeAdded, List<byte[]> boxIdsToRemove);
    void onRollback(byte[] version);
  }

As an example, the onChangeBoxes method gets called every time new blocks are added or removed from the chain; it can be used to implement for instance the update to a local storage of values that are modified by the opening and/or creation of specific box types.


Custom API creation 
###################

A user application can extend the default standard API (see chapter 6) and add custom API endpoints. For example if your application defines a custom transaction, you may want to add an endpoint that creates one.

To add custom API you have to create a class which extends the com.horizen.api.http.ApplicationApiGroup abstract class, and implements the following methods:

-  ``public String basePath()``
   returns the base path of this group of endpoints (the first part of the URL)

-  ``public List<Route> getRoutes()``
   returns a list of Route objects: each one is an instance of a `akka.Http Route object <https://doc.akka.io/docs/akka-http/current/routing-dsl/routes.html>`_ and defines a specific endpoint url and its logic.
   To simplify the developement, the ApplicationApiGroup abstract class provides a method (bindPostRequest) that builds a akka Route that responds to a specific http request with an (optional) json body as input. This method receives the following parameters:
   
   - the endpoint path

   - the function to process the request 

   - the class that represents the input data received by the  HTTP request call 
   
   Example:
    ::

      public List<Route> getRoutes() {
            List<Route> routes = new ArrayList<>();
            routes.add(bindPostRequest("createCar", this::createCar, CreateCarBoxRequest.class));
            routes.add(bindPostRequest("createCarSellOrder", this::createCarSellOrder, CreateCarSellOrderRequest.class));
            routes.add(bindPostRequest("acceptCarSellOrder", this::acceptCarSellOrder, SpendCarSellOrderRequest.class));
            routes.add(bindPostRequest("cancelCarSellOrder", this::cancelCarSellOrder, SpendCarSellOrderRequest.class));
            return routes;
        }

    Let's look in more details at the 3 parameters of the bindPostRequest method.

    - The endpoint path: 
      defines the endpoint path, that appended to the basePath will represent the http endpoint url.
       | For example, if your API group has a basepath = "carApi", and you define a route with endpoint path "createCar", the overall url will be: ``http://<node_host>:<api_port>/carAPi/createCar``

    - The function to process the request:
      Currently we support three types of function’s signature:
    
        * ApiResponse ``custom_function_name(Custom_HTTP_request_type)`` -- a function that by default does not have access to *SidechainNodeView*. 

        * ``ApiResponse custom_function_name(SidechainNodeView, Custom_HTTP_request_type)`` -- a function that offers by default access to SidechainNodeView
        
        * ``ApiResponse custom_function_name(SidechainNodeView)`` -- a function to process empty HTTP requests, i.e. endpoints that can be called without a JSON body in the request

        The format of the ApiResponse to be returned will be described later in this chapter.

    - The class that represents the body in the HTTP request
      
      | This needs to be a java bean, defining some private fields and  getter and setter methods for each field.
      | Each field in the json input will be mapped to the corresponding field by name-matching.
      | For example to handle the  following json body :
      ::
        
        {
        "number": "342",
        "someBytes": "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
        }

      you should code a request class like this one:
      ::

        public class MyCustomRequest {
          byte[] someBytes;
          int number;

          public byte[] getSomeBytes(){
            return someBytes;
          }

          public void setSomeBytes(String bytesInHex){
            someBytes = BytesUtils.fromHexString(bytesInHex);
          }

          public int getNumber(){
            return number;
          }

          public void setNumber(int number){
            this.number = number;
          }
        }

API response classes

The function that processes the request must return an object of type com.horizen.api.http.ApiResponse.
In most cases, we can have two different responses: either the operation is successful, or an error has occurred during the API request processing. 

For a successful response, you have to:
- define an object implementing the  SuccessResponse interface
- add the annotation  @JsonView(Views.Default.class) on top of the class, to allow the automatic conversion of the object into a json format.
- add some getters representing the values you want to return.

 For example, if a string should be returned, then the following response class can be defined:

  ::
  
    @JsonView(Views.Default.class)
    class CustomSuccessResponce implements SuccessResponse{
      private final String response;

      public CustomSuccessResponce (String response) {
        this.response = response;
      }

      public String getResponse() {
        return response;
      }
    }

In such a case, the API response will be represented in the following JSON format:

  ::
  
    {"result": {“response” : “response from CustomSuccessResponse object”}}


    
If an error is returned, then the response will implement the ErrorResponse interface. The ErrorResponse interface has the following default functions implemented:

```public String code()``` -- error code

```public String description()``` -- error description 

```public Option<Throwable> exception()``` -- Caught exception during API processing

As a result the following JSON will be returned in case of error:

  ::
  
    {
      "error": 
      {
      "code": "Defined error code",
      "description": "Defined error description",
      "Detail": “Exception stack trace”
      }
    }

  
Custom api group injection:

Finally, you have to instruct the SDK to use your ApiGroup.
This can be done with Guice, by binding the ""CustomApiGroups" field:
::

   bind(new TypeLiteral<List<ApplicationApiGroup>> () {})
         .annotatedWith(Names.named("CustomApiGroups"))
         .toInstance(mycustomApiGroups);
 
