.. _install-sidechain-sdk-tutorial:

########################
Installing the Horizen Sidechain SDK
########################

We'll get started by setting up our environment.

*******************
Supported Platforms
*******************

The Sidechain SDK is available and tested on 64-bit versions of Linux and Windows.


************
Requirements
************

The Sidechain SDK requires Java 11 or newer, Scala 2.12.10+ or newer, and the latest version of `zen <https://github.com/ZencashOfficial/zen>`_.


**********************
Installing on Windows
**********************

  1. Install Java JDK version 11 (`link <https://www.oracle.com/java/technologies/javase-jdk11-downloads.html>`_)
  2. Install Scala 2.12.10+ (`link <https://www.scala-lang.org/download/2.12.10.html>`_)
  3. Install Git (`link <https://git-scm.com/downloads>`_)
  4. Clone the Sidechains-SDK git repository 

  .. code:: Bash
  
     git clone git@github.com:HorizenOfficial/Sidechains-SDK.git
    
  5. As IDE, please install and use IntelliJ IDEA Community Edition (`link <https://www.jetbrains.com/idea/download/#section=windows>`_). In the IDE, please also install the Intellij Scala plugin: in the Settings->Plugins tab, select it from the marketplace: 
  
  .. image:: /images/intellij.png
   :alt: IntelliJ
  
  6. In the IDE, you can now  go to File and Open the root directory of the project repository, “\Sidechains-SDK”. The pom.xml file - the Maven Project Object Model XML file that contains all the project configuration details - should be automatically imported by the IDE. Otherwise, you can just open it.
  7. Keep reading this tutorial, and start playing with the code. You will find a sidechain example in the “examples/simpleapp” directory (`link <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/examples/simpleapp/>`_); you can study the code and experiment with it while reading this documentation.
  8. While fiddling with the code, you might also want to see a sidechain in action, understand its configuration files, look at its interaction with mainchain and its user interface. Best way to do that is to install a local mainchain and sidechain example node (`link <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/examples/simpleapp/mc_sc_workflow_example.md>`_)
  9. When you are comfortable with the SDK core functionalities, you can tackle Chapter 8 and 9, and learn how to extend the software to add your own data and logic. Here the "Lambo Registry" example (`link <https://github.com/HorizenOfficial/lambo-registry>`_) will complement your reading, and show you how to create your own blockchain-based dApp.   
  
*******************
Installing on Linux
*******************

  1. Install Java JDK version 11 (`link <https://www.oracle.com/java/technologies/javase-jdk11-downloads.html>`_)
  2. Install Scala 2.12.10+ (`link <https://www.scala-lang.org/download/2.12.10.html>`_)
  3. Install Git (`link <https://git-scm.com/downloads>`_)
  4. Clone the Sidechains-SDK git repository 
  
  .. code:: Bash
  
     git clone git@github.com:HorizenOfficial/Sidechains-SDK.git
     
  5. As IDE, please install and use IntelliJ IDEA Community Edition (`link <https://www.jetbrains.com/idea/download/#section=linux>`_) In the IDE, please also install the Intellij Scala plugin: in the Settings->Plugins tab, select it from the marketplace: 
  
  .. image:: /images/intellij.png
   :alt: IntelliJ
  
  6. In the IDE, you can now  go to File and Open the root directory of the project repository, “\Sidechains-SDK”. The pom.xml file - the Maven Project Object Model XML file that contains all the project configuration details - should be automatically imported by the IDE. Otherwise, you can just open it.
  7. Keep reading this tutorial, and start playing with the code. You will find a sidechain example in the “examples/simpleapp” directory (`link <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/examples/simpleapp/>`_); you can study the code and experiment with it while reading this documentation.
  8. While fiddling with the code, you might also want to see a sidechain in action, understand its configuration files, look at its interaction with mainchain and its user interface. Best way to do that is to install a local mainchain and sidechain example node (`link <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/examples/simpleapp/mc_sc_workflow_example.md>`_)
  9. When you are comfortable with the SDK core functionalities, you can tackle Chapter 8 and 9, and learn how to extend the software to add your own data and logic. Here the "Lambo Registry" example (`link <https://github.com/HorizenOfficial/lambo-registry>`_) will complement your reading, and show you how to create your own blockchain-based dApp.

   

  



