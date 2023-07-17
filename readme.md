# Python Polygons API

## Project Overview
The goal of this project is to develop a robust RESTful API to support shuttle companies in providing their services. One of the challenges faced by shuttle companies is the lack of precise location information, such as zip codes or cities they serve. To overcome this challenge, the project aims to introduce a solution that allows shuttle companies to define custom polygons as their service areas. This approach empowers shuttle company staff to independently define and modify their service areas, allowing them to attribute a fixed price to each polygon.

## API Documentation
API Documentation is available at http://18.230.150.109/polygons

## Project Objectives

**1) Build a RESTful API:** Develop an API that enables shuttle companies to interact with the system and manage their service areas efficiently.

**2) Custom Polygon Definition:** Implement a mechanism for shuttle company staff to define custom polygons as their service areas. This flexibility allows them to accurately represent the regions they serve, even in cases where traditional location information is inadequate.

**3) Polygon Modification:** Enable shuttle company owners and administrators to modify the defined polygons as needed. This feature ensures that service areas can be adjusted to reflect changes in business operations or expansion plans.

**4) Pricing for Service Areas:** Associate a fixed price with each defined polygon to provide transparency and clarity to customers. This enables shuttle companies to offer consistent pricing based on the specific service areas they cover.

**5) Scalability and Performance:** Build the API to handle a high volume of requests and ensure fast response times, allowing shuttle companies to retrieve service areas and pricing information swiftly.

**6) Data Security:** Implement robust security measures to protect sensitive information, including authentication and authorization mechanisms to ensure that only authorized users can access and modify the service areas and pricing data.

By achieving these objectives, the RESTful API will empower shuttle companies to overcome the limitations of traditional location information. Shuttle company staff will have the flexibility to define and modify their service areas using custom polygons, enabling precise representation of the regions they serve. Additionally, customers will benefit from transparent and consistent pricing based on these defined polygons.

## Project Description

The project uses a set of technologies to achieve the objectives described above. The following sections provide an overview of the technologies used and the rationale behind each choice.

**Python:** The project uses Python as the primary programming language. Python is a popular choice for building RESTful APIs due to its simplicity, readability, and extensive library support. Additionally, Python is a versatile language that can be used for a wide range of applications, including web development, data science, and machine learning. This versatility makes Python a valuable skill for developers to learn and use in their projects.

**Flask:** The project uses the Flask framework to build the RESTful API. Flask is a lightweight framework that provides the core functionality needed to build a RESTful API. Flask is also highly extensible, allowing developers to add additional functionality as needed. Additionally, Flask is a popular choice for building RESTful APIs due to its simplicity and ease of use.

**AWS DocumentDB:** The project uses AWS DocumentDB as the database for storing service areas and pricing information. AWS DocumentDB is a popular choice for building RESTful APIs due to its scalability and reliability. Additionally, AWS DocumentDB provides a high level of control over the database environment, allowing developers to customize the environment as needed. AWS DocumentDB allows scalling up and down the resources as needed, for example, to handle a high volume of requests. If needed, horizontal scaling can be implemented by adding as many as DocumentDB instances necessary to handle the load. AWS DocumentDB is fully compatible with MongoDB, allowing developers to use the same tools and libraries they are familiar with.

**MongoEngine:** The project uses MongoEngine as the Object-Document Mapper (ODM) for MongoDB. MongoEngine is a popular choice for building RESTful APIs due to its simplicity and ease of use. Additionally, MongoEngine provides a high-level abstraction layer that simplifies the process of interacting with MongoDB. 

**AWS EC2:** The project uses AWS EC2 to host the RESTful API. AWS EC2 is a popular choice for hosting RESTful APIs due to its scalability and reliability. Additionally, AWS EC2 provides a high level of control over the hosting environment, allowing developers to customize the environment as needed. AWS EC2 allows scalling up and down the resources as needed, for example, to handle a high volume of requests. If needed, horizontal scaling can be implemented by adding as many as EC2 instances necessary to handle the load.

**AWS Linux:** The project uses AWS Linux as the operating system for the RESTful API. AWS Linux is a popular choice for hosting RESTful APIs due to its scalability and reliability. Additionally, AWS Linux provides a high level of control over the hosting environment, allowing developers to customize the environment as needed. AWS Linux is based on Red Hat Enterprise Linux (RHEL), which is a popular choice for hosting RESTful APIs due to its stability and reliability. 

**AWS ElastiCache:** The project uses AWS ElastiCache to cache the service areas and pricing information. AWS ElastiCache is a popular choice for caching data due to its scalability and reliability. Additionally, AWS ElastiCache provides a high level of control over the caching environment, allowing developers to customize the environment as needed. AWS ElastiCache allows scalling up and down the resources as needed, for example, to handle a high volume of requests. If needed, horizontal scaling can be implemented by adding as many as ElastiCache instances necessary to handle the load.


