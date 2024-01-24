## RAG Backend with Sanic API

The purpose of this API is really to do two core things:
    - Create embeddings around user data that is end to end encrypted
    - Generate responses for queries around that encrypted data 

## Flow
    - Create embedding on plaintext so that search functionality still works
    - Once you're upserting, encrypt data in metadata field with key you're managing
    - When you query, retrieval works in the same way as normal, but there is a custom postprocessor class that will decrypt the text of each node for the response
    - Query engine responds with raw data


# Privacy Note
This flow will make it easier so that the creators of a certain app don't have access to the raw data and are also in compliance with the the kind of data they are custodying. The real question becomes, if you can somehow not also have to manage the key that is doing the encrpyting, you can have a really defensible claim. (Wallets-as-a-Service flow but on a backend for every user)




