========================
Sidechains SDK extension
========================


Data serialization
##################

Any data like **Box**/**BoxData**/**Secret**/**Proposition**/**Proof**/**Transaction** shall provide a way to  serialize itself to bytes and provide a way to parse it from bytes.
Serialization is performed via a special Serializer class. Any custom data needs to define its own Serializer and definition of parsing/serializing
and needs to declare those Serializers for the SDK. Thus SDK will be able to use proper Serializer for custom data. The steps to describe serialization/parsing for some
CustomData are the following:

* Implement `BytesSerializable <https://github.com/ScorexFoundation/Scorex/blob/master/src/main/scala/scorex/core/serialization/BytesSerializable.scala>`_ interface for *CustomData*, i.e.  ``functions byte[] bytes()`` and ``Serializer serializer()`` (which shall return CustomDataSerializer), also implement ``public static CustomData parseBytes(byte[] bytes)`` function for parsing from bytes
* Create ``CustomDataSerializer`` and implement ``ScorexSerializer interface``, i.e. functions  ``void serialize(CustomData customData, Writer writer)`` and ``CustomData parse(Reader reader)``;
* Provide a unique id for that data type by implementing a special function. List of data type and appropriate functions is next:

+-------------------------------+---------------------------+
| Data type / Base class        | Function to be overridden |
+===============================+===========================+
| interface Box                 | byte boxTypeId()          |
+-------------------------------+---------------------------+
| interface NoncedBoxData       | byte boxDataTypeId()      |
+-------------------------------+---------------------------+
| interface Proof               | byte proofTypeId()        |
+-------------------------------+---------------------------+
| interface Secret              | byte secretTypeId()       |
+-------------------------------+---------------------------+
| abstract class BoxTransaction | byte transactionTypeId()  |
+-------------------------------+---------------------------+


* In your AppModule class (i.e. class which extends  ```AbstractModule```, in SimpleApp it is ```SimpleAppModule```) define Custom Serializer map, for example for boxes it could be ```Map<Byte, BoxSerializer<Box<Proposition>>> customBoxSerializers = new HashMap<>();``` where key is data type id and value is CustomSerializer for those data type id.
  
* Add your custom serializer to the map, for example it could be something  ```like customBoxSerializers.put((byte)MY_CUSTOM_BOX_ID, (BoxSerializer) CustomBoxSerializer.getSerializer());```

* Bind map with custom serializers to your application in the app model class:
  ::

   TypeLiteral<HashMap<Byte, Common serializer type>() {})
         .annotatedWith(Names.named(Bound property name))
         .toInstance(Created map with custom serializers);
       
Where **Common serializer type** and **Bound property name** can have the following values 


+--------------------------------+----------------------------------------+
| Bound property name            | Common serializer type                 |
+================================+========================================+
| CustomBoxSerializers           | BoxSerializer<Box<Proposition>>>       |  
+--------------------------------+----------------------------------------+
| CustomBoxDataSerializers       | NoncedBoxDataSerializer<NoncedBoxData  |
|                                | <Proposition, NoncedBox<Proposition>>> |           
+--------------------------------+----------------------------------------+
| CustomSecretSerializers        | SecretSerializer<Secret>>              |           
+--------------------------------+----------------------------------------+
| CustomProofSerializers         | ProofSerializer<Proof<Proposition>>    |        
+--------------------------------+----------------------------------------+
| CustomTransactionSerializers   |  TransactionSerializer<BoxTransaction  |                                  
|                                |  <Proposition, Box<Proposition>>>      |
+--------------------------------+----------------------------------------+

Example: 

::

  bind(new TypeLiteral<HashMap<Byte, BoxSerializer<Box<Proposition>>>>() {})
       .annotatedWith(Names.named("CustomBoxSerializers"))
       .toInstance(customBoxSerializers);

Where

* **BoxSerializer<Box<Proposition>>>** -- common serializer type
* **"CustomBoxSerializers"** -- bound property name 
* **customBoxSerializers** -- created map with all defined custom serializers.

Custom box creation
###################

  a) SDK Box extension Overview

To build a real application, a developer will need to do more than receive, transfer, and send coins back. A distributed app, built on a sidechain, will typically have to define some custom data that the sidechain users will be able to exchange according to a defined logic. The creation of new Boxes requires the definition of four new classes. We will use the name Custom Box as a definition for some abstract custom Box:  


+--------------------------------------+------------------------------------------------------------------------------------+
| Class type                           | Class description                                                                  |
+======================================+====================================================================================+
| Custom Box Data class                | -- Contains all custom data definitions plus proposition for Box                   |
|                                      | -- Provides required information for serialization of Box Data                     |
|                                      | -- Defines the way to create a new Custom Box from current Custom Box Data         |
+--------------------------------------+------------------------------------------------------------------------------------+
| Custom Box Data Serializer Singleton | -- Defines how to parse bytes from Reader into Custom Box Data object              |
|                                      | -- Defines the way to put boxData object into Writer Parsing function used in a    |
|                                      | Serializer class can be put in that class as well. However, it can be defined      |
|                                      | somewhere else                                                                     |
+--------------------------------------+------------------------------------------------------------------------------------+
| Custom Box                           | Representation new entity in Sidechain, contains appropriate Custom Box Data class |
+--------------------------------------+------------------------------------------------------------------------------------+
| Custom Box Serializer Singleton      | -- Defines how to parse bytes from Reader into Box object                          |
|                                      | -- Defines the way how to put boxData object into Writer Parsing function used in a|
|                                      | Serializer class can be put in that class as well. However, it can be defined      |
|                                      | somewhere else                                                                     |
+--------------------------------------+------------------------------------------------------------------------------------+

Custom Box Data class creation
##############################

The SDK provides a base class for any Box Data class: 

::

  AbstractNoncedBoxData<P extends Proposition, B extends AbstractNoncedBox<P, BD, B>, BD extends AbstractNoncedBoxData<P, B, BD>>


**where**

``P extends Proposition`` -- Proposition type for the box, for common purposes ``PublicKey25519Proposition`` can be used as it used in regular boxes
  
``BD extends AbstractNoncedBoxData<P, B, BD>`` -- Definition of type for Box Data which contains all custom data for a new custom box

``B extends AbstractNoncedBox<P, BD, B>`` -- Definition of type for Box itself, required for description inside of new Custom Box data 


That base class provides the following data by default:

::

  proposition of type P long value

If the box type is a Coin-Box, then this value is required and will contain data such as coin value. In the case of a Non-Coin box it will be used in custom logic only. As a common practice for non-Coin box you can set it always equal to 1 

So the creation of new Custom Box Data takes place as follows:
::
  public class CustomBoxData extends AbstractNoncedBoxData<PublicKey25519Proposition, CustomBox, CustomBoxData>

The new custom box data class requires the following:

1. Custom data definition
  * Custom data itself
  * Hash of all added custom data shall be returned in "public byte[] customFieldsHash() "function, otherwise, custom data will not be "protected," i.e., some malicious actor can change custom data during transaction creation.  
    
2. Serialization definition
  * Serialization to bytes shall be provided by Custom Box Data by overriding and implementing the method ``public byte[] bytes()`` this function serializes the proposition, value and any added custom data.
  * Additionally definition of Custom Box Data id for serialization by overriding ``public byte boxDataTypeId()`` function, please check the serialization section for more information about using ids. 
  * Override ``public NoncedBoxDataSerializer serializer()`` function with proper **Custom Box Data serializer**. Parsing Custom Box Data from bytes can be defined in that class as well, please refer to the serialization section for more information about it

3. Custom Box creation
  * Any Box Data class shall provide the way how to create a new Box for a given nonce. For that purpose override the function 
    ::
     public CustomBox getBox(long nonce) 

Custom Box Data Serializer class creation
#########################################

The SDK provides a base class for Custom Box Data Serializer
``NoncedBoxDataSerializer<D extends NoncedBoxData>`` where **D** is type of serialized Custom Box Data

So creation of a Custom Box Data Serializer can be done in following way:
::
 public class CustomBoxDataSerializer implements NoncedBoxDataSerializer<CustomBoxData>

The new Custom Box Data Serializer requires the following:

  1. Definition of a function for writing Custom Box Data into the Scorex Writer by implementation of the following method.
     ::
      public void serialize(CustomBoxData boxData, Writer writer)

  2. Definition of a function for reading Custom Box Data from Scorex *Reader* by implementation of the function 
     ::
      public CustomBoxData parse(Reader reader)

  3. Class shall be converted to singleton. For example, this can be done as follows:

     ::
        
      private static final CustomBoxDataSerializer serializer = new CustomBoxDataSerializer();

      private CustomBoxDataSerializer() {
      super();
      }

      public static CustomBoxDataSerializer getSerializer() {
      return serializer;
      }
  
Custom Box class creation
#########################

The SDK provides a base class for creation of a Custom Box:
::
 public class CustomBox extends AbstractNoncedBox<PublicKey25519Proposition, CustomBoxData, CustomBoxBox>

As parameters for **AbstractNoncedBox** three template parameters shall be provided:
::
 P extends Proposition

- Proposition type for the box, for common purposes. ``PublicKey25519Proposition`` could be used as it is used in regular boxes
  ::
   BD extends AbstractNoncedBoxData<P, B, BD>
   
- Definition of type for Box Data which contains all custom data for a new custom box
  ::
   B extends AbstractNoncedBox<P, BD, B>

- Definition of type for the Box itself, required for description inside of new Custom Box data.
  
  
The Custom Box itself requires implementation of following functionality:

  1. Serialization definition

    * The box itself provides the way to be serialized into bytes, thus function ``public byte[] bytes()`` shall be implemented 
    * Method for creation of a new Car Box object from bytes ``public static CarBox parseBytes(byte[] bytes)``
    * Providing box type id by implementation of function  ``public byte boxTypeId()`` which return custom box type id. Finally, proper serializer for the Custom Box shall be returned by implementing function ``public BoxSerializer serializer()``

Custom Box Serializer Class
###########################

SDK provide base class for Custom Box Serializer BoxSerializer<B extends Box> where B is type of serialized Custom Box
So the creation of Custom Box Serializer can be done in the following way:
::
 public class CustomBoxSerializer implements NoncedBoxSerializer<CustomBox>

The new Custom Box Serializer requires the following:

  1. Definition of function for writing *Custom Box* into the *Scorex Writer* by implementation of the following.
     ::
      public void serialize(CustomBox box, Writer writer)

  2. Definition of function for reading *Custom Box* from *Scorex Reader* by implementation of the following method
     ::
      public CustomBox parse(Reader reader)

  3. Class shall be converted to singleton, for example it could be done in following way:
     ::
      private static final CustomBoxSerializer serializer = new CustomBoxSerializer();
      private CustomBoxSerializer() {
       super();
      }
      public static CustomBoxSerializer getSerializer() {
       return serializer;
      }
      
      
Specific actions for extension of Coin-box
###########################################

A Coin box is created and extended as a usual non-coin box, only one additional action is required: *Coin box class* shall also implement interface ``CoinsBox<P extends PublicKey25519Proposition>`` interface without any additional function implementations, i.e., it is a mixin interface.

Transaction extension
#####################

A transaction in the SDK is represented by the following class.
::
 public abstract class BoxTransaction<P extends Proposition, B extends Box<P>>
 
This class provides access to data such as which boxes will be created, unlockers for input boxes, fees, etc. the 
SDK developer could add a custom transaction check by implementing *custom ApplicationState* 

Any custom transaction shall implement three important functions:
``public boolean transactionSemanticValidity()`` -- this function defines if a transaction is semantically valid or not, i.e. verify stateless (without context) transaction correctness. Non-zero fee and positive timestamp are examples of such verification.

``public List<BoxUnlocker<Proposition>> unlockers()`` -- The SDK core does box opening verification by checking proofs against input box ids. However, information about closed boxes and proofs for that box shall be returned separately by each transaction. For such purposes, each transaction shall return a list of `unlockers <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/box/BoxUnlocker.java>`_ which are implemented by the following interface:
::
  public interface BoxUnlocker<P extends Proposition>
  {
    byte[] closedBoxId();
    Proof<P> boxKey();
  }

Where *closedBoxId* is the id of the closed box and *boxKey* is correct proof for that box.

``public List<NoncedBox<Proposition>> newBoxes()`` -- function returns list of new boxes which shall be created by current transaction. Be aware that due to some internal implementation of SDK that function must be implemented in the following way:
::
 @Override
 public List<NoncedBox<Proposition>> newBoxes() {
   if(newBoxes == null) {
   //new boxes are created here, newBoxes shall be updated by those new boxes
       }
   }
   return Collections.unmodifiableList(newBoxes);
 }

Custom Proof / Proposition creation
###################################

A proposition is a locker for a box, and Proof is an unlocker for a box. For some reason, the manner in which the box is locked/unlocked can be changed by the SDK developer (should this be sidechain developer?). For example, a special box can be opened by two or more independent private keys. For such reason, custom Proof/Proposition can be created.

* Creating custom Proposition
  For creating a custom Proposition  ``ProofOfKnowledgeProposition<S extends Secret>`` interface shall be implemented. Generic parameter is just a marker for the type of private key. For example, *PrivateKey25519* could be used. Inside the Proposition, we could use two different public keys to lock the box.

* Creating custom Proof interface ``Proof<P extends Proposition>`` shall be implemented where *P* is an appropriate Proposition class. ``Function boolean isValid(P proposition, byte[] messageToVerify);`` shall be implemented. That function defines whether Proof is valid for a given proposition and Proof or not. For example, in the case of Proposition with two different public keys, we could try to verify the message using public keys in Proposition one by one and return true if Proof had been created by one of the expected private keys.

ApplicationState and Wallet
###########################

ApplicationState:
::
  interface ApplicationState {
  boolean validate(SidechainStateReader stateReader, SidechainBlock block);

  boolean validate(SidechainStateReader stateReader, BoxTransaction<Proposition, Box<Proposition>> transaction);

  Try<ApplicationState> onApplyChanges(SidechainStateReader stateReader, byte[] version, List<Box<Proposition>> newBoxes, List<byte[]> boxIdsToRemove);

  Try<ApplicationState> onRollback(byte[] version);
  }

For example, the custom application may have the possibility to tokenize cars by the creation of Box entries - let us call them CarBox. Each CarBox token should represent a unique car by having a unique *VIN* (Vehicle Identification Number). To do this, the sidechain developer may define ApplicationState to store the list of actual VINs and reject transactions with CarBox tokens with VIN already existing.

The next custom state checks could be done here:

  * ``public boolean validate(SidechainStateReader stateReader, SidechainBlock block)`` -- any custom block validation could be done here. If the function returns false, then the block will not be accepted by the sidechain node.
  
  * ``public boolean validate(SidechainStateReader stateReader, BoxTransaction<Proposition, Box<Proposition>> transaction)`` -- any custom checks for the transaction could be done here. If the function returns false, then the transaction is assumed as invalid and, for example, will not be included in a memory pool. 

  * ``public Try<ApplicationState> onApplyChanges(SidechainStateReader stateReader, byte[] version, List<Box<Proposition>> newBoxes, List<byte[]> boxIdsToRemove)`` -- any specific action after block applying in State could be defined here.
  
  * ``public Try<ApplicationState> onRollback(byte[] version)`` -- any specific action after rollback of State (for example, in case of fork/invalid block) could be defined here.
  
Application Wallet 
##################

The Wallet by default keeps user secret info and related balances. The actual data is updated when a new block is applied to the chain or when some blocks are reverted. Developers can specify custom secret types that will be processed by the wallet. The developer may extend the logic using `ApplicationWallet <https://github.com/ZencashOfficial/Sidechains-SDK/blob/master/sdk/src/main/java/com/horizen/wallet/ApplicationWallet.java>`_
::
  interface ApplicationWallet {
    void onAddSecret(Secret secret);
    void onRemoveSecret(Proposition proposition);
    void onChangeBoxes(byte[] version, List<Box<Proposition>> boxesToUpdate, List<byte[]> boxIdsToRemove);
    void onRollback(byte[] version);
  }

For example, a developer needs to have some event-based data, like an auction slot that belongs to him, that will start in 10 blocks and expire in 100 blocks. So in ApplicationWallet, he will additionally keep this event-based info and will react when a new block is going to be applied (onChangeBoxes method execution) to activate or deactivate that slot in ApplicationWallet.

Custom API creation 
###################

  Steps to extend the API:
  
    1. Create a class (e.g. MyCustomApi) which extends the ApplicationApiGroup abstract class (you could create multiple classes, for example, to group functions by functionality).

    2. In a class where all dependencies are declared (e.g. SimpleAppModule in our Simple App example ), we need to create the following variable: ``List<ApplicationApiGroup> customApiGroups = new ArrayList<>();``

    3. Create a new instance of the class MyCustomApi, and then add it to *customApiGroups* 

At this point, MyCustomApi will be included in the API route, but we still need to declare the HTTP address. To do that:

  1. Override the basepath() method -
     ::   
      public String basePath() {
       return "myCustomAPI";
      }

Where "myCustomAPI" is part of the HTTP path for that API group 

  2.  Define HTTP request classes -- i.e. the JSON body in the HTTP request will be converted to that request class. For example, if as “request” we want to use byte array data with some integer value, we could define the following class:
  
  ::
  
    public static class MyCustomRequest {
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

Setters are defined to expect data from JSON. So, for the given MyCustomRequest we could use this JSON: 

    ::
    
      {
      "number": "342",
      "someBytes": "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"
      }

 And it will be converted to an instance of the *MyCustomRequest* class with vin = 342, and someBytes = bytes which are represented by hex string "a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac"


  3. Define a function to process the HTTP request: Currently we support three types of function’s signature:
  
      * ApiResponse ``custom_function_name(Custom_HTTP_request_type)`` -- a function that by default does not have access to *SidechainNodeView*. To have access to *SidechainNodeViewHolder*, this special call should be used: ``getFunctionsApplierOnSidechainNodeView().applyFunctionOnSidechainNodeView(Function<SidechainNodeView, T> function)``
      
      * ``ApiResponse custom_function_name(SidechainNodeView, Custom_HTTP_request_type)`` -- a function that offers by default access to SidechainNodeView
      
      * ``ApiResponse custom_function_name(SidechainNodeView)`` -- a function to process empty HTTP requests, i.e. JSON body shall be empty
      
Inside those functions, all required action could be defined, and with them also function response results. Responses could be based on *SuccessResponse* or *ErrorResponse* interfaces. The JSON response will be formatted by using the defined getters.  

  4. Add response classes

As a result of an API request, the result shall be sent back via HTTP response. In a typical case, we could have two different responses: operation is successful, or some error had appeared during processing the API request. The SDK provides following way to declare those API responses:
For a successful response, implement SuccessResponse interface with data to be returned. That data shall be accessible via getters. Also, that class shall have the next annotation required for marshaling and correct conversion to JSON: ``@JsonView(Views.Default.class)``. The developer can define here some other custom class for JSON marshaling. For example, if a string should be returned, then the following response class can be defined:

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
    
If an error shall be returned, then the response shall implement the ErrorResponse interface, which by default have these functions implemented:

```public String code()``` -- error code

```public String description()``` -- error description 

```public Option<Throwable> exception()``` -- Caught exception during API processing

As a result the following JSON will be returned in case of error:

  ::
  
    {
    "error": {
    "code": "Defined error code",
    "description": "Defined error description",
    "Detail": “Exception stack trace”
    }
    }
    
  5. Add defined route processing functions to route

  Override ``public List<Route> getRoutes() function`` by returning all defined routes, for example:

    ::
      
      List<Route> routes = new ArrayList<>();
      routes.add(bindPostRequest("getNSecrets", this::getNSecretsFunction, GetSecretRequest.class));
      routes.add(bindPostRequest("getNSecretOtherImplementation", this::getNSecretOtherImplementationFunction, GetSecretRequest.class));
      routes.add(bindPostRequest("getAllSecretByEmptyHttpBody", this::getAllSecretByEmptyHttpBodyFunction));
      return routes;
      
 Where 
 
 ``getNSecrets``, ``getNSecretOtherImplementation``, ``getAllSecretByEmptyHttpBody`` are defined API end points; ``this::getNSecretsFunction``, ``this::getNSecretOtherImplementationFunction``, ``getAllSecretByEmptyHttpBodyFunction`` binded functions;
``GetSecretRequest.class`` -- class for defining type of HTTP request



      
