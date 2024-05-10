# RobinApi Framework

**Description:**  
RobinApi Framework is a comprehensive solution designed to facilitate efficient interaction with Large Language Model (LLM) APIs and advanced vector data management. This framework provides robust tools for uploading and storing files in an optimized vector database, allowing users to fully leverage content-based search and retrieval. Users can upload documents via the API, which are then stored in a vector database, enabling them to query for the most similar phrases. Moreover, RobinApi Framework includes dedicated endpoints for complex queries, enabling users to extract valuable insights and conduct in-depth analyses of the stored data. Ideal for developers looking to integrate LLM capabilities into their applications and efficiently manage large volumes of data, RobinApi Framework stands out for its flexibility, scalability, and ease of use.

**Key Features:**

- **LLM API Consumption:** Optimized interfaces for interacting with language models, facilitating integration and real-time response handling.
- **Vector Database File Management:** Efficient file uploading, storage, and management with vector search, perfect for applications requiring fast and accurate access to large volumes of data.
- **Query Endpoints:** Specialized functionalities for asking questions and retrieving responses based on stored data, supporting a wide range of analytical and search queries.
- **High Configurability and Security:** Detailed parameter configuration and advanced security protocols to protect information and ensure performance.



**Descripción:**  
RobinApi Framework es una solución integral diseñada para facilitar la interacción eficiente con APIs de modelos de lenguaje de aprendizaje automático (LLM) y la gestión avanzada de datos vectoriales. Este framework proporciona herramientas robustas para la carga y almacenamiento de archivos en una base de datos vectorial optimizada, permitiendo a los usuarios aprovechar completamente la búsqueda y recuperación de datos basados en contenido. Además, RobinApi Framework incluye endpoints dedicados para realizar consultas complejas, permitiendo a los usuarios extraer información valiosa y realizar análisis profundos sobre los datos almacenados. Ideal para desarrolladores que buscan integrar capacidades de LLM en sus aplicaciones y gestionar grandes volúmenes de datos de manera eficiente, RobinApi Framework se destaca por su flexibilidad, escalabilidad y facilidad de uso.

**Características principales:**

- **Consumo de API de LLM:** Interfaces optimizadas para la interacción con modelos de lenguaje, facilitando la integración y el manejo de respuestas en tiempo real.
- **Gestión de archivos en base de datos vectorial:** Carga, almacenamiento y gestión eficiente de archivos con búsqueda vectorial, ideal para aplicaciones que requieren acceso rápido y preciso a grandes volúmenes de datos.
- **Endpoints para consultas:** Funcionalidades específicas para formular preguntas y obtener respuestas basadas en los datos almacenados, soportando una amplia variedad de consultas analíticas y de búsqueda.
- **Alta configurabilidad y seguridad:** Configuración detallada de parámetros y protocolos de seguridad avanzados para proteger la información y garantizar el rendimiento.



## Example code

### Example Code

**1. Creating a Stream of Responses**

```python
from robin_api import RobinAIClient

# Initialize the client with an API key
client = RobinAIClient(api_key="API_KEY")

### Example Code

**1. Creating a Stream of Responses**


from robin_api import RobinAIClient

# Initialize the client with an API key
client = RobinAIClient(api_key="API_KEY")

# Create a conversation prompt
value = [
    {
        "role": "system",
        "content": "system_prompt"
    },
    {
        "role": "user",
        "content": "Give a hello word in python"
    }
]

# Generate a stream of responses
stream = client.completions.create_stream(
    model="ROBIN_4", 
    conversation=value, 
    max_tokens=512, 
    stream=True, 
    save_response=False, 
    temperature=1
)

# Print each chunk of the streamed response
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

2. Generating a Complete Response 


```python
response = client.completions.create(
    model="ROBIN_4",
    conversation=value, 
    max_tokens=512, 
    stream=True, 
    save_response=False, 
    temperature=1
)

# Print the entire response
print(response.choices[0].delta.content, end="")
```

**Parameters:**

- **model**: Specifies which LLM model to use, e.g., "ROBIN_4".

- **conversation**: An array of messages that form the prompt conversation.

- **max_tokens**: Maximum number of tokens for the response.

- **save_response**: If `False`, does not store the response in persistent storage.

- **temperature**: Controls the randomness of responses; values close to 1 are more diverse.





3. Upload a file from a web URL

```python

folder_information = client.files.upload_file(url="https://arxiv.org/pdf/2302.13971.pdf")

# Example response
{
    "folder": {
        "id": "232f179d-a2f2-42c6-b9b8-3e7ad8f4174e",
        "apiFolderId": "83273a99-f722-4d92-8261-bf6a29735782",
        "createdAt": "2024-05-06T21:06:44.000000Z"
    },
    "file": {
        "id": "7cb7fa8d-30f5-4748-ba6a-b1281398c532",
        "url": "https://arxiv.org/pdf/2302.13971.pdf",
        "tokens": 1200,
        "documentId": "8b1a18bf-43ac-4c5c-abad-1a4c45bbf585",
        "createdAt": "2024-05-06T21:06:44.000000Z"
    }
}

```

**Parameters:**

- **url**:  URL of the document to upload.



4. Finding Similar Sentences in the Folder

```python

similar_sentences = client.files.get_similar_sentences( 
    query = "What are the practical implications of the findings in the document?",
    top = 15,
    api_folder_id = "83273a99-f722-4d92-8261-bf6a29735782",
    similarity_threshold = 0.4 )

```
**Parameters:**

- **query**: Text query to search for similar sentences.

- **top**: Number of top matching sentences to return.

- **api_folder_id**: Unique identifier for the folder where the document is stored.

- **similarity_threshold**: Minimum similarity score required for sentences to be returned.



# Example response
```json
{
    "sentences": [
        {
            "sentence": "and Denny Zhou. 2022. Self-consistency improves\nchain of thought reasoning in language models.\nJason Wei, Yi Tay, Rishi Bommasani, Colin Raffel,\nBarret Zoph, Sebastian Borgeaud, Dani Yogatama,\nMaarten Bosma, Denny Zhou, Donald Metzler, et al.\n2022. Emergent abilities of large language models.\narXiv preprint arXiv:2206.07682 .\nGuillaume Wenzek, Marie-Anne Lachaux, Alexis Con-\nneau, Vishrav Chaudhary, Francisco Guzmán, Ar-\nmand Joulin, and Edouard Grave. 2020. CCNet: Ex-\ntracting high quality monolingual datasets from web\ncrawl data. In Language Resources and Evaluation\nConference .\nCarole-Jean Wu, Ramya Raghavendra, Udit Gupta,\nBilge Acun, Newsha Ardalani, Kiwan Maeng, Glo-\nria Chang, Fiona Aga, Jinshi Huang, Charles Bai,\net al. 2022. Sustainable ai: Environmental implica-\ntions, challenges and opportunities. Proceedings of\nMachine Learning and Systems , 4:795–813.\nRowan Zellers, Ari Holtzman, Yonatan Bisk, Ali\nFarhadi, and Yejin Choi. 2019. Hellaswag: Can a\nmachine really ﬁnish your sentence? arXiv preprint\narXiv:1905.07830 .\nAohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang,\nHanyu Lai, Ming Ding, Zhuoyi Yang, Yifan Xu,\nWendi Zheng, Xiao Xia, Weng Lam Tam, Zixuan\nMa, Yufei Xue, Jidong Zhai, Wenguang Chen, Peng\nZhang, Yuxiao Dong, and Jie Tang. 2022. Glm-\n130b: An open bilingual pre-trained model.\nBiao Zhang and Rico Sennrich. 2019. Root mean\nsquare layer normalization. Advances in Neural In-\nformation Processing Systems , 32.\nSusan Zhang, Stephen Roller, Naman Goyal, Mikel\nArtetxe, Moya Chen, Shuohui Chen, Christopher De-\nwan, Mona Diab, Xian Li, Xi Victoria Lin, et al.\n2022. Opt: Open pre-trained transformer language\nmodels. arXiv preprint arXiv:2205.01068 .",
            "score": 0.4931640625,
            "metadata": {
                "document_id": "83273a99-f722-4d92-8261-bf6a29735782",
                "file_name": "zqA6c.pdf",
                "page_label": "16",
                "source_url": "https://arxiv.org/pdf/2302.13971.pdf"
            }
        },
        {
            "sentence": "7B 13B 33B 65B\nAll 66.0 64.7 69.0 77.5\nher/her/she 65.0 66.7 66.7 78.8\nhis/him/he 60.8 62.5 62.1 72.1\ntheir/them/someone 72.1 65.0 78.3 81.7\nher/her/she ( gotcha ) 64.2 65.8 61.7 75.0\nhis/him/he ( gotcha ) 55.0 55.8 55.8 63.3\nTable 13: WinoGender. Co-reference resolution ac-\ncuracy for the LLaMA models, for different pronouns\n(“her/her/she” and “his/him/he”). We observe that our\nmodels obtain better performance on “their/them/some-\none’ pronouns than on “her/her/she” and “his/him/he’,\nwhich is likely indicative of biases.\nTruthful Truthful*Inf\nGPT-31.3B 0.31 0.19\n6B 0.22 0.19\n175B 0.28 0.25\nLLaMA7B 0.33 0.29\n13B 0.47 0.41\n33B 0.52 0.48\n65B 0.57 0.53\nTable 14: TruthfulQA. We report the fraction of truth-\nful and truthful*informative answers, as scored by spe-\ncially trained models via the OpenAI API. We follow\nthe QA prompt style used in Ouyang et al. (2022), and\nreport the performance of GPT-3 from the same paper.\nIn Table 14, we report the performance of our\nmodels on both questions to measure truthful mod-\nels and the intersection of truthful and informative.\nCompared to GPT-3, our model scores higher in\nboth categories, but the rate of correct answers is\nstill low, showing that our model is likely to hallu-\ncinate incorrect answers.\n6 Carbon footprint\nThe training of our models have consumed a mas-\nsive quantity of energy, responsible for the emis-\nsion of carbon dioxide. We follow the recent liter-\nature on the subject and breakdown both the total\nenergy consumption and the resulting carbon foot-\nprint in Table 15. We follow a formula for Wu et al.\n(2022) to estimate the Watt-hour, Wh, needed to\ntrain a model, as well as the tons of carbon emis-\nsions, tCO 2eq. For the Wh, we use the formula:\nWh =GPU-h×(GPU power consumption )×PUE,where we set the Power Usage Effectiveness (PUE)\nat1.1. The resulting carbon emission depends on\nthe location of the data center used to train the net-\nwork. For instance, BLOOM uses a grid that emits\n0.057 kg CO 2eq/KWh leading to 27 tCO 2eq and\nOPT a grid that emits 0.231 kg CO 2eq/KWh, lead-\ning to 82 tCO 2eq. In this study, we are interested in\ncomparing the cost in carbon emission of training\nof these models if they were trained in the same\ndata center. Hence, we do not take the location\nof data center in consideration, and use, instead,\nthe US national average carbon intensity factor of\n0.385 kg CO 2eq/KWh. This leads to the following\nformula for the tons of carbon emissions:\ntCO2eq=MWh×0.385.\nWe apply the same formula to OPT and BLOOM\nfor fair comparison. For OPT, we assume training\nrequired 34 days on 992 A100-80B (see their logs4).\nFinally, we estimate that we used 2048 A100-80GB\nfor a period of approximately 5 months to develop\nour models. This means that developing these mod-\nels would have cost around 2,638 MWh under our\nassumptions, and a total emission of 1,015 tCO 2eq.\nWe hope that releasing these models will help to\nreduce future carbon emission since the training is\nalready done, and some of the models are relatively\nsmall and can be run on a single GPU.\n7 Related work\nLanguage models are probability distributions\nover sequences of words, tokens or charac-\nters (Shannon, 1948, 1951). This task, often framed\nas next token prediction, has long been considered a\ncore problem in natural language processing (Bahl\net al., 1983; Brown et al., 1990). Because Turing\n(1950) proposed to measure machine intelligence\nby using language through the “imitation game”,\nlanguage modeling has been proposed as a bench-\nmark to measure progress toward artiﬁcial intelli-\ngence (Mahoney, 1999).\nArchitecture. Traditionally, language models\nwere based on n-gram count statistics (Bahl\net al., 1983), and various smoothing techniques\nwere proposed to improve the estimation of rare\nevents (Katz, 1987; Kneser and Ney, 1995). In the\npast two decades, neural networks have been suc-\ncessfully applied to the language modelling task,\n4https://github.com/facebookresearch/metaseq/\ntree/main/projects/OPT/chronicles",
            "score": 0.464111328125,
            "metadata": {
                "document_id": "83273a99-f722-4d92-8261-bf6a29735782",
                "file_name": "zqA6c.pdf",
                "page_label": "10",
                "source_url": "https://arxiv.org/pdf/2302.13971.pdf"
            }
        }
    ]
}
```




5. Getting Context-Based Responses from the Folder

```python
answer = client.files.get_response_similar_sentences(
    model="ROBIN_4",
    max_new_tokens = 200,
    top = 15,
    api_folder_id = "17206d13-594c-4e70-a627-24ad26d1c869",
    similarity_threshold = 0.4,
    conversation=value,
    only_with_context = True)
```


**Parameters:**

- **model**: Specifies the LLM model to use.

- **max_new_tokens**: Maximum number of tokens to generate in the new response.

- **top**: Number of top matches to return.

- **api_folder_id**: Unique identifier for the folder containing the documents.

- **similarity_threshold**: Minimum similarity score required for sentences to be returned.

- **conversation**: An array of messages forming the conversation context.

- **only_with_context**: If `True`, generates a response only if relevant context is found in the folder.



# Example response
print(answer.message.choices[0].message.content)
```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "According to the context provided, LLAMA (sometimes written as LLaMA) refers to a language model. It is compared to other language models such as PaLM and LaMDA in terms of performance on quantitative reasoning datasets and code generation tasks. The specific details about what \"LLAMA\" stands for or its unique characteristics are not provided in the context.",
                "role": "assistant"
            },
            "logprobs": null
        }
    ],
    "created": 1715054099,
    "id": "chatcmpl-782cc59b-7729-4809-a661-4b7e9ba875d8",
    "model": "ROBIN_4",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 76,
        "prompt_tokens": 2915,
        "total_tokens": 2991
    }
}
```


6. Upload Web Page information Function
This function allows uploading information from a web page into the system, storing the relevant data in an organized structure for subsequent analysis and retrieva

```python
folder_information = client.files.upload_web_page_information(
    url="https://web.com/example",
    deep_level=1
)

folder_information = client.files.upload_web_page_information(
    url="https://web.com/example",
    deep_level=1,
    folder_id="112ccd00-3814-4f1e-975d-adsflkj6l"
)


```
**Parameters:**

- **url**: The URL of the web page from which to extract information.

- **deep_level** (optional): The depth level for data extraction. A higher value results in more exhaustive exploration.
  - **Accepted Values**: `1`, `2`, `3`.
  - **Default**: `1`.

- **folder_id** (optional): The folder ID where the extracted information will be stored. If not specified, a new folder will be created.

**Response Structure:**

```python
ApiResponse(
    status_code=200,
    message={
        'folder': {
            'apiFolderId': '112ccd00-3814-4f1e-975d-094974d2b89d',
            'createdAt': '2024-05-09T20:26:55.000000Z'
        },
        'file': {
            'url': 'https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset',
            'tokens': None,
            'documentId': None,
            'createdAt': '2024-05-09T20:29:12.000000Z'
        }
    }
)
```


- **folder**: Contains details about the folder where the web page data is stored.
  - **apiFolderId**: The unique identifier of the folder created or used for storing the extracted information.
  - **createdAt**: The timestamp indicating when the folder was created, in ISO 8601 format.

- **file**: Provides information about the extracted web page.
  - **url**: The URL of the web page that was uploaded for data extraction.
  - **tokens**: This field will be populated once the indexing process is complete, representing the total number of tokens extracted from the web page content.
  - **documentId**: Will be created after indexing, serving as a unique identifier for the document.
  - **createdAt**: The timestamp indicating when the file was created, in ISO 8601 format.




