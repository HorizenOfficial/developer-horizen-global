====================================
Car Registry Tutorial
====================================

Car Registry App High-Level Overview
####################################

The `Lambo-Registry app <https://github.com/HorizenOfficial/lambo-registry>`_ is a demo dApp implemented as a sidechain, that makes use of custom data and logic. It was developed to serve as a practical example of how the SDK can be extended.
From a functional point of view, the application acts as a repository of existing cars and their owners, and offers to its users the possibility to sell and buy cars. It is a demo application, so it does not include all the needed checks and functionalities that a production application would need; for instance, users are now able to register a car by broadcasting a simple "Car Declaration" transaction. We could think that, in a real-world scenario, the ability to declare the existence of a new car in the sidechain, might be instead subject to the inclusion in the transaction of a certificate signed by the Department of Motor Vehicles, that guarantees that the car exists and it’s owned by a user with a specified public key.

To sum up, the Lambo-Registry applications just accepts transactions that create cars, and then provides the following functionalities:

    1. It stores information that identifies a specific car, such as vehicle identification number (VIN), model, production year, colour.
    2. It allows car owners to be able to prove their ownership of the cars anonymously.
    3. It gives the possibility to sell a car in exchange for ZEN. 



User stories:
#############

As usual, the first step of software development is the analysis. Let's list the functional requirements of our dApp as some simple user requests ("R"), and then the associated design decisions ("D"):

**R: I want to add my car to the Car Registry App.**

*D:* We'll introduce a transaction that creates a "Car Entry Box", with all the vehicle's identification information (VIN, manufacturer, model, year, registration number). The proposition associated to this box is the public key of the owner of the car. When a Car Box is created, the sidechain should verify that the vehicle identification information are unique to this sidechain.

**R: I want to sell my car.**

*D:* We'll introduce a "Car Sell Order Box" that includes the vehicle's information and its price in ZEN. Cars can exist in the sidechain either as a "Car Entry Box" or as a "Car Sell Order Box", but not both at the same time. The Car Sell Order Box will contain also the public key of the prospective buyer, so we assume that some kind of negotiation/agreement between the seller and the buyer took place off-chain. When a sell order is created, the sidechain will have to verify that there is no other active sell order for the same vehicle.


**R: I want to buy a car.**

*D:* To buy a car, the user will have to create a new transaction that accepts a sell order. That sell order must specify the user's public key. The transaction will create a new Car Entry Box, closed by the new owner's public key as proposition. The transaction will also transfer the correct amount of ZEN coins from the buyer to the seller.

**R: I've changed my mind, and don't want to sell my car any more.**

*D:* If the sell order is still active, it can be recalled by its creator. The car owner will create a new transaction containing the Car Sell Order as input, and a Car Entry Box closed by his public key as output.

**R: I want to see all the cars I own, and the ones that have been offered to me.**

*D:* This piece of information will be managed by ApplicationWallet. We can use the SDK standard endpoint "wallet/allBlocks" and filter by box type.


We can now start the development process, by addressing the data representation.


Boxes
#############

When designing a new application, the preliminary step is to identify the needed custom boxes and their respective properties. Boxes are the basic objects that describe the state of our application. The Lambo-registry example implements the following custom boxes:

- **CarBox**  
  A Box that represents a car instance. The following properties were selected to describe a car:

  - vehicle identification number (vin)
  - year of production
  - model
  - color
  
- **CarSellOrderBox**  
  A Box that represents the intention to sell a car to someone. It has the same properties of a car, a price (in ZEN), and it is closed by a special proposition which can be opened either by the seller (to remove the car from sale) or the buyer (to complete the purchase).

Let's have a closer look at the code that defines a CarBox:

  ::

    @JsonView(Views.Default.class)
    @JsonIgnoreProperties({"carId", "value"})
    public final class CarBox extends AbstractBox<PublicKey25519Proposition, CarBoxData, CarBox> {

        public CarBox(CarBoxData boxData, long nonce) {
            super(boxData, nonce);
        }

        @Override
        public BoxSerializer serializer() {
            return CarBoxSerializer.getSerializer();
        }

        @Override
        public byte boxTypeId() {
            return CarBoxId.id();
        }

        CarBoxData getBoxData() {
            return boxData;
        }

        // Set car attributes getters, that is used to automatically construct JSON view:
        public String getVin() {
            return boxData.getVin();
        }

        public int getYear() {
            return boxData.getYear();
        }

        public String getModel() {
            return boxData.getModel();
        }

        public String getColor() {
            return boxData.getColor();
        }

        public byte[] getCarId() {
            return Bytes.concat(
                    getVin().getBytes(),
                    Ints.toByteArray(getYear()),
                    getModel().getBytes(),
                    getColor().getBytes()
            );
        }
    }


Let's start from the top declaration:

  ::

    
    @JsonView(Views.Default.class)
    @JsonIgnoreProperties({"carId", "value"})
    public final class CarBox extends AbstractBox<PublicKey25519Proposition, CarBoxData, CarBox> {
   

 Our class extends the *AbstractBox* default class, is locked by a standard *PublicKey25519Proposition* and keeps all its properties into an object of type CarBoxData.
 The annotation *@JsonView* instructs the SDK to use a default viewer to convert an instance of this class into JSON format when a CarBox is included in the result of an http API endpoint. With that, there is no need to write the conversion code: all the properties associated to getter methods of the class are automatically converted to json attributes. 
 For example, since our class has a getter method "*getModel()*", the json will contain the attribute "model" with its value. 
 We can specify some properties that must be excluded from the json output with the *@JsonIgnoreProperties* annotation.

 The constructor of boxes extending AbstractBox is very simple, it just calls the superclass with two parameters: the BoxData and the nonce.

 
  ::

    public CarBox(CarBoxData boxData, long nonce) {
        super(boxData, nonce);
    }
   
The BoxData is a container of all the properties of our Box, we'll have a look at it later.
The nonce is a random number that allows the generation of different hash values also if the inner properties of two boxes have the same values.


 
  ::

    @Override
    public byte boxTypeId() {
        return CarBoxId.id();
    }
    

The method *boxTypeId()* returns the id of this box type: every custom box needs to have a unique type id inside the application. Note that the ids of custom boxes can overlap with the ids of the standard boxes (e.g. you can re-use the id type 1 that is already used for standard coin boxes).

The next method is used for serialization and deserialization of our Box: it defines the serializer to be used to generate a byte array from the box and to obtain the box back from the byte array:



  ::

    @Override
    public BoxSerializer serializer() {
        return CarBoxSerializer.getSerializer();
    }



 The last methods of the class are just the getters of the box properties. In particular *getCarId()* is an example of a property that is the result of operations performed on other stored properties.

 There are three more classes related to our CarBox: the boxdata and the serializers. Let's have a closer look at them.

BoxData
***********

 BoxData allows us to group all the box properties and their serialization and deserialization logic in a single container object. Although its use is not mandatory (you can define field properties directly inside the Box), it is required if you choose to extend the base class AbstractBox, as we did for the CarBox, and it is in any case a good practice.



  ::

    @JsonView(Views.Default.class)
    public final class CarBoxData extends AbstractBoxData<PublicKey25519Proposition, CarBox, CarBoxData> {

        // In CarRegistry example we defined 4 main car attributes:
        private final String vin;   // Vehicle Identification Number
        private final int year;     // Car manufacture year
        private final String model; // Car Model
        private final String color; // Car color

        public CarBoxData(PublicKey25519Proposition proposition, String vin,
                          int year, String model, String color) {
            super(proposition, 1);
            this.vin = vin;
            this.year = year;
            this.model = model;
            this.color = color;
        }

        public String getVin() {
            return vin;
        }

        public int getYear() {
            return year;
        }

        public String getModel() {
            return model;
        }

        public String getColor() {
            return color;
        }

        @Override
        public CarBox getBox(long nonce) {
            return new CarBox(this, nonce);
        }

        @Override
        public byte[] customFieldsHash() {
            return Blake2b256.hash(
                    Bytes.concat(
                            vin.getBytes(),
                            Ints.toByteArray(year),
                            model.getBytes(),
                            color.getBytes()));
        }

        @Override
        public BoxDataSerializer serializer() {
            return CarBoxDataSerializer.getSerializer();
        }

        @Override
        public String toString() {
            return "CarBoxData{" +
                    "vin=" + vin +
                    ", proposition=" + proposition() +
                    ", model=" + model +
                    ", color=" + color +
                    ", year=" + year +
                    '}';
        }
    }


Let's look in detail at the code above, starting from the beginning:



  ::

    @JsonView(Views.Default.class)
    public final class CarBoxData extends AbstractBoxData<PublicKey25519Proposition, CarBox, CarBoxData> {
    
 

Also this time, we have a basic class we can extend: AbstractBoxData.



  ::

    public CarBoxData(PublicKey25519Proposition proposition, String vin,
                     int year, String model, String color) {
       super(proposition, 1);
       this.vin = vin;
       this.year = year;
       this.model = model;
       this.color = color;
	}
 

The constructor receives all the box properties, and the proposition that locks it. The proposition is passed up to the superclass constructor, which also receives a long number representing the ZEN value of the box. For boxes that don't handle coins (like this one) we can just pass a constant value 1.

 
  ::

    @Override
    public CarBox getBox(long nonce) {
       return new CarBox(this, nonce);
	}

  The *getBox(long nonce)* is a helper method used to generate a new box from the content of this boxdata.



  ::

    @Override
    public byte[] customFieldsHash() {
       return Blake2b256.hash(
               Bytes.concat(
                       vin.getBytes(),
                       Ints.toByteArray(year),
                       model.getBytes(),
                       color.getBytes()));
	}
 
The method *customFieldsHash()* is used by the sidechain to generate a unique hash for each box instance: it needs to be defined in a way such that different property values of a boxdata always produce a different hash value. To achieve this, the code uses a scorex helper class (*scorex.crypto.hash.Blake2b256*) that generates a hash from a bytearray; the bytearray is the concatenation of all the properties values.

Boxdata, as Box, has some methods to define its serializer, and a unique type id:


  ::

    @Override
    public BoxDataSerializer serializer() {
       return CarBoxDataSerializer.getSerializer();
    }

    @Override
    public byte boxDataTypeId() {
       return CarBoxDataId.id();
    }
 


 As expected, the class includes all the getters of every custom property (*getModel()*, *getColor()* etc..). Also, the *toString()* method is redefined to print out the content of boxdata in a more user-friendly format:



  ::

    @Override
    public String toString() {
        return "CarBoxData{" +
                "vin=" + vin +
                ", proposition=" + proposition() +
                ", model=" + model +
                ", color=" + color +
                ", year=" + year +
                '}';
    }
 
  

BoxSerializer and BoxDataSerializer
***********

Serializers are companion classes that are invoked by the SDK every time a Scorex reader and writer needs to deserialize or serialize a Box. We define one serializer/deserializer both for box and for boxdata.
As you can see in the code below, since the "heavy" byte handling happens inside boxdata, their logic is very simple: they just call the right methods already defined in the associated (Box or BoxData) objects.



  ::

    public final class CarBoxSerializer implements BoxSerializer<CarBox> {

        private static final CarBoxSerializer serializer = new CarBoxSerializer();

        private CarBoxSerializer() {
            super();
        }

        public static CarBoxSerializer getSerializer() {
            return serializer;
        }

        @Override
        public void serialize(CarBox box, Writer writer) {
            writer.putLong(box.nonce());
            CarBoxDataSerializer.getSerializer().serialize(box.getBoxData(), writer);
        }

        @Override
        public CarBox parse(Reader reader) {
            long nonce = reader.getLong();
            CarBoxData boxData = CarBoxDataSerializer.getSerializer().parse(reader);

            return new CarBox(boxData, nonce);
        }
    }



  ::


    public final class CarBoxDataSerializer implements BoxDataSerializer<CarBoxData> {

        private static final CarBoxDataSerializer serializer = new CarBoxDataSerializer();

        private CarBoxDataSerializer() {
            super();
        }

        public static CarBoxDataSerializer getSerializer() {
            return serializer;
        }

        @Override
        public void serialize(CarBoxData boxData, Writer writer) {
            PublicKey25519PropositionSerializer.getSerializer().serialize(boxData.proposition(), writer);
            byte[] vinBytes = boxData.getVin().getBytes(StandardCharsets.UTF_8);
            writer.putInt(vinBytes.length);
            writer.putBytes(vinBytes);
            writer.putInt(boxData.getYear());
            byte[] modelBytes = boxData.getModel().getBytes(StandardCharsets.UTF_8);
            writer.putInt(modelBytes.length);
            writer.putBytes(modelBytes);
            byte[] colorBytes = boxData.getColor().getBytes(StandardCharsets.UTF_8);
            writer.putInt(colorBytes.length);
            writer.putBytes(colorBytes);
        }

        @Override
        public CarBoxData parse(Reader reader) {
            PublicKey25519Proposition proposition = PublicKey25519PropositionSerializer.getSerializer().parse(reader);
            int vinBytesLength = reader.getInt();
            String vin = new String(reader.getBytes(vinBytesLength), StandardCharsets.UTF_8);
            int year = reader.getInt();
            int modelBytesLength = reader.getInt();
            String model = new String(reader.getBytes(modelBytesLength), StandardCharsets.UTF_8);
            int colorBytesLength = reader.getInt();
            String color = new String(reader.getBytes(colorBytesLength), StandardCharsets.UTF_8);
            return new CarBoxData(proposition, vin, year, model, color);
        }
    }



Transactions
#############


If Boxes are the objects that describe the state of our application, transactions are the actions that can describe the application state. They typically do that by opening (and therefore removing) some boxes ("input"), and creating new ones ("output").

Our Car Registry application defines the following custom transactions:

- **CarDeclarationTransaction** - a transaction that declares a new car (by creating a new CarBox).
- **SellCarTransaction** - it creates a sell order for a car: a CarBox is "spent", and a CarSellOrderBox containing all the data of the car to be sold is created.
- **BuyCarTransaction** - this transaction is used either by the buyer to accept the sell order, or by the seller to cancel it. It opens a CarSellOrderBox, and creates a CarBox (if it's a sell order cancellation, the new CarBox will be assigned to the original owner).

Let's look at the code of the last one, BuyCarTransaction, that is slightly more complicated than the other two:





  ::

    public final class BuyCarTransaction extends AbstractRegularTransaction {

        private final CarBuyOrderInfo carBuyOrderInfo;

        public final static byte BUY_CAR_TRANSACTION_VERSION = 1;

        private byte version;

        public BuyCarTransaction(List<byte[]> inputZenBoxIds,
                                 List<Signature25519> inputZenBoxProofs,
                                 List<ZenBoxData> outputZenBoxesData,
                                 CarBuyOrderInfo carBuyOrderInfo,
                                 long fee,
                                 byte version) {
            super(inputZenBoxIds, inputZenBoxProofs, outputZenBoxesData, fee);
            this.carBuyOrderInfo = carBuyOrderInfo;
            this.version = version;
        }

        // Specify the unique custom transaction id.
        @Override
        public byte transactionTypeId() {
            return BuyCarTransactionId.id();
        }

        @Override
        protected List<BoxData<Proposition, Box<Proposition>>> getCustomOutputData() {
            ArrayList<BoxData<Proposition, Box<Proposition>>> customOutputData = new ArrayList<>();
            customOutputData.add((BoxData)carBuyOrderInfo.getNewOwnerCarBoxData());
            if(!carBuyOrderInfo.isSpentByOwner())
                customOutputData.add((BoxData)carBuyOrderInfo.getPaymentBoxData());

            return customOutputData;
        }

        @Override
        public byte[] customDataMessageToSign() {
            return new byte[0];
        }

        @Override
        public byte[] customFieldsData() {
            return carBuyOrderInfo.getNewOwnerCarBoxData().bytes();
        }

        @Override
        public byte version() {
            return version;
        }

        // Override unlockers to contains ZenBoxes from the parent class appended with CarSellOrderBox entry.
        @Override
        public List<BoxUnlocker<Proposition>> unlockers() {
            // Get Regular unlockers from base class.
            List<BoxUnlocker<Proposition>> unlockers = super.unlockers();

            BoxUnlocker<Proposition> unlocker = new BoxUnlocker<Proposition>() {
                @Override
                public byte[] closedBoxId() {
                    return carBuyOrderInfo.getCarSellOrderBoxToOpen().id();
                }

                @Override
                public Proof boxKey() {
                    return carBuyOrderInfo.getCarSellOrderSpendingProof();
                }
            };
            // Append with the CarSellOrderBox unlocker entry.
            unlockers.add(unlocker);

            return unlockers;
        }

        // Define object serialization, that should serialize both parent class entries and CarBuyOrderInfo as well
        void serialize(Writer writer) {
            writer.put(version());
            writer.putLong(fee());

            writer.putInt(inputZenBoxIds.size());
            for(byte[] id: inputZenBoxIds)
                writer.putBytes(id);

            zenBoxProofsSerializer.serialize(inputZenBoxProofs, writer);
            zenBoxDataListSerializer.serialize(outputZenBoxesData, writer);
            CarBuyOrderInfoSerializer.getSerializer().serialize(carBuyOrderInfo, writer);
        }

        static BuyCarTransaction parse(Reader reader) {
            byte version = reader.getByte();
            long fee = reader.getLong();

            int inputBytesIdsLength = reader.getInt();
            int idLength = NodeViewModifier$.MODULE$.ModifierIdSize();
            List<byte[]> inputZenBoxIds = new ArrayList<>();
            while(inputBytesIdsLength-- > 0)
                inputZenBoxIds.add(reader.getBytes(idLength));

            List<Signature25519> inputZenBoxProofs = zenBoxProofsSerializer.parse(reader);
            List<ZenBoxData> outputZenBoxesData = zenBoxDataListSerializer.parse(reader);
            CarBuyOrderInfo carBuyOrderInfo = CarBuyOrderInfoSerializer.getSerializer().parse(reader);

            return new BuyCarTransaction(inputZenBoxIds, inputZenBoxProofs, outputZenBoxesData,
                    carBuyOrderInfo, fee, version);
        }

        // Set specific Serializer for BuyCarTransaction class.
        @Override
        public TransactionSerializer serializer() {
            return BuyCarTransactionSerializer.getSerializer();
        }
    }



Let's start from the top declaration: 


  ::

    public final class BuyCarTransaction extends AbstractRegularTransaction {
    

 Our class extends the *AbstractRegularTransaction* default class, an abstract class designed to handle regular coin boxes. Since blockchain transactions usually require the payment of a fee (including the three custom transactions of our Car Registry application), and to pay a fee you need to handle coin boxes, usually custom transactions will extend this abstract class.




  ::

    public BuyCarTransaction(List<byte[]> inputZenBoxIds,
                             List<Signature25519> inputZenBoxProofs,
                             List<ZenBoxData> outputZenBoxesData,
                             CarBuyOrderInfo carBuyOrderInfo,
                             long fee,
                             byte version) {
        super(inputZenBoxIds, inputZenBoxProofs, outputZenBoxesData, fee);
        this.carBuyOrderInfo = carBuyOrderInfo;
        this.version = version;
    }

   
The constructor receives all the parameters related to regular boxes handling (box ids to be opened, proofs to open them, regular boxes to be created, fee to be paid), and pass them up to the superclass. Moreover, it receives all other parameters specifically related to the custom boxes; in our example, the transaction needs info about the sell order that it needs to open, and it finds in the CarBuyOrderInfo object.



  ::

    @Override
    public List<BoxUnlocker<Proposition>> unlockers() {
        // Get Regular unlockers from base class.
        List<BoxUnlocker<Proposition>> unlockers = super.unlockers();

        BoxUnlocker<Proposition> unlocker = new BoxUnlocker<Proposition>() {
            @Override
            public byte[] closedBoxId() {
                return carBuyOrderInfo.getCarSellOrderBoxToOpen().id();
            }

            @Override
            public Proof boxKey() {
                return carBuyOrderInfo.getCarSellOrderSpendingProof();
            }
        };
        unlockers.add(unlocker);
        return unlockers;
    }


The *unlockers()* method must return a list of BoxUnlocker's, that contains the boxes which will be opened by this transaction, and the proofs to open them. The list returned from the superclass (in the first line of the method) contains the unlockers for the coin boxes, and it is combined with the unlocker for the CarSellOrderBox. As you can see we have used an inline declaration for the new unlocker, since it is a very simple object that has only two methods, one returning the box id to open and the other one the proof to open it.



  ::

    @Override
    public byte transactionTypeId() {
        return BuyCarTransactionId.id();
    }
 

Just like with boxes, also each transaction type must have a unique id, returned by the method *transactionTypeId()*.

The last three methods of the class are related to the serialization handling.
The approach is very similar to what we saw for boxes: the methods *bytes()* and *parseBytes(byte[] bytes)* perform a "two-way conversion" into and from an array of bytes, while the *serializer()* method returns the serializer helper to operate with Scorex reader's and writer's.

As we did with the CarBox, also here we have chosen to code the low level "byte handling" logic inside the two methods *serialize()* and *parse(Reader reader)*, keeping a very simple implementation for the serializer:




  ::

    public final class BuyCarTransactionSerializer implements TransactionSerializer<BuyCarTransaction> {

        private static final BuyCarTransactionSerializer serializer = new BuyCarTransactionSerializer();

        private BuyCarTransactionSerializer() {
            super();
        }

        public static BuyCarTransactionSerializer getSerializer() {
            return serializer;
        }

        @Override
        public void serialize(BuyCarTransaction transaction, Writer writer) {
            transaction.serialize(writer);
        }

        @Override
        public BuyCarTransaction parse(Reader reader) {
            return BuyCarTransaction.parse(reader);
        }
    }


One of the parameters of the class constructor is CarBuyOrderInfo, an object that contains the needed info about the sell order we are handling. Let's take a look at its implementation:




  ::

    public final class CarBuyOrderInfo implements BytesSerializable {
        final CarSellOrderBox carSellOrderBoxToOpen;  // Sell order box to be spent in BuyCarTransaction
        final SellOrderSpendingProof proof;           // Proof to unlock the box above

        public CarBuyOrderInfo(CarSellOrderBox carSellOrderBoxToOpen, SellOrderSpendingProof proof) {
            this.carSellOrderBoxToOpen = carSellOrderBoxToOpen;
            this.proof = proof;
        }

        public CarSellOrderBox getCarSellOrderBoxToOpen() {
            return carSellOrderBoxToOpen;
        }

        public SellOrderSpendingProof getCarSellOrderSpendingProof() {
            return proof;
        }

        // Recreates output CarBoxData with the same attributes specified in CarSellOrder.
        // Specifies the new owner depends on proof provided:
        // 1) if the proof is from the seller then the owner remain the same
        // 2) if the proof is from the buyer then it will become the new owner
        public CarBoxData getNewOwnerCarBoxData() {
            PublicKey25519Proposition proposition;
            if(proof.isSeller()) {
                proposition = new PublicKey25519Proposition(carSellOrderBoxToOpen.proposition().getOwnerPublicKeyBytes());
            } else {
                proposition = new PublicKey25519Proposition(carSellOrderBoxToOpen.proposition().getBuyerPublicKeyBytes());
            }

            return new CarBoxData(
                    proposition,
                    carSellOrderBoxToOpen.getVin(),
                    carSellOrderBoxToOpen.getYear(),
                    carSellOrderBoxToOpen.getModel(),
                    carSellOrderBoxToOpen.getColor()
            );
        }

        // Check if proof is provided by Sell order owner.
        public boolean isSpentByOwner() {
            return proof.isSeller();
        }

        // Coins to be paid to the owner of Sell order in case if Buyer spent the Sell order.
        public ZenBoxData getPaymentBoxData() {
            return new ZenBoxData(
                    new PublicKey25519Proposition(carSellOrderBoxToOpen.proposition().getOwnerPublicKeyBytes()),
                    carSellOrderBoxToOpen.getPrice()
            );
        }

        @Override
        public byte[] bytes() {
            return serializer().toBytes(this);
        }

        @Override
        public ScorexSerializer<BytesSerializable> serializer() {
            return (ScorexSerializer) CarBuyOrderInfoSerializer.getSerializer();
        }
    }

 

 If you look at the code above, you can see that this object is not much more than a container of the information that needs to be processed: the CarSellOrderBox that should be opened, and the proof to open it. It then includes their getters, and a couple of "utility" methods: *getNewOwnerCarBoxData()* and *getPaymentBoxData()*. The first one, *getNewOwnerCarBoxData()*, creates a new CarBox with the same properties of the sold car, and "assigns" it (by locking it with the right proposition) to either the buyer or the seller, depending on who opened the order.




  ::

    public CarBoxData getNewOwnerCarBoxData() {
        PublicKey25519Proposition proposition;
        if(proof.isSeller()) {
            proposition = new PublicKey25519Proposition(carSellOrderBoxToOpen.proposition().getOwnerPublicKeyBytes());
        } else {
            proposition = new PublicKey25519Proposition(carSellOrderBoxToOpen.proposition().getBuyerPublicKeyBytes());
        }
        return new CarBoxData(
                proposition,
                carSellOrderBoxToOpen.getVin(),
                carSellOrderBoxToOpen.getYear(),
                carSellOrderBoxToOpen.getModel(),
                carSellOrderBoxToOpen.getColor()
        );
    }


The second one, *getPaymentBoxData()*, creates a coin box with the payment of the order price to the seller (it will be used only if the buyer accepts the order):




  ::

    public ZenBoxData getPaymentBoxData() {
        return new ZenBoxData(
                new PublicKey25519Proposition(carSellOrderBoxToOpen.proposition().getOwnerPublicKeyBytes()),
                carSellOrderBoxToOpen.getPrice()
        );
    }


Also this time we have the methods to serialize and deserialize the object: since the CarBuyOrderInfo is a property of our transaction and the transaction can be serialized, we need to be able to serialize and deserialize it as well.

Now that we have seen how a transaction is built, you may wonder how it can be created and submitted to the sidechain. This could be achieved in several ways, depending on the needs of our application, e.g. by using an RPC command, a code defined trigger, an offline wallet that creates the byte-array of the transaction and sends it through the default API method '*transaction/sendTransaction*', ... 
One of the most common ways to support the creation of a custom transaction is by extending the default API endpoints, and add a new custom local wallet endpoint to let the user create it via HTTP. We will look into that at the end of this chapter.


Custom proof and proposition
#######################################

A proposition is a box locker, and a proof is its unlocker.
The SDK offers default Propositions and Proofs, and a developer can define custom ones.

Inside the Lambo Registry application, you can find a custom proposition: SellOrderProposition. It requires two public keys, while the corresponding proof (SellOrderSpendingProof) is able to unlock it by supplying only one of those two keys.

Let's look at them, starting with the SellOrderProposition:




  ::

    @JsonView(Views.Default.class)
    public final class SellOrderProposition implements ProofOfKnowledgeProposition<PrivateKey25519> {
        static final int KEY_LENGTH = Ed25519.publicKeyLength();

        // Specify json attribute name for the ownerPublicKeyBytes field.
        @JsonProperty("ownerPublicKey")
        private final byte[] ownerPublicKeyBytes;

        // Specify json attribute name for the buyerPublicKeyBytes field.
        @JsonProperty("buyerPublicKey")
        private final byte[] buyerPublicKeyBytes;

        public SellOrderProposition(byte[] ownerPublicKeyBytes, byte[] buyerPublicKeyBytes) {
            if(ownerPublicKeyBytes.length != KEY_LENGTH)
                throw new IllegalArgumentException(String.format("Incorrect ownerPublicKeyBytes length, %d expected, %d found", KEY_LENGTH, ownerPublicKeyBytes.length));

            if(buyerPublicKeyBytes.length != KEY_LENGTH)
                throw new IllegalArgumentException(String.format("Incorrect buyerPublicKeyBytes length, %d expected, %d found", KEY_LENGTH, buyerPublicKeyBytes.length));

            this.ownerPublicKeyBytes = Arrays.copyOf(ownerPublicKeyBytes, KEY_LENGTH);

            this.buyerPublicKeyBytes = Arrays.copyOf(buyerPublicKeyBytes, KEY_LENGTH);
        }


        @Override
        public byte[] pubKeyBytes() {
            return Arrays.copyOf(ownerPublicKeyBytes, KEY_LENGTH);
        }

        public byte[] getOwnerPublicKeyBytes() {
            return pubKeyBytes();
        }

        public byte[] getBuyerPublicKeyBytes() {
            return Arrays.copyOf(buyerPublicKeyBytes, KEY_LENGTH);
        }

        @Override
        public PropositionSerializer serializer() {
            return SellOrderPropositionSerializer.getSerializer();
        }

        @Override
        public int hashCode() {
            int result = Arrays.hashCode(ownerPublicKeyBytes);
            result = 31 * result + Arrays.hashCode(buyerPublicKeyBytes);
            return result;
        }

        @Override
        public boolean equals(Object obj) {
            if (obj == null)
                return false;
            if (!(obj instanceof SellOrderProposition))
                return false;
            if (obj == this)
                return true;
            SellOrderProposition that = (SellOrderProposition) obj;
            return Arrays.equals(ownerPublicKeyBytes, that.ownerPublicKeyBytes)
                    && Arrays.equals(buyerPublicKeyBytes, that.buyerPublicKeyBytes);
        }
    }



As you can see from the code above, a custom proposition can have a number of private fields; in our case the *ownerPublicKeyBytes* and *buyerPublicKeyBytes* properties, which also have *getOwnerPublicKeyBytes()* and *getBuyerPublicKeyBytes()* as getter methods. 

A custom proposition must:

- **implement the ProofOfKnowledgeProposition interface**, and define its "pubKeyBytes" method, that returns a byte representation of the public key of this proposition:

  ::

    @Override
    public byte[] pubKeyBytes() {
        return Arrays.copyOf(ownerPublicKeyBytes, KEY_LENGTH);
    }
    
- **provide the usual method and class for serialization and deserialization**: 
   -  serializer()
   - implement SellOrderPropositionSerializer:

   ::

    public final class SellOrderPropositionSerializer implements PropositionSerializer<SellOrderProposition> {

        private static final SellOrderPropositionSerializer serializer = new SellOrderPropositionSerializer();

        private SellOrderPropositionSerializer() {
            super();
        }

        public static SellOrderPropositionSerializer getSerializer() {
            return serializer;
        }

        @Override
        public void serialize(SellOrderProposition proposition, Writer writer) {
            writer.putBytes(proposition.getOwnerPublicKeyBytes());
            writer.putBytes(proposition.getBuyerPublicKeyBytes());
        }

        @Override
        public SellOrderProposition parse(Reader reader) {
            byte[] ownerPublicKeyBytes = reader.getBytes(SellOrderProposition.KEY_LENGTH);
            byte[] buyerPublicKeyBytes = reader.getBytes(SellOrderProposition.KEY_LENGTH);

            return new SellOrderProposition(ownerPublicKeyBytes, buyerPublicKeyBytes);
        }
    }


- **implement the hashCode() and equals() methods**, used to compare the proposition with other ones:

 


  ::

    @Override
    public int hashCode() {
        int result = Arrays.hashCode(ownerPublicKeyBytes);
        result = 31 * result + Arrays.hashCode(buyerPublicKeyBytes);
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null)
            return false;
        if (!(obj instanceof SellOrderProposition))
            return false;
        if (obj == this)
            return true;
        SellOrderProposition that = (SellOrderProposition) obj;
        return Arrays.equals(ownerPublicKeyBytes, that.ownerPublicKeyBytes)
                && Arrays.equals(buyerPublicKeyBytes, that.buyerPublicKeyBytes);
    }
 
   

Now we can analyse the corresponding proof class, SellOrderSpendingProof:




  ::

    public final class SellOrderSpendingProof extends AbstractSignature25519<PrivateKey25519, SellOrderProposition> {
        // To distinguish who opened the CarSellOrderBox: seller or buyer
        private final boolean isSeller;
        private final byte[] signatureBytes;

        public static final int SIGNATURE_LENGTH = Ed25519.signatureLength();

        public SellOrderSpendingProof(byte[] signatureBytes, boolean isSeller) {
            super(signatureBytes);
            if (signatureBytes.length != SIGNATURE_LENGTH)
                throw new IllegalArgumentException(String.format("Incorrect signature length, %d expected, %d found", SIGNATURE_LENGTH,
                        signatureBytes.length));
            this.isSeller = isSeller;
            this.signatureBytes = signatureBytes;
        }

        public boolean isSeller() {
            return isSeller;
        }

        public byte[] signatureBytes() {
            return Arrays.copyOf(signatureBytes, SIGNATURE_LENGTH);
        }

        // Depends on isSeller flag value check the signature against seller or buyer public key specified in SellOrderProposition.
        @Override
        public boolean isValid(SellOrderProposition proposition, byte[] message) {
            if(isSeller) {
                // Car seller wants to discard selling.
                return Ed25519.verify(signatureBytes, message, proposition.getOwnerPublicKeyBytes());
            } else {
                // Specific buyer wants to buy the car.
                return Ed25519.verify(signatureBytes, message, proposition.getBuyerPublicKeyBytes());
            }
        }

        @Override
        public byte[] bytes() {
            return Bytes.concat(
                    new byte[] { (isSeller ? (byte)1 : (byte)0) },
                    signatureBytes
            );
        }

        public static SellOrderSpendingProof parseBytes(byte[] bytes) {
            int offset = 0;

            boolean isSeller = bytes[offset] != 0;
            offset += 1;

            byte[] signatureBytes = Arrays.copyOfRange(bytes, offset, offset + SIGNATURE_LENGTH);

            return new SellOrderSpendingProof(signatureBytes, isSeller);
        }

        @Override
        public ProofSerializer serializer() {
            return SellOrderSpendingProofSerializer.getSerializer();
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            SellOrderSpendingProof that = (SellOrderSpendingProof) o;
            return Arrays.equals(signatureBytes, that.signatureBytes) && isSeller == that.isSeller;
        }

        @Override
        public int hashCode() {
            int result = Objects.hash(signatureBytes.length);
            result = 31 * result + Arrays.hashCode(signatureBytes);
            result = 31 * result + (isSeller ? 1 : 0);
            return result;
        }
    }
  

 The most important method here is *isValid*: it receives a proposition and a byte[] message, and checks that the signature contained in this proof is valid against them. The signature was passed in the constructor. If this method returns true, any box locked with the proposition can be opened with this proof.




  ::

    @Override
    public boolean isValid(SellOrderProposition proposition, byte[] message) {
        if(isSeller) {
            // Car seller wants to discard selling.
            return Ed25519.verify(
                signatureBytes, message, proposition.getOwnerPublicKeyBytes()
            );
        } else {
            // Specific buyer wants to buy the car.
            return Ed25519.verify(
                signatureBytes, message, proposition.getBuyerPublicKeyBytes()
            );
        }
    }    
  

 You should be familiar with all the other methods. *proofTypeId* returns a unique identifier of this proof type:




  ::

    @Override
    public byte proofTypeId() {
        return CarRegistryProofsIdsEnum.SellOrderSpendingProofId.id();
    }
   
Then we have the methods that compare the proof with other ones:




  ::

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        SellOrderSpendingProof that = (SellOrderSpendingProof) o;
        return Arrays.equals(signatureBytes, that.signatureBytes) && isSeller == that.isSeller;
    }

    @Override
    public int hashCode() {
        int result = Objects.hash(signatureBytes.length);
        result = 31 * result + Arrays.hashCode(signatureBytes);
        result = 31 * result + (isSeller ? 1 : 0);
        return result;
    }
    


 and the methods to serialize and deserialize it;

 


  ::

    @Override
    public ProofSerializer serializer() {
        return SellOrderSpendingProofSerializer.getSerializer();
    }
   

  ::

    @Override
    public void serialize(SellOrderSpendingProof boxData, Writer writer) {
        writer.put(boxData.isSeller() ? (byte)1 : (byte)0);
        writer.putBytes(boxData.signatureBytes());
    }

    @Override
    public SellOrderSpendingProof parse(Reader reader) {
        boolean isSeller = reader.getByte() != 0;
        byte[] signatureBytes = reader.getBytes(SellOrderSpendingProof.SIGNATURE_LENGTH);

        return new SellOrderSpendingProof(signatureBytes, isSeller);
    }

Please note: the relationship between proposition, proofs and boxes is already defined by the generics used when declaring them. For example, the SellOrderProposition (first row below) is also part of the declaration of the related proof and custom box (CarSellOrderBox) that gets locked by it:

public final class **SellOrderProposition** implements ProofOfKnowledgeProposition<PrivateKey25519> 

public final class SellOrderSpendingProof extends AbstractSignature25519<PrivateKey25519, **SellOrderProposition**> 

public final class CarSellOrderBox extends AbstractBox<**SellOrderProposition**, CarSellOrderBoxData, CarSellOrderBox> 

This way, some design errors can be identified already at compile time.


Application state
##########################


By implementing the *io.horizen.utxo.state.ApplicationState* interface with a custom class, developers can:

- define specific rules to validate transactions (before they are accepted in the mempool and later when included in a block)
- define specific rules to validate blocks (before they are appended to the blockchain)
- be notified when a new block is added to the blockchain ("*onApplyChanges*"), receiving all the boxes created and removed by its transactions, or when a block revert happens ("*onRollback*").

The methods of the interface are the following ones:




  ::

    public interface ApplicationState {
    
    	void validate(SidechainStateReader stateReader, SidechainBlock block) throws IllegalArgumentException;

        void validate(SidechainStateReader stateReader, BoxTransaction<Proposition, Box<Proposition>> transaction) throws IllegalArgumentException;

    	Try<ApplicationState> onApplyChanges(SidechainStateReader stateReader, byte[] blockId, List<Box<Proposition>> newBoxes, List<byte[]> boxIdsToRemove);

    	Try<ApplicationState> onRollback(byte[] blockId);

        boolean checkStoragesVersion(byte[] blockId);
    }


Please note how the block revert notification is implemented: a byte[] representing a version id is passed every time *onApplyChanges* is called. If a rollback happens, the same version id is passed by the *onRollback* method: all versions after that one have to be discarded.

The method *checkStoragesVersion* is called by the SDK in order to check the alignment of SDK and any application custom storages versions (if any) at node restart.

Most methods have a *SidechainStateReader* parameter. It's a utility class you can use to access the closed boxes of the sidechain, i.e. all the boxes that haven't been spent yet. Here its interface definition:




  ::

    public interface SidechainStateReader {
        Optional<Box> getClosedBox(byte[] boxId);
    }


Now let's see how the application State is used in our Lambo Registry app, staring from the *onApplyChanges* method:




  ::

    @Override
    public Try<ApplicationState> onApplyChanges(SidechainStateReader stateReader,
                                                byte[] blockId,
                                                List<Box<Proposition>> newBoxes, List<byte[]> boxIdsToRemove) {
        //we update the Car info database. The data from it will be used during validation.

        //collect the vin to be added: the ones declared in new boxes
        Set<String> vinToAdd = carInfoDbService.extractVinFromBoxes(newBoxes);
        //collect the vin to be removed: the ones contained in the removed boxes that are not present in the previous list
        Set<String> vinToRemove = new HashSet<>();
        for (byte[] boxId : boxIdsToRemove) {
            stateReader.getClosedBox(boxId).ifPresent( box -> {
                    if (box instanceof CarBox){
                        String vin = ((CarBox)box).getVin();
                        if (!vinToAdd.contains(vin)){
                            vinToRemove.add(vin);
                        }
                    } else if (box instanceof CarSellOrderBox){
                        String vin = ((CarSellOrderBox)box).getVin();
                        if (!vinToAdd.contains(vin)){
                            vinToRemove.add(vin);
                        }
                    }
                }
            );
        }
        carInfoDbService.updateVin(blockId, vinToAdd, vinToRemove);
        return new Success<>(this);
    }


As you can see this method is used to update a list containing all the VIN (vehicle identification numbers) that appear in our blockchain. To do that, it inspects the two types of boxes that contain a VIN (CarBox and CarSellOrderBox), and adds each VIN to the list if the box has been created, or remove it if the box has been spent.
Since this method is called every time a new block is appended to the chain, we can be sure the list is always updated.

The list is then used in the *validate* method. 
To validate a single transaction, we check that the VIN is not already in the list:




  ::

    @Override
    void validate(SidechainStateReader stateReader, BoxTransaction<Proposition, Box<Proposition>> transaction) throws IllegalArgumentException {
        // we go through all CarDeclarationTransactions and verify that each CarBox represents a unique Car.
        if (CarDeclarationTransaction.class.isInstance(transaction)){
            Set<String> vinList = carInfoDbService.extractVinFromBoxes(transaction.newBoxes());
            for (String vin : vinList) {
                if (! carInfoDbService.validateVin(vin, Optional.empty())){
                    throw new IllegalArgumentException("Vin has been used before.");
                }
            }
        }
    }


To validate an entire block, we need an additional check, to be sure that in the same block two different transactions don't declare the same VIN:




  ::

    @Override
    void validate(SidechainStateReader stateReader, SidechainBlock block) throws IllegalArgumentException {
        //We check that there are no multiple transactions declaring the same VIN inside the block
        Set<String> vinList = new HashSet<>();
        for (BoxTransaction<Proposition, Box<Proposition>> t :  JavaConverters.seqAsJavaList(block.transactions())){
            if (CarDeclarationTransaction.class.isInstance(t)){
                for (String currentVin :  carInfoDbService.extractVinFromBoxes(t.newBoxes())){
                    if (vinList.contains(currentVin)){
                        throw new IllegalArgumentException("Vin has been used in another transaction.");
                    }else{
                        vinList.add(currentVin);
                    }
                }
            }
        }
	}


The *rollback* method, which is very simple and delegates all the logic to the service used to store our list:




  ::

    @Override
    public Try<ApplicationState> onRollback(byte[] blockId) {
        carInfoDbService.rollback(blockId);
        return new Success<>(this);
    }


Finally, the *checkStoragesVersion* method, which is also very simple and just check the version of *carInfoDbService* storage against the input parameter:




  ::

    @Override
    public boolean checkStoragesVersion(byte[] blockId)
    {
        byte[] ver = carInfoDbService.lastVersionID().orElse(new ByteArrayWrapper(NULL_VERSION)).data();
        return Arrays.equals(blockId, ver);
    }



Application wallet
##########################

The interface *io.horizen.utxo.wallet.ApplicationWallet* is another extension point that allows an application to be notified each time a secret or box is added or removed from the sidechain node local wallet.




  ::

    public interface ApplicationWallet {
      void onAddSecret(Secret secret);
      void onRemoveSecret(Proposition proposition);
      void onChangeBoxes(byte[] blockId, List<Box<Proposition>> boxesToUpdate, List<byte[]> boxIdsToRemove);
      void onRollback(byte[] blockId);
      boolean checkStoragesVersion(byte[] blockId);
    }


The Lambo registry example does not implement the interface *ApplicationWallet* because its wallet has basic requirements. You may need to use interface *io.horizen.utxo.wallet.ApplicationWallet* depending on your app requirements. For example, if the app needs to maintain a separate wallet balance or counter of a specific kind of custom boxes associated to locally stored keys, you could put the code that updates those records inside the *onChangeBoxes* method.


Application Stopper 
#############################

The interface *io.horizen.SidechainAppStopper* allows an application to be called when the node stop procedure is initiated:

::

  public interface SidechainAppStopper {
      void stopAll();
  }



Such a procedure can be explicitly triggered via the API 'node/stop' or can be triggered when the JVM is shutting down,
for instance when a SIGINT is received.
In the Lambo registry implementation of the method 'void stopAll()', the *carInfoDbService* storage is closed:

::

    @Override
    public void stopAll() {
        carInfoDbService.close()
    }



API extension
##########################

An application can extend the standard API endpoints and define custom ones.
As an example, the Lambo Registry application adds four endpoints, one for each added transaction:

- createCar
- createCarSellOrder
- acceptCarSellOrder
- cancelCarSellOrder

These new endpoints do not broadcast the transaction directly, but only produce a signed hex version of it; to execute the transaction, the user will later have to post it to the standard endpoint  */transaction/sendTransaction*. This approach is just a design choice, so it's not a mandatory requirement.
Before looking at the code, please note that all these endpoints need to interact with the local wallet to unlock boxes and sign the transactions.

So, the first step to add endpoints is to extend the *io.horizen.api.http.ApplicationApiGroup* class, and implement its two methods:


  ::

    @Override
    public String basePath() {
        return "carApi";
    	}

    @Override
    public List<Route> getRoutes() {
        List<Route> routes = new ArrayList<>();
        routes.add(bindPostRequest("createCar", this::createCar, CreateCarBoxRequest.class));
        routes.add(bindPostRequest("createCarSellOrder", this::createCarSellOrder, CreateCarSellOrderRequest.class));
        routes.add(bindPostRequest("acceptCarSellOrder", this::acceptCarSellOrder, SpendCarSellOrderRequest.class));
        routes.add(bindPostRequest("cancelCarSellOrder", this::cancelCarSellOrder, SpendCarSellOrderRequest.class));
        return routes;
    }


The first method defines the first part of our endpoint urls.

The second method returns the list of the new routes.
The SDK uses the `Akka Http Routing library <https://doc.akka.io/docs/akka-http/current/routing-dsl/routes.html>`_, and the type of each array element returned by this method must be an Akka Route. In most cases (including the Lambo registry example) you don't have to know much more about Akka routes, as you can just use the provided *bindPostRequest* method to build a route element.
The *bindPostRequest* method returns an Akka route that responds to an HTTP POST request, and receives three parameters:

- a String, representing the request path
- the method implementing the logic
- a class representing the request class

We can see all this in the first endpoint defined in the Lambo registry: "createCar".

This is the class associated to its request (CreateCarBoxRequest - the third parameter):

  ::

    public class CreateCarBoxRequest {
    	public String vin;
    	public int year;
    	public String model;
    	public String color;
    	public String proposition; 
    	public long fee;

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


As you can see the class is just a javabean that will map the fields of the input json into the request body. You have to provide the setter of each property, to allow the SDK engine to populate the fields with the request data.

Now let's check out the method implementing the endpoint logic (i.e. the second parameter of the *bindPostRequest* method):


  ::

    private ApiResponse createCar(SidechainNodeView view, CreateCarBoxRequest ent) {
        try {
            // Parse the proposition of the Car owner.
            PublicKey25519Proposition carOwnershipProposition = PublicKey25519PropositionSerializer.getSerializer()
                    .parseBytes(BytesUtils.fromHexString(ent.proposition));

            //check that the vin is unique (both in local veichle store and in mempool)
            if (! carInfoDBService.validateVin(ent.vin, Optional.of(view.getNodeMemoryPool()))){
                throw new IllegalStateException("Vehicle identification number already present in blockchain");
            }

            CarBoxData carBoxData = new CarBoxData(carOwnershipProposition, ent.vin, ent.year, ent.model, ent.color);

            // Try to collect regular boxes to pay fee
            List<Box<Proposition>> paymentBoxes = new ArrayList<>();
            long amountToPay = ent.fee;

            // Avoid to add boxes that are already spent in some Transaction that is present in node Mempool.
            List<byte[]> boxIdsToExclude = boxesFromMempool(view.getNodeMemoryPool());
            List<Box<Proposition>> ZenBoxes = view.getNodeWallet().boxesOfType(ZenBox.class, boxIdsToExclude);
            int index = 0;
            while (amountToPay > 0 && index < ZenBoxes.size()) {
                paymentBoxes.add(ZenBoxes.get(index));
                amountToPay -= ZenBoxes.get(index).value();
                index++;
            }

            if (amountToPay > 0) {
                throw new IllegalStateException("Not enough coins to pay the fee.");
            }

            // Set change if exists
            long change = Math.abs(amountToPay);
            List<ZenBoxData> regularOutputs = new ArrayList<>();
            if (change > 0) {
                regularOutputs.add(new ZenBoxData((PublicKey25519Proposition) paymentBoxes.get(0).proposition(), change));
            }

            // Create fake proofs to be able to create transaction to be signed.
            List<byte[]> inputIds = new ArrayList<>();
            for (Box b : paymentBoxes) {
                inputIds.add(b.id());
            }

            List fakeProofs = Collections.nCopies(inputIds.size(), null);
            Long timestamp = System.currentTimeMillis();

            CarDeclarationTransaction unsignedTransaction = new CarDeclarationTransaction(
                    inputIds,
                    fakeProofs,
                    regularOutputs,
                    carBoxData,
                    ent.fee,
                    timestamp);

            // Get the Tx message to be signed.
            byte[] messageToSign = unsignedTransaction.messageToSign();

            // Create real signatures.
            List<Signature25519> proofs = new ArrayList<>();
            for (Box<Proposition> box : paymentBoxes) {
                proofs.add((Signature25519) view.getNodeWallet().secretByPublicKey(box.proposition()).get().sign(messageToSign));
            }

            // Create the transaction with real proofs.
            CarDeclarationTransaction signedTransaction = new CarDeclarationTransaction(
                    inputIds,
                    proofs,
                    regularOutputs,
                    carBoxData,
                    ent.fee,
                    timestamp);

            return new TxResponse(ByteUtils.toHexString(sidechainTransactionsCompanion.toBytes((BoxTransaction) signedTransaction)));
        }
        catch (Exception e) {
            return new CarResponseError("0102", "Error during Car declaration.", Some.apply(e));
        }
    }


Please note that:

- the method receives two parameters: the first one is *SidechainNodeView*, an utility class that gives access to a snapshot of the current blockchain state and the current wallet. It can be used, for example, to find a closed box owned by the user, that is a box that can be spent in the transaction. The second parameter is the "request class" previously introduced. 
- the method must return a class implementing the *ApiResponse* interface, or its sub-interface *SuccessResponse* if the method executes without errors. It can be any javabean, but it must include the *@JsonView* annotation, to instruct the SDK engine to serialize it to json, and must expose the data to be returned in public fields. The response class in the Lambo registry example has only one field (*transactionBytes*), which is a String containing the HEX representation of the created transaction:

  ::

    @JsonView(Views.Default.class)
    static class TxResponse implements SuccessResponse {
        public String transactionBytes;

        public TxResponse(String transactionBytes) {
            this.transactionBytes = transactionBytes;
        }
    }


If we now look into the method logic, we can see that, at first, it parses the input data and constructs the objects from it (carOwnershipProposition and carBoxData).
It also performs a security check that returns an error if the user tries to declare a car with a Vehicle Identification Number which already exists: 

  ::

	// Parse the proposition of the Car owner.
	PublicKey25519Proposition carOwnershipProposition = PublicKey25519PropositionSerializer.getSerializer()
    	.parseBytes(BytesUtils.fromHexString(ent.proposition));

	//check that the vin is unique (both in local veichle store and in mempool)
	if (! carInfoDBService.validateVin(ent.vin, Optional.of(view.getNodeMemoryPool()))){
            throw new IllegalStateException("Vehicle identification number already present in blockchain");
	}

	CarBoxData carBoxData = new CarBoxData(carOwnershipProposition, ent.vin, ent.year, ent.model, ent.color);

One more note about the Vehicle Identification Number check: a similar check is also performed in the applicationState as part of the consensus validation, to discard invalid transactions. As a general design rule, all checks on data correctness must be performed in both points. This way, transactions are verified by the endpoint. The endpoint will only allow valid transactions on the network. If a user tries to bypass the creation endpoint by broadcasting the binary transaction hex directly, the consensus check will not accept invalid transactions.

After this check, the code builds two lists: *paymentBoxes*, a list of coins used to pay the fee, and *regularOutputs*, the output boxes. We start this second list with the change (if any) of the fee payment.


  ::

	// Try to collect regular boxes to pay fee
    List<Box<Proposition>> paymentBoxes = new ArrayList<>();
    long amountToPay = ent.fee;

    // Avoid to add boxes that are already spent by transactions in the node Mempool.
    List<byte[]> boxIdsToExclude = boxesFromMempool(view.getNodeMemoryPool());
    List<Box<Proposition>> ZenBoxes = view.getNodeWallet().boxesOfType(ZenBox.class, boxIdsToExclude);
    int index = 0;
    while (amountToPay > 0 && index < ZenBoxes.size()) {
        paymentBoxes.add(ZenBoxes.get(index));
        amountToPay -= ZenBoxes.get(index).value();
        index++;
    }

    if (amountToPay > 0) {
        throw new IllegalStateException("Not enough coins to pay the fee.");
    }

    // Set change if exists
    long change = Math.abs(amountToPay);
    List<ZenBoxData> regularOutputs = new ArrayList<>();
    if (change > 0) {
        regularOutputs.add(new ZenBoxData((PublicKey25519Proposition) 
           paymentBoxes.get(0).proposition(), change));
    }


Now everything is ready to build and sign the transaction.
To generate signature proofs, we need the transaction bytes. 
But to obtain the transaction bytes, we need to create it with the needed proofs.
To cut this dependency loop, transactions are built in the following way:

1. Create fake/empty proofs,
2. Create transaction by using those dummy proofs
3. Receive Tx message to be signed from transaction at step 2 (we can do it because proofs are not part of the message that needs to be signed)
4. Create real proof by using Tx message to be signed
5. Create the real transaction with real proofs

In the code:


  ::

	// Create fake proofs to be able to create transaction to be signed.
    List<byte[]> inputIds = new ArrayList<>();
    for (Box b : paymentBoxes) {
        inputIds.add(b.id());
    }

    List fakeProofs = Collections.nCopies(inputIds.size(), null);
    Long timestamp = System.currentTimeMillis();

    CarDeclarationTransaction unsignedTransaction = new CarDeclarationTransaction(
            inputIds,
            fakeProofs,
            regularOutputs,
            carBoxData,
            ent.fee,
            timestamp);

    // Get the Tx message to be signed.
    byte[] messageToSign = unsignedTransaction.messageToSign();

    // Create real signatures.
    List<Signature25519> proofs = new ArrayList<>();
    for (Box<Proposition> box : paymentBoxes) {
        proofs.add((Signature25519) view.getNodeWallet()
            .secretByPublicKey(box.proposition())
            .get()
            .sign(messageToSign));
    }

    // Create the transaction with real proofs.
    CarDeclarationTransaction signedTransaction = new CarDeclarationTransaction(
            inputIds,
            proofs,
            regularOutputs,
            carBoxData,
            ent.fee,
            timestamp);

          

 Finally, the response construction:

 
  ::

	return new TxResponse(
        ByteUtils.toHexString(sidechainTransactionsCompanion.toBytes((BoxTransaction) signedTransaction))
    );
     


As a result, this endpoint will be exposed by this url: */carApi/createCar*
and will be invoked with a post http request.
Input and output data will be represented in json format.

The structure of the others endpoints is similar, it's a good exercise to check them out and see how they were implemented.












