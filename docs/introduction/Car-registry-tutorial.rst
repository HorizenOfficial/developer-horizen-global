====================================
Car Registry Tutorial
====================================

Car Registry App High-Level Overview
####################################

The Car Registry app is an example of a sidechain that implements specific custom data and logic. The purpose of the application is to provide a simplified service that keeps records of existing cars and their owners. It is simplified as sidechain users will be able to register cars by merely paying a transaction fee. In contrast, in a real-world scenario, the ability to create a car will be bound by the presentation of a certificate signed by the Department of Motor Vehicles or analogous authority, or some other consensus mechanism that guarantees that the car exists in the real world and it’s owned by a user with a given public key.
Accepting that cars will show up in the sidechain in our example, we want to build an application that has the following capabilitis:

    1. It can store information that identifies a specific car, such as vehicle identification number (VIN), model, production year, color.
    2. Allows car owners to be able to prove their ownership of the cars anonymously.
    3. Require the use of ZEN for all transactions. 



User stories:
#############

**Q: I want to add my car to the Car Registry App.**

*A:* Create a new Car Entry Box, which contains vehicle identification information (VIN, manufacturer, model, year, registration number), and a certificate. The proposition in this box is your public key in this sidechain. When you create a box, the sidechain should verify that the vehicle identification information and certificate are unique to this sidechain.

**Q: I want to create a sell order to sell my vehicle using the Car Registry App.**

*A:* You can create a new Car Sell Order Box that contains the price in coins and the vehicle information from the Car Entry Box. Cars can exist in the sidechain either as a Car Entry Box or as a Car Sell Order, but not both at the same time. This box must contains the buyer’s public key. When you create a sell order, the sidechain should verify that there is no other active sell order with this Car Entry Box. The current Sell Order consists of the same information that is contained in the Car Entry Box plus a description.

**Q: I want to see all available Sell Orders in the sidechain.**

*A:* Have additional storage, which is managed by ApplicationState and stores all Car Sell Orders. All orders can be retrieved using the new HTTP API call. 

**Q: I want to accept a sell order and buy the car.**

*A:* By accepting a sell order, you create a new transaction in the sidechain, which creates a new Car Entry Box with your public key as the proposition and transfers the correct value of coins from you to the seller.

**Q: I want to cancel my Car Sell Order.**

*A:* You will create a new transaction containing the Car Sell Order as input and a Car Entry Box with your public key and the proposition as the output.

**Q: I want to see the car entry boxes and car sell orders related to me (both created by me and proposed to me).**

*A:* Implement a new storage that will be managed by ApplicationState to store this information. Then implement a new HTTP API that contains a new method to get this information.

The starting point of the development process is the data representation. A car is an example of a Non-CoinBox. It represents an item, but not money. Another example of a Non-CoinBox is a car that is for sale. We need another box for a car for sale because a standard CarBox does not have additional data like sale price, seller proposition address, etc. For the money representation, a standard RegularBox is used (a RegularBox is a CoinBox), which the SDK provides. Besides new entities CarBox and CarSellOrder, we also need to define a way to create/destroy those new entities. For that purpose, these new transactions are defined: a transaction for creating a new car, a transaction that moves a CarBox to a CarSellOrder, a transaction that declares a car was purchased i.e., moving CarSellOrder to the new CarBox. All created transactions are not automatically put into the memory pool, so a raw transaction in hex representation is created with the /transaction/sendTransaction API request. In summary, we will add the next car boxes and transactions:

+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Entity name         | Entity description                                                                                                                                                                                                    | Entity fields                                                                                                                                                                                                       |
+=====================+=======================================================================================================================================================================================================================+=====================================================================================================================================================================================================================+
| CarBox              | Is a box that contains CarBox data, which could be stored and operated in the sidechain.                                                                                                                                  | boxData -- contains  car box data                                                                                                                                                                                   |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CarBoxData          | Description of the car by using defined properties                                                                                                                                                                    | vin -- vehicle identification number which contains unique identification number of the car                                                                                                                         |
|                     |                                                                                                                                                                                                                       | year -- vehicle year production                                                                                                                                                                                     |
|                     |                                                                                                                                                                                                                       | model -- car model                                                                                                                                                                                                  |
|                     |                                                                                                                                                                                                                       | color -- car color                                                                                                                                                                                                  |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CarSellOrderBox     | is a box which contains CarSellOrder data which could be stored and operated in the sidechain.| boxData -- contains CarSellOrder data|
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CarSellOrderBoxData | Is the description of a vehicle for sale. The box data contains a special type of proposition, a SellOrderProposition. This proposition allows us to spend the box in two different ways: by seller and by buyer| VIN -- vehicle identification number contains the unique identification number of the car|
|                     |                                                                                                                                                                                                                       | year -- vehicle year production                                                                                                                                                                                     |
|                     |                                                                                                                                                                                                                       | model -- car model                                                                                                                                                                                                  |
|                     |                                                                                                                                                                                                                       | color -- car color                                                                                                                                                                                                  |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CarSellOrderInfo    | Is information about the car being sold as well as proof of ownership of seller. Used in transaction processing.                                                                                                        | carBoxToOpen -- A CarBox to initiate a sale                                                                                                                                                                           |
|                     |                                                                                                                                                                                                                       | proof -- proof for open initial car box                                                                                                                                                                             |
|                     |                                                                                                                                                                                                                       | price -- selling price                                                                                                                                                                                              |
|                     |                                                                                                                                                                                                                       | buyerProposition -- current implementation expect to have the specific buyer which had been found off chain. Thus during creation of car sell order we already know buyer and shall put his future car proposition  |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CarBuyOrderInfo     |  Is data required for buying a car or recalling a CarSellOrder. Used in transaction processing.                                                                                                                    | carSellOrderBoxToOpen -- A CarSellOrder box to be opened.|
|                     |                                                                                                                                                                                                                       | proof -- specific proof of type SellOrderSpendingProof                                                                                                                                                              |
|                     |                                                                                                                                                                                                                       | for confirming buying of the car or recall car sell order                                                                                                                                                           |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Special proposition and proof:
##############################

    a) **SellOrderProposition** 
       The standard proposition only contains one public key, i.e., only one specific private key could open that proposition. 
       However, for a sell order, we need a way to open and spend the box in two different ways, so we need to specify an additional proposition/proof. 
       A SellOrderProposition contains two public keys: 
       ::
        ownerPublicKeyBytes
       
       and 
       ::
        buyerPublicKeyBytes 

       So the seller or buyer's private keys could open that proposition.  

    b) **SellOrderSpendingProof**
       The proof that allows us to open and spend
       ::
        CarSellOrderBox 
       
       A SellOrderProposition is presented in two different ways: opened by the buyer (meaning they buy the car), or opened by the seller (meaning the seller recalled the CarSellOrder). This proof creation requires two different API calls, but as a result in both cases, we will have the same type of transaction with the same proof type. 


Transactions:
#############

AbstractRegularTransaction 
**************************

Base custom transaction, all other custom transactions extend this base transaction. 

        *Input parameters are:*
        
            ``inputRegularBoxIds`` - list of regular boxes for payments like fee and car buying
            ``inputRegularBoxProofs`` - appropriate list of proofs for box opening for each regular box in ``inputRegularBoxIds``
            ``outputRegularBoxesData`` - list of output regular boxes, used as the change from paying a fee, as well as a new regular box for payment for the car.
            ``fee`` - transaction fee
            ``timestamp`` - transaction timestamp 

        *Output boxes:*
                
            Regular Boxes created by change or car payment 

CarDeclarationTransaction
*************************

Transaction for declaring a car in the Sidechain, this transaction extends ``AbstractRegularTransaction`` thus some base functionality already is implemented. 

        *Input parameters are:*
        
            ``inputRegularBoxIds`` -- list of regular boxes for payments like fee and car buying
            ``inputRegularBoxProofs`` -- appropriate list of proofs for box opening for each regular box in inputRegularBoxIds
            ``outputRegularBoxesData`` -- list of output regular boxes, used as change from paying a fee, as well as a new regular box for car payment.
            ``fee`` -- transaction fee
            ``timestamp`` -- transaction timestamp
            ``outputCarBoxData`` -- box data which contains information about a new car.

        *Output boxes:*
        
            New CarBox with new declared car

SellCarTransaction 
******************

Transaction to initiate the selling process of the car. 

         *Input parameters are:*
         
            ``inputRegularBoxIds`` - list of regular boxes for payments like fee and car buying
            ``inputRegularBoxProofs`` - appropriate list of proofs for box opening for each regular box in inputRegularBoxIds
            ``outputRegularBoxesData`` - list of output regular boxes, used as change from paying fee, as well as new regular box for payment for car.
            ``fee`` -- transaction fee
            ``timestamp`` - transaction timestamp
            ``carSellOrderInfo`` - information about car selling, including such information as car description and specific proposition ``SellOrderProposition``.

        *Output boxes:*
         
            A CarSellOrderBox represents a car to be sold. This box could be opened by the car owner to recall the order, or by a specified buyer if a someone buys the car.    

BuyCarTransaction 
*****************

This transaction allows us to buy a car or recall a car sell order. 

        *Input parameters are:*
        
            ``inputRegularBoxIds`` - list of regular boxes for payments like fee and purchasing the car 
            ``inputRegularBoxProofs`` - appropriate list of proofs for box opening for each regular box in inputRegularBoxIds
            ``outputRegularBoxesData`` - list of output regular boxes, used as change from paying fee, as well as a new regular box for payment for the car.
            ``fee`` - transaction fee
            ``timestamp`` - transaction timestamp
            ``carBuyOrderInfo`` - information for buy car or recall car sell order.      
            
        *Output boxes:*
        
            Two outputs are possible. In the case of buying a car, a new CarBox with a new owner, a new RegularBox with a value declared in CarBuyOrderInfo for the car's former owner. 

Car registry implementation
###########################

First of all, we need to define new boxes. 
As described before, a CarBox is a Non-CoinBox, and similarly we need the CarBoxData class to describe custom data. So we need to define the CarBox and the CarBoxData as separate classes to allow proper serialization/deserialization.  

Implementation of CarBoxData:
*****************************

CarBoxData is implemented according to the description from the Custom Box Data Creation section as a public class CarBoxData extends AbstractNoncedBoxData<PublicKey25519Proposition, CarBox, CarBoxData> with custom data as:
::    
 private final BigInteger vin;
 private final int year;
 private final String model;
 private final String color;
        
A few comments about implementation:

    1. @JsonView(Views.Default.class) is used during class declaration. That annotation allows SDK core to do proper JSON serialization.
    2. Serialization is implemented in  public byte[] bytes() function as well as parsing implemented in public static CarBoxData parseBytes(byte[] bytes) function. SDK developer, as described before, shall include proposition and value into serialization/deserialization. The order doesn't matter. 
    3. CarBoxData shall have a value parameter as a Scorex limitation, but in our business logic, CarBoxData does not use that data at all because each car is unique and doesn't have any inherent value. Thus value is hidden, i.e., value is not present in the constructor parameter and just set by default to "1" in the class constructor.
    4. ``public byte[] customFieldsHash()`` shall be implemented because we introduce some new custom data.
    
Implementation of CarBoxDataSerializer:
***************************************

``CarBoxDataSerializer`` is implemented according to the description from ``Custom Box Data Serializer Creation`` section as ``public class CarBoxDataSerializer implements NoncedBoxDataSerializer<CarBoxData>``. 

Implementation of CarBox:
*************************

 A ``CarBox`` is implemented according to the description from ``Custom Box Class creation`` section as ``public class CarBox extends AbstractNoncedBox<PublicKey25519Proposition, CarBoxData, CarBox>``

A few comments about implementation:

    1. As a serialization part SDK developer shall include ``long nonce`` as a part of serialization, thus serialization is implemented in the following way:
       ::
        public byte[] bytes()
        {
            return Bytes.concat(
                Longs.toByteArray(nonce),
                CarBoxDataSerializer.getSerializer().toBytes(boxData)
            );
        }

    2. A ``CarBox`` defines its own unique id by implementing the function ``public byte boxTypeId()``. A similar function is defined in ``CarBoxData`` but it is a different id despite the value returned in ``CarBox`` and ``CarBoxData`` being the same.

Implementation of CarBoxSerializer:
***********************************

A CarBoxSerializer is implemented according to the description from the (`“Custom Box Data Serializer Creation section” <Sidechain-SDK-extension.html#custom-box-data-serializer-class-creation>`_) as 
::
 public class CarBoxSerializer implements BoxSerializer<CarBox> 

Implementation of SellOrderProposition
**************************************

A SellOrderProposition is implemented as 
::
 public final class SellOrderProposition implements ProofOfKnowledgeProposition<PrivateKey25519>

A point to note is that the proposition contains two public keys, thus that proposition could be opened by two different private keys.

Implementation of SellOrderPropositionSerializer
************************************************
A SellOrderPropositionSerializer is implemented as 
::
 public final class SellOrderPropositionSerializer implements PropositionSerializer<SellOrderProposition>

Implementation of SellOrderSpendingProof  
****************************************
A SellOrderSpendingProof is implemented as  
::
 extends AbstractSignature25519<PrivateKey25519, SellOrderProposition>

Implementation Comments: Information about the proof type is defined by the result of the boolean method isSeller(). For example an implementation of the method isValid uses the flag:
::
 public boolean isValid(SellOrderProposition proposition, byte[] message) {
  if(isSeller) {
   // Car seller wants to discard selling.
   return Ed25519.verify(signatureBytes, message, proposition.getOwnerPublicKeyBytes());
  } else {
   // Specific buyer wants to buy the car.
   return Ed25519.verify(signatureBytes, message, proposition.getBuyerPublicKeyBytes());
  }
 }

Implementation of CarSellOrderBoxData
*************************************

A CarSellOrderBoxData is implemented according to the description from the (`“Custom Box Data class creation section” <Sidechain-SDK-extension.html#custom-box-data-class-creation>`_) as 
::
 public class CarSellOrderData extends AbstractNoncedBoxData<SellOrderProposition, CarSellOrderBox, CarSellOrderBoxData> 
 
with custom data as:
::
 private final String vin;
 private final int year;
 private final String model;
 private final String color;

A few comments about implementation:
Proposition and value shall be included in serialization as is done in CarBoxData 
Id of that box data could be different than in CarBoxData
CarSellOrderBoxData uses custom proposition type, thus *proposition* field has *SellOrderProposition* type 

Implementation of CarSellOrderBoxDataSerializer
***********************************************

A CarSellOrderDataSerializer is implemented according to the description from the (`“Custom Box Data Serializer creation section” <Sidechain-SDK-extension.html#custom-box-data-serializer-class-creation>`_) as
::
 public class CarSellOrderBoxDataSerializer implements NoncedBoxDataSerializer<CarSellOrderData>

Implementation of CarSellOrderBox
*********************************

A CarSellorder is implemented according to the description from the (`“Custom Box Class creation section” <Sidechain-SDK-extension.html#custom-box-class-creation>`_) as
::
 public final class CarSellOrderBox extends AbstractNoncedBox<SellOrderProposition, CarSellOrderBoxData, CarSellOrderBox>

AbstractRegularTransaction
**************************

*AbstractRegularTransaction* is implemented as 
::
 public abstract class AbstractRegularTransaction extends SidechainTransaction<Proposition, NoncedBox<Proposition>>

Basic functionality is implemented for building required unlockers for input Regular boxes and returning a list of output Regular boxes according to input parameter *outputRegularBoxesData*. Also, basic transaction semantic validity is checked here. 

CarDeclarationTransaction 
*************************

*CarDeclarationTransaction* extends previously declared *AbstractRegularTransaction* in the following way: ``public final class CarDeclarationTransaction extends AbstractRegularTransaction``
newBoxes() -- a new box for a new car must be added as well. This function will be overridden by adding a new CarBox to the RegularBoxes.  

SellCarTransaction 
******************

A *SellCarTransaction* extends previously declared AbstractRegularTransaction in following way: ``public final class SellCarTransaction extends AbstractRegularTransaction``
Similar to the *CarDeclarationTransaction* function, the *newBoxes()* function will also return a new specific box. In our case that new box is a *CarSellOrderBox*.Since we have a specific box to open (CarBox), we also need to add an unlocker for CarBox. The unlocker for that CarBox had been added to the ``public List<BoxUnlocker<Proposition>> unlockers()``


BuyCarTransaction
*****************

A few comments about implementation: 
During the creation of the unlockers in function *unlockers()*, we need to create a specific unlocker for opening a CarSellOrder. Another *newBoxes()* function has a bit-specific implementation. That function forces the creation of a new RegularBox as payment for a car (if the vehicle has sold). A NewCarBox will be created according to information provided in  ``carBuyOrderInfo``. 


Extend API: 
***********

* Create a new class CarAPI which extends ApplicationAPIGroup class. Add this new class to route it in SimpleAppModule, as described in the Custom API manual. In our case it is done in ``CarRegistryAppModule`` by 

    * Creating ``customApiGroups`` as a list of custom API Groups:
    * ``List<ApplicationApiGroup> customApiGroups = new ArrayList<>()````;

    * Adding created ``CarApi`` into ``customApiGroups: customApiGroups.add(new CarApi())``;

    * Binding that custom api group via dependency injection:
      ::
       bind(new TypeLiteral<List<ApplicationApiGroup>> () {})
               .annotatedWith(Names.named("CustomApiGroups"))
               .toInstance(customApiGroups);


* Define Car creation transaction.

    * Defining request class/JSON request body
      As input for the transaction we expected: 
      Regular box id  as input for paying fee; 
      Fee value; 
      Proposition address which will be recognized as a Car Proposition; 
      Vehicle identification number of car. So next request class shall be created:
      :: 
       public class CreateCarBoxRequest {
       public String vin;
       public int year;
       public String model;
       public String color;
       public String proposition; // hex representation of public key proposition
       public long fee;

       // Setters to let Akka Jackson JSON library to automatically deserialize the request body.
            public void setVin(String vin) {
                this.vin = vin;
            }

            public void setYear(int year) {
                this.year = year;
            }

            public void setModel(String model) {
                this.model = model;
            }

            public void setColor(String color) {
                this.color = color;
            }

            public void setProposition(String proposition) {
                this.proposition = proposition;
            }

            public void setFee(long fee) {
                this.fee = fee;
            }
        }


Request class shall have appropriate setters and getters for all class members. Class members' names define a structure for related JSON structure according to `Jackson library <https://github.com/FasterXML/jackson-databind/>`_, so next JSON structure is expected to be set: 
::
 {
    "vin":"30124",
    “year”:1984,
    “model”: “Lamborghini”
    “color”:”deep black”
    "carProposition":"a5b10622d70f094b7276e04608d97c7c699c8700164f78e16fe5e8082f4bb2ac",
    "fee": 1,
    "boxId": "d59f80b39d24716b4c9a54cfed4bff8e6f76597a7b11761d0d8b7b27ddf8bd3c"
 }
        
A few notes: setter’s input parameter could have a different type than set class member. It allows us to make all necessary conversion in setters.


Define the response for the car creation transaction, the result of transaction shall be defined by implementing the SuccessResponse interface with the class members. Class members will be returned as an API response. All members will have properly set getters and the response class will have proper annotation ``@JsonView(Views.Default.class)`` thus the Jackson library is able to correctly represent the response class in JSON format. In our case, we expect to return transaction bytes. The response class is next:

  ::
    @JsonView(Views.Default.class)
    class TxResponse implements SuccessResponse {
    public String transactionBytes;
        public TxResponse(String transactionBytes) {
            this.transactionBytes = transactionBytes;
        }
    }

* Define Car creation transaction itself
  ::
   private ApiResponse createCar(SidechainNodeView view, CreateCarBoxRequest ent)

As a first parameter we pass reference to SidechainNodeView, second reference is previously defined class on step 1 for representation of JSON request. 

* Define the request for the CarSellOrder transaction with a CreateCarSellOrderRequest as we did for the car creation transaction request.

    * Define request class for Car sell order transaction CreateCarSellOrderRequest as it was done for Car creation transaction request:
      ::
       public class CreateCarSellOrderRequest {
        public String carBoxId; // hex representation of box id
        public String buyerProposition; // hex representation of public key proposition
        public long sellPrice;
        public long fee;

        // Setters to let Akka Jackson JSON library to automatically deserialize the request body.

        public void setCarBoxId(String carBoxId) {
            this.carBoxId = carBoxId;
        }

        public void setBuyerProposition(String buyerProposition) {
            this.buyerProposition = buyerProposition;
        }

        public void setSellPrice(long sellPrice) {
            this.sellPrice = sellPrice;
        }

        public void setFee(int fee) {
            this.fee = fee;
        }
       }

* Define Car Sell order transaction itself -- ``private ApiResponse createCarSellOrder(SidechainNodeView view, CreateCarSellOrderRequest ent)`` Required actions are similar as it was done to Create Car transaction. The main idea is a moving Car Box into CarSellOrderBox.

* Define Car sell order response --  As a result of Car sell order we could still use TxResponse
 
* Create AcceptCarSellorder transaction
    * Specify request as  
      ::
       public class SpendCarSellOrderRequest {
        public String carSellOrderId; // hex representation of box id
        public long fee;
        // Setters to let the Akka Jackson JSON library automatically deserialize the request body.
        public void setCarSellOrderId(String carSellOrderId) {
        this.carSellOrderId = carSellOrderId;
        }

        public void setFee(long fee) {
        this.fee = fee;
        }
       }
            
    * Specify acceptCarSellOrder transaction itself
    * As a result we still could use TxResponse class
    * Important part is creation proof for BuyCarTransaction, because we accept car buying then we shall form proof with defining that we buy car:
        ::
            
            SellOrderSpendingProof buyerProof = new SellOrderSpendingProof(
            buyerSecretOption.get().sign(messageToSign).bytes(),
            isSeller
            );
            
    Where *isSeller* is false.

* Create cancelCarSellOrder transaction
    * Specify cancel request as 
      ::
        public class SpendCarSellOrderRequest {
            public String carSellOrderId; // hex representation of box id
            public long fee;

            // Setters to let Akka Jackson JSON library to automatically deserialize the request body.

            public void setCarSellOrderId(String carSellOrderId) {
                this.carSellOrderId = carSellOrderId;
            }

            public void setFee(long fee) {
                this.fee = fee;
            }
        }
    * Specify the transaction itself. Because we recalled our sell order, the isSeller parameter during transaction creation is set to false.




