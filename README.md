# Knowledge Retriever app

## Table of Contents
- [Description](#Description)
- [Workflow](#Workflow)
- [Challenges](#Challenges)
- [Installation](#Installation)

## Description
Designed and implemented a field-specific AI assistant leveraging AWS Bedrock foundation models and Retrieval-Augmented Generation (RAG) techniques. 
This solution provides precise and contextually relevant answers to enterprise queries by combining state-of-the-art language models with an intelligent retrieval mechanism.

Key Features:
 -Document Ingestion Pipeline:
  -Developed a robust pipeline to preprocess and segment documents into semantic data chunks.
  -Stored vector embeddings of these data chunks in Elasticsearch, enabling fast and efficient similarity-based retrieval.
  
-Intelligent Context Retrieval:
  -Integrated K-Nearest Neighbors (KNN) search to fetch relevant context from the vector database.
  -Enhanced the AI assistant's responses by augmenting prompts with retrieved context, ensuring high relevance and accuracy.

-Foundation Model Integration:
  -Utilized AWS Bedrock to deliver advanced natural language understanding and response generation.
  -Seamlessly combined large language model capabilities with RAG to address specific enterprise needs.

-Django Server with RESTful Endpoints to:
  -Push documents into the knowledge base.
  -Submit prompts for context-enriched responses.
  -Ensured a scalable and user-friendly API interface for smooth integration with enterprise workflows.

-Containerized Services:
  -Used Docker Compose to containerize and manage the Elasticsearch service, ensuring a streamlined and reproducible deployment process.
  -Simplified development, testing, and scaling with a fully containerized stack.

This AI assistant empowers enterprises to unlock the full potential of their knowledge base by delivering fast, accurate, and context-aware answers, 
improving decision-making and operational efficiency. Its modular architecture, powered by scalable and containerized services, 
ensures adaptability to diverse enterprise environments.


## Workflow
- Used an AWS Bedrock model to implement a domain specific AI assistant.
- Knowledge documents can be ingested into a pipeline which are divided into semantic chunks and stored as vector embeddings in a vector database.
- Another AWS Bedrock model is used to generate these vector embeddings.
- ElasticSearch is used as a vector database.
- When a user asks a prompt, vector embeddings are generated for that prompt and context is searched in vector database using KNN similarity.
- The context is passed along with the prompt to Bedrock model to generate an accurate response.


## Challenges
- For small size documents, they can be easily converted into vector embeddings and stored in vector database. However, for large documents we need to
  divide them into smaller chunks and and the store in database. The challenge is to choose the right size of chunk in which document will be divided.
  Smaller chunk sizes can improve retrieval speed and reduce computational overhead, but they may lack sufficient context for the model to generate coherent
  and relevant responses. Larger chunk sizes provide more context, but can be computationally expensive and may introduce noise or irrelevant information.
  ![ChunkSizeTradeoff_NOPROCESS_](https://github.com/user-attachments/assets/95f74405-7e27-4646-a34c-28090945c709)

- Choosing the right embedding model: The size of the embedding vectors directly impacts the computational requirements and the ability to capture semantic
  information. Larger embeddings (e.g., 1024 dimensions) tend to encode more semantic nuances but demand higher computational resources. Smaller embeddings
  (e.g., 100 dimensions) are more efficient but may sacrifice some semantic richness.

- An AI assistant does not hold state, so if there are follow up questions based on previous responses it might not perform well. Many FMs have a limited context window,
  which means you can only pass a fixed length of data as input. Storing state information in a multiple-turn conversation becomes a problem when the conversation exceeds
  the context window.








