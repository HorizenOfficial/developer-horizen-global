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

The Sidechain SDK requires Java 8  or newer (Java 11 recommended), Scala 2.12.10+ or newer, and the latest version of `zend_oo <https://github.com/ZencashOfficial/zend_oo>`_.


**********************
Installing on Windows:
**********************

  1. Install Java JDK version 11 (`link <https://www.oracle.com/java/technologies/javase-jdk11-downloads.html>`_)
  2. Install Scala 2.12.10+ (`link <https://www.scala-lang.org/download/2.12.10.html>`_)
  3. Install Git (`link <https://git-scm.com/downloads>`_)
  4. Clone the Sidechains-SDK git repository 

  .. code:: Bash
  
     git clone git@github.com:HorizenOfficial/Sidechains-SDK.git
    
  5. As IDE, please install and use IntelliJ IDEA Community Edition (link). In the IDE, please also install the Intellij Scala plugin: in the Settings->Plugins tab, select it from the marketplace: 
  
  .. image:: /images/intellij.png
   :alt: IntelliJ
  
  6. In the IDE, you can now go to File and Open the root directory of the project repository, “\Sidechains-SDK”. The pom.xml file, the Maven Project's Object Model XML file that contains all the project configuration details, should be automatically imported by the IDE. Otherwise, you can just open it.
  7. Keep reading this tutorial, and start playing with the code. You will find some sidechain examples in the “examples/simpleapp” directory that you can customize. Start from there! When you are ready to run your standalone sidechain, you can install Maven (`link <https://maven.apache.org/install.html>`_).
  8. To produce your specific sidechain .jar files, you can change directory to the repository root and run the “mvn package” command.   
  
*******************
Installing on Linux:
*******************

  1. Install Java JDK version 11 (`link <https://www.oracle.com/java/technologies/javase-jdk11-downloads.html>`_)
  2. Install Scala 2.12.10+ (`link <https://www.scala-lang.org/download/2.12.10.html>`_)
  3. Install Git (`link <https://git-scm.com/downloads>`_)
  4. Clone the Sidechains-SDK git repository 
  
  .. code:: Bash
  
     git clone git@github.com:HorizenOfficial/Sidechains-SDK.git
     
  5. As IDE, please install and use IntelliJ IDEA Community Edition (link). In the IDE, please also install the Intellij Scala plugin: in the Settings->Plugins tab, select it from the marketplace: 
  
  .. image:: /images/intellij.png
   :alt: IntelliJ
  
  6. In the IDE, you can now  go to File and Open the root directory of the project repository, “\Sidechains-SDK”. The pom.xml file - the Maven Project's Object Model XML file that contains all the project configuration details, should be automatically imported by the IDE. Otherwise, you can just open it.
  7. Keep reading this tutorial, and start playing with the code. You will find some sidechain examples in the “examples/simpleapp” directory that you can customize. Start from there! When you are ready to run your own sidechain, you can install Maven (link).
  8. To produce your specific sidechain .jar files, you can change the directory to the repository root and run the “mvn package” command.   
  
  
*************************
Sidechain SDK Components:
*************************

As a result of step 8, three jar files will be generated:
  
  * **sdk/target/Sidechains-SDK-0.2.0.jar** - The main SDK jar file that contains all the necessary classes and components
  * **tools/sctool/target/Sidechains-SDK-ScBootstrappingTools-0.2.0.jar** - An executable bootstrap tool used to create the configuration of the new sidechain. You can find all available commands and examples of usage here
  
  ..  code:: Bash
  
      examples/simpleapp/mc_sc_workflow_example.md;   
      
  * **examples/simpleapp/target/Sidechains-SDK-simpleapp-0.2.0.jar** - A sidechain application example. You can find more details in the examples/simpleapp/readme.md file.

  
*****************************
Sidechain Setup Configuration
*****************************

Check the following `link <https://github.com/HorizenOfficial/Sidechains-SDK/blob/master/examples/simpleapp/mc_sc_workflow_example.md>`_

  



