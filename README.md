# Approval-System
Approval System Based on Threshold Cryptography

## Description ##
This is a multi-user application that demonstrates the use of a (t,n) threshold signature scheme.
The application has been implemented as a client server system with 'n' clients. Every client can do the following:

* Initiate a transaction
* Sign the transaction  
where transaction is an integer.  
Once the threshold number of 't' clients sign the message, the message is approved. 
The BLS signature scheme has been used for the signature part. The implementation has been taken from [here](https://github.com/asonnino/bls).
The client server system was implemented using Python socket programming and multithreading. A basic implementation, referred from [here](https://github.com/chandu333/Simple-python-multithreaded-server-client-chat), formed the basis for the client server system in this project.
## Pre-requisites ##

* Python 2.7
* Socket Programming and MultiThreading modules of Python 2.7
* bls-lib package

## Installation guidelines ##

* Install Python 2.7
* To install bls-lib, please refer [here](https://github.com/asonnino/bls) and http://www.google.fr/ or <http://example.com/>

