Hi! Welcome to your lab environment.
##Abstract
Discover how to orchestrate **multi agents** for intelligent, context-aware data retrieval and leverage **Azure OpenAI's** API with Transformer models for seamless integration of **multimodal** and collaborative AI systems. It features automated deployment and ingestion of multimodal content, **AI semantic search**, smart chunking, and support for cutting-edge embedding models to enable precise, scalable, and context-aware information retrieval.

This lab is divided into **3 components**:
1. Basic **Infrastructure** Setup : Azure + Local
1. Coding and understanding **Multi-Agent Multimodal** setup
1. Deploy a **Multimodal Multi-Agent RAG** application to Azure + Understanding the architecture and common use-cases 

# Exercise 1 : Azure and Local Infrastructure Setup
>[+] Step 1: Launch and Login to Azure Portal
>1. Open the **Resources** tab next to instructions at the top of your screen to get the **credentials**.
>1. **Sign in** to the **VM** using the machine credentials.
>1. Open a web **browser**.
>2. **Navigate** to **Azure Portal** by writing this url in the address bar.<br>
> ++++https://portal.azure.com++++.
>4. Enter the provided **username** from the resources tab and click **Next**.
>5. Enter the **password** from the **resources tab** and click **Sign in**. 

>[+] Step 2: Access Azure OpenAI Studio
>1. In the Azure portal, search for **Azure OpenAI** in the search bar.
>2. Inside Azure Open AI, Click on **Create**. 
>3. Select resource group as **RG_Lab710**, **provide** an instance **name**, select **Standard S0** Pricing tier. Click on Next until the last tab.
>4. Click on **Create**, Wait for the deployment to complete.
>5. Click on Go to Resource. Click on **Go to Azure AI Foundry Portal**.<br>
>!IMAGE[ltn888o8.jpg](instructions281451/ltn888o8.jpg)
>6. If you see an authorization warning at the top just refresh the page in a few seconds.<br>
>!IMAGE[ojpypy31.jpg](instructions281451/ojpypy31.jpg)

>[+] Step 3: Deploy GPT-4 Model
>1. Click on **Deployments** under **Shared Resources** in the Azure OpenAI Studio.<br>
!IMAGE[xgkk7e0b.jpg](instructions281451/xgkk7e0b.jpg)
>2. Click the **+ Deploy model** button, Select Deploy base model.<br>
>!IMAGE[8c85kyex.jpg](instructions281451/8c85kyex.jpg)
>3. Select **GPT-4** from the list of available models.
>4. Provide ++++gpt-4++++ as the name for your deployment. Deployment type should be **Global Standard**. <br> 
!IMAGE[u04qb17h.jpg](instructions281451/u04qb17h.jpg)
>5. Click **Deploy** to deploy the **GPT-4** model.
>## Note: Wait for the deployment process to complete before proceeding.

>[+] Step 4: Deploy DALL-E-3 Model
>1. In the same **Deployments** section, click the **+ Deploy model** button again, Select Deploy base model.
>2. Select **DALL-E-3** from the list of available models.
>3. Provide ++++dall-e-3++++ as the name for your deployment. Deployment type should be **standard**. <br>
!IMAGE[6yfp7x0z.jpg](instructions281451/6yfp7x0z.jpg)
>4. Click **Deploy** to deploy the **DALL-E-3** model.
>
>## Note: Ensure that both deployments are completed successfully. Also, if you have entered a different model name apart from gpt-4 or dall-e-3, please update the same in OAI_Config_List.json file. 

>[+] Step 5: Retrieve API Details
> 1. Click on **Deployments** Tab from the left menu.<br>
!IMAGE[0mpnwg03.jpg](instructions281451/0mpnwg03.jpg)
> 1. Click on **gpt-4**. <br>
!IMAGE[zpjcwyzt.jpg](instructions281451/zpjcwyzt.jpg)
> 1. Scroll a bit down till you see Target URI and KEY.
> 1. **Copy** the following information:
>   - **Key**: Click on copy button against the key as mentioned in the screenshot.
>   - **Target URI**: Note the endpoint URL, you need to copy only the first part of the URI till azure.com (e.g., `https://<your-service-name>.openai.azure.com`).<br>
>    !IMAGE[y72ifieb.jpg](instructions281451/y72ifieb.jpg)
> ## Note: **Key** and **Target URI** are same for both the deployments(gpt-4 and dall-e-3).


>[+] Step 6:  Update the `OAI_Config_List.json`
>1. Open **Visual Studio Code**, open **LabExercise** folder present on the **desktop**. 
Folder structure of your solution should look similar to this :<br>
>!IMAGE[8ggku5yg.jpg](instructions281451/8ggku5yg.jpg)
>1. Open the file **`OAI_Config_List.json`** from VS code explorer.
>2. **Update** the file with the copied values:<br>
>   ```json-linenums
>   [
>      {
>        "model": "gpt-4",
>        "api_type": "azure",
>        "api_key": "<Your Azure Open AI API Key>",
>        "base_url": "<Your Azure Open AI Target URI>",
>        "api_version": "2024-08-01-preview",
>        "tags": ["gpt-4", "azureopenai", "Compact-Model", "Advanced-Language", "High-Performance"]
>      },
>      {
>        "model": "dall-e-3",
>        "api_type": "azure",
>        "api_key": "<Your Azure Open AI API Key>",
>        "base_url": "<Your Azure Open AI Target URI>",
>        "api_version": "2024-02-01",
>        "tags": ["dall-e-3", "azureopenai", "Image-Generation", "Creative-AI"]
>      }
>   ]
>   ```
>3. **Save** the file.

>[+] Step 7: Local Machine Setup
>1. Open **Terminal**<br>
>!IMAGE[dlbl63oy.jpg](instructions281451/dlbl63oy.jpg)
>1. **Type** the following commands and press **Enter** after each command:<br>
>a. Create a new **virtual environment** <br>
>    ++++python -m venv .venv++++<br>
>b. Click **Yes** on the environment prompt if it pops up.<br>
!IMAGE[mq220mwc.jpg](instructions281451/mq220mwc.jpg)<br>
>c. **Activate** the created virtual environment <br>
>    ++++.venv\Scripts\activate++++<br>
>!IMAGE[hxg6ih61.jpg](instructions281451/hxg6ih61.jpg)<br>
>d. **Install** the required modules using requirements.txt file<br>
>    ++++pip  install --no-cache-dir -r requirements.txt++++<br>
>    !IMAGE[mcr852y3.jpg](instructions281451/mcr852y3.jpg)
>2. Open **LabCode.ipynb** file from VS solution explorer.<br>
>!IMAGE[a5zufuvc.jpg](instructions281451/a5zufuvc.jpg)
>2. Click on **Select Kernel** on the top right.<br>
>!IMAGE[2xmohshf.jpg](instructions281451/2xmohshf.jpg)
>3. Click on **Install/Enable suggested extensions** and wait for the installation to complete.
>4. Select **python environments** then choose .venv(3.11.5).<br>
>!IMAGE[10hhiji8.jpg](instructions281451/10hhiji8.jpg)
>5. Click on **Allow** button to complete the local machine setup for this exercise.<br>
>!IMAGE[gy0ew0wh.jpg](instructions281451/gy0ew0wh.jpg)


# Exercise 2 : Coding and understanding Multi-Agent Multimodal setup
In this exercise we will learn how to code multi-agent, multi-modal solution and run it locally.
>[+] Step 1: Configuration import for models
>1. Open **LabCode.ipynb** file in VS code.
>2. Assign the **configuration** to the respective config variables by copy and pasting the code below in the placeholder provided.
>```python-linenums
>llm_config_dalle3 = {"config_list": config_list_dalle3, "timeout": 60, "temperature": 0.7, "seed": 5678}
>llm_config_gpt4 = {"config_list": config_list_gpt4, "timeout": 60, "temperature": 0.7, "seed": 5678}
>```

>[+] Step 2: Initialize the User Proxy Agent - Boss
>1. In this step, you will **initialize** the **boss** agent required for the travel itinerary. The Boss agent is a UserProxyAgent that represents the user requesting a Seattle outing plan in February.
>
>Copy and paste the following code.
>```python-linenums
>boss = UserProxyAgent(
>name="Boss",
>is_termination_msg=termination_msg,
>human_input_mode="ALWAYS",
>code_execution_config=False,
>default_auto_reply="Reply `TERMINATE` if the task is done.",
>description="User requesting a Seattle outing plan in February."
>)
> ```

>[+] Step 3: Give the system message for planner agent

1. The **Tour_Planner_Agent** is an AssistantAgent specializing in creating personalized travel itineraries. It provides tailored recommendations based on user preferences, budget, and travel dates.

    Copy and paste the following code.
    ````    
    system_message = """ You are a smart, personable, and proactive Tour Planner Agent specializing in creating personalized travel itineraries and experiences for users. Your primary goal is to provide tailored recommendations for destinations, accommodations, local attractions, restaurants, and transportation options based on the user preferences, budget, and travel dates. Use the following guidelines to assist users effectively:


    Ask for user preferences such as travel style (e.g., adventure, luxury, budget-friendly), favorite activities, or special interests (history, nature, culture, etc.).
    Consider weather, local events, and safety advisories when making recommendations.
    Destination Knowledge:

    Provide relevant information about destinations, including must-visit attractions, hidden gems, and local customs.
    Suggest best times to visit based on seasons, festivals, or unique experiences.
    Travel Planning:

    Help create detailed itineraries with activity suggestions, transit times, and tips for efficient travel.
    Offer options for transportation (car rentals, public transport), lodging (hotels, homestays), and dining.
    Budget and Deals:

    Recommend cost-effective options or luxury upgrades based on the user budget.
    Share insights on travel packages, discounts, or local savings cards where applicable.
    Contextual Awareness:

    If the user mentions specific travel constraints or goals (e.g., eco-friendly travel, solo trips, family-friendly), incorporate them into suggestions.
    Engagement:

    Use a friendly, conversational tone to build excitement and maintain a helpful demeanor.
    Clarify any questions and follow up with personalized solutions or refined plans as needed.
    Examples of user inquiries you should handle:

    "Plan a 7-day adventure trip to New Zealand for under $3,000."
    "Recommend family-friendly activities in Paris in April."
    "Suggest a luxury honeymoon itinerary for 10 days in Greece."
    Remember, your mission is to make trip planning stress-free, engaging, and uniquely tailored to every traveler’s dream journey. Enjoy planning the perfect travel experience!""",
    ````
>[+] Step 4: Give the system message for Local_Tourist_Guide agent

1. The **Local_Tourist_Guide** is an AssistantAgent focused on providing detailed, context-aware recommendations for Seattle. It assists the Tour Planner Agent by offering insights into local attractions, events, and culture.

    Copy and paste the following code.
    ````    
    system_message="""
    You are a knowledgeable, personable, and insightful Local Tourist Guide Agent for the city of Seattle, Washington. Your role is to provide detailed, context-aware recommendations and insights to assist the Tour Planner Agent in creating perfect travel experiences for users. Your expertise spans both the rich history and the current attractions of Seattle, ensuring that suggestions are relevant, seasonally appropriate, and tailored to visitor interests.

    Seattle-Specific Expertise:

    Share knowledge of popular attractions like Pike Place Market, Space Needle, Chihuly    Garden and Glass, and hidden gems such as local street art tours or unique coffee shops.
    Include seasonal highlights like the Cherry Blossom Festival in spring, Seafair events in summer, fall foliage tours, or holiday markets in winter.
    Offer insights into historical landmarks such as Pioneer Square, Klondike Gold Rush Museum, and Seattle Underground.
    Monthly and Seasonal Recommendations:

    Suggest best months for visiting based on weather, activities, and events.
    Example:
    April-May: Ideal for cherry blossoms and mild weather.
    July-September: Best for outdoor activities, festivals, and clear views of Mount Rainier.
    December: Highlight winter markets, holiday lights, and indoor attractions.
    Mention any potential seasonal challenges, such as rainy winters or peak tourist seasons, and provide tips to navigate them.
    Current Events and Conditions:

    Include updates on local events, festivals, and temporary exhibits or attractions.
    Share insights into current travel conditions, such as traffic congestion, construction, or transit improvements.
    Local Culture and Food:

    Recommend iconic foods to try (like salmon, clam chowder, or coffee culture).
    Suggest neighborhoods to explore for dining, art, and culture (e.g., Ballard for seafood, Capitol Hill for nightlife, Fremont for quirky attractions).
    Collaboration with Planner Agent:

    Provide precise, context-aware suggestions to enhance itineraries, ensuring alignment with the traveler’s interests, budget, and timeline.
    Example response to a query:
    “For a trip in July, I recommend adding a visit to Discovery Park for sunset views, kayaking on Lake Union, and enjoying the Ballard SeafoodFest. These activities showcase Seattle summer beauty while offering unique local experiences.”
    """,
    ````
>[+] Note: No changes required in the code blocks which are marked as **No action required**, just observe and proceed to Step 5.

>[+] Step 5: Group chat Initialization
>1. Initialize the **group chat among boss, planner and tourist guide, prompt and dalle agent**. Copy and paste the following code into your notebook.
>```python-linenums
>     groupchat = autogen.GroupChat(
>        agents=[boss, planner,localtourist_Guide, prompt_agent, dalle_agent],
>        messages=[preferences_message],
>        max_round=12,
>        speaker_selection_method="auto",
>        allow_repeat_speaker=True,
>        send_introductions=True,
>        select_speaker_auto_verbose=True,   
>    )
>```
>#### Please Note : Make sure the indentation is proper, it should align with the preferences_message variable, there should be no red underline warnings in the entire code.

>[+] Step 6: Run the code
>1. Click on **Run All**, select **Install/Allow** if prompted during the run.<br>
>!IMAGE[01snmrxl.jpg](instructions281451/01snmrxl.jpg)
>1. Click on **Install** if prompted and wait for the installation to get completed.<br>
!IMAGE[4zcjqxpk.jpg](instructions281451/4zcjqxpk.jpg)
>1. Close the **Terminal Window**.
!IMAGE[9eo4ud3f.jpg](instructions281451/9eo4ud3f.jpg)
>2. **Observe** the **output** at the **bottom** of your jupyter **notebook**.<br>
>!IMAGE[ptk5z1n2.jpg](instructions281451/ptk5z1n2.jpg)
>4. **Scroll** to the **output section** at the **bottom** of your jupyter **notebook**, click on **scrollable element**<br>
!IMAGE[3x6g8jnh.jpg](instructions281451/3x6g8jnh.jpg)
>3. **Try** the **prompt** below for example and press **Enter**<br>
>++++Can you generate an illustartion for my itinerary++++ <br>
>++++I am more interested in visiting the space needle during a snowfall, please generate an illustration for the same++++<br>
!IMAGE[qf1j7f2y.jpg](instructions281451/qf1j7f2y.jpg)
>4. Observe the output and see how the below **agents coordinate** with each other to create an itinerary for you as well generate an illustration for the same.<br>
>4. **Scroll** to the **output section** at the **bottom** of your jupyter **notebook**, click on **scrollable element**<br>
!IMAGE[3x6g8jnh.jpg](instructions281451/3x6g8jnh.jpg)
>4. **Images generated** by **dalle agent** will be visible in the **output section** as well as in the **images folder**<br>
!IMAGE[5nxel6z6.jpg](instructions281451/5nxel6z6.jpg)
>5. Type **exit** and press **Enter** to end the chat.<br>
>!IMAGE[a9yy90hd.jpg](instructions281451/a9yy90hd.jpg)
>| **Agent** | **Autogen Agent Type** | **Description** |<br>
>|:--------:|:--------:|:--------:|<br>
>
>| BOSS   | UserProxyAgent   | User agent who provides the inputs and queries|
>| Travel Planner   | AssistantAgent   | Provides personalized itineraries, booking recommendations, cost optimization, and real-time travel insights|
>|Local Tourist Guide | AssistantAgent | Provides personalized recommendations, historical insights, hidden gems, and real-time navigation tips to enhance the traveler’s experience in Seattle location|
>|Prompt Agent | AssistantAgent| Creates a Image Generation Prompt for the itinerary created by Travel Planner and Local Tourist Guide |
>|Dalle Image Creation Agent| ConversableAgent | Generates Images based on the prompt created by Prompt Agent |
><br>


#####**Conclusion**
**Congratulations!** You have completed this exercise. In this exercise, you learned how to set up and use autogen agents to create a travel itinerary for Seattle in February. Make sure to save your work and review the concepts covered.

# Exercise 3 (Optional): Deploy a Multimodal Multi-Agent application to Azure
In this exercise we will deploy an application to azure which will help us better understand a multimodal, multi-agentic setup.
>[+] Step 1: Run the deployment script
>1. In a **browser TAB** open this link and sign in if required.<br> ++https://portal.azure.com/?feature.customportal=false#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkzkalra%2FRAGPublic%2FTCUpdates%2Fdeployment%2Finfra-as-code-public%2Fbicep%2Fmain-1click.json++<br>
>2. Select **RG_Lab710** as the resource group from the dropdown. Do not modify anything else.<br>
!IMAGE[yzho2ple.jpg](instructions281451/yzho2ple.jpg)
>3. Click on **Next**, Review and **Create**.<br>
!IMAGE[9wvrpeg9.jpg](instructions281451/9wvrpeg9.jpg)
>4. Deployment will take approximately 5-10 mins to get completed. Meanwhile you can continue with Step 2: Understanding of the solution.

>[+] Step 2: Understanding the solution
>- The following are technical features implemented as part of this solution:
>1. Supported file formats are PDFs, MS Word documents, MS Excel sheets, and csv files. 
>1. Ingestion of multimodal documents including images and tables
>1. Full deployment script that will create the solution components on Azure and build the docker images for the web apps
>1. Hybrid search with AI Search using vector and keyword search, and semantic re-ranker
>1. Extraction of chunk-level tags and whole-document-level chunks to optimize keyword search
>1. Whole document summaries used as part of the final search prompt to give extra context 
>1. Code Execution with the OpenAI Assistants API Code Interpreter
>1. Tag-based Search for optimizing really long user query, e.g. Generation Prompts
>1. Modular and easy-to-use interface with Processors for customizable processing pipelines
>1. Smart chunking of Markdown tables with repeatable header and table summary in every chunk
>
>### The Concept of Processing Pipelines and Processors
>
>For the sake of providing an extendable modular architecture, we have implemented in this accelerator the concept of a processing pipeline, where each document undergoes a pre-specified number of processing steps, each step adding some degree of change to the documents. Processors are format-specific (e.g. PDF, MS Word, Excel, etc..), and are created to ingest multimodal documents in the most efficient way for that format. Therefore the list of processing steps for a PDF is different than the list of steps for an Excel sheet. 
>
>At the start of the processing pipeline, a Python dictionary variable called `ingestion_pipeline_dict` with all the input parameters is created in the constructor of the Processor and then passed to the first step. The step will do its own processing, will change variables inside the `ingestion_pipeline_dict` and will add new ones. The `ingestion_pipeline_dict` is then returned by this first step, and will then become the input for the second step. This way, the `ingestion_pipeline_dict` is passed from each step to the next downstream the pipeline. It is the common context which all steps work on. The `ingestion_pipeline_dict` is saved in a text file at the end of each step, so as to provide a way for debugging and troubleshooting under the processing folder name in the `stages` directory.
>The below JSON block describes the processing pipelines per document format per processing option: 
<br/>
>```json
{
    ".pdf": {
        "gpt-4-vision": [
            "create_pdf_chunks", "pdf_extract_high_res_chunk_images", "pdf_extract_text", "pdf_extract_images", "delete_pdf_chunks", "post_process_images", "extract_tables_from_images", "post_process_tables", "generate_tags_for_all_chunks", "generate_document_wide_tags", "generate_document_wide_summary", "generate_analysis_for_text"
        ],
        "document-intelligence": [
            "create_pdf_chunks", "pdf_extract_high_res_chunk_images", "pdf_extract_text", "pdf_extract_images", "delete_pdf_chunks", "extract_doc_using_doc_int", "create_doc_chunks_with_doc_int_markdown", "post_process_images", "generate_tags_for_all_chunks", "generate_document_wide_tags", "generate_document_wide_summary", "generate_analysis_for_text"
        ],
        "hybrid": [
            "create_pdf_chunks", "pdf_extract_high_res_chunk_images", "delete_pdf_chunks", "extract_doc_using_doc_int", "create_doc_chunks_with_doc_int_markdown", "post_process_images", "post_process_tables", "generate_tags_for_all_chunks", "generate_document_wide_tags", "generate_document_wide_summary", "generate_analysis_for_text"
        ]
    },
    ".docx": {
        "py-docx": [
            "extract_docx_using_py_docx", "create_doc_chunks_with_doc_int_markdown", "post_process_images", "generate_tags_for_all_chunks", "generate_document_wide_tags", "generate_document_wide_summary", "generate_analysis_for_text"
        ],
        "document-intelligence": [
            "extract_doc_using_doc_int", "create_doc_chunks_with_doc_int_markdown", "post_process_images", "generate_tags_for_all_chunks", "generate_document_wide_tags", "generate_document_wide_summary", "generate_analysis_for_text"
        ]
    },
    ".xlsx": {
        "openpyxl": [
            "extract_xlsx_using_openpyxl", "create_table_doc_chunks_markdown", "create_image_doc_chunks", "generate_tags_for_all_chunks", "generate_document_wide_tags", "generate_document_wide_summary", "generate_analysis_for_text"
        ]
    }
}
>```
Here is a visual representation of a pipeline
!IMAGE[pipeline.png](instructions281451/pipeline.png)
<br/>
### Solution Architecture
The below is the high-level logical architecture of this lab solution.
!IMAGE[p10qngl2.jpg](instructions281451/p10qngl2.jpg)
More details on the processing steps is provided towards the end of this manual.

>[+] Step 3: Data Ingestion using Ingestion App
>1. Once the deployment is completed, **open** the resource group - **RG_Lab710**<br>
!IMAGE[zm2yaq53.jpg](instructions281451/zm2yaq53.jpg)
>1. Scroll down in the resources and look for a **container app** with the name **`dev-main-******`**, open it.
>1. Copy the **application URL** and paste it in the **new tab**, open it. Click on the **Ingestion** Tab.<br>
>!IMAGE[212gy1et.jpg](instructions281451/212gy1et.jpg)
>1. Click on **browse files**, select all the 3 files present in **Desktop/TechConnect** files repo.<br>
>!IMAGE[4h4tly1s.jpg](instructions281451/4h4tly1s.jpg)
>1. Click **start Ingestion** at the bottom, wait for a 45-60 seconds and click **refresh**. Observe the status log getting generated. **Wait** till all the 3 files are **ingested successfully**. You can click on Refresh to check the updated status.<br>
>!IMAGE[to1fnhis.jpg](instructions281451/to1fnhis.jpg)
>1. Information related to New York is ingested using a PDF<br>
!IMAGE[diqf4wz1.jpg](instructions281451/diqf4wz1.jpg)
>1. Docx file contains the information related to Bainbridge Island
!IMAGE[17id1dcb.jpg](instructions281451/17id1dcb.jpg)
>1. Excel file contains temperature related information
!IMAGE[zfh2yb9j.jpg](instructions281451/zfh2yb9j.jpg)

>[+] Step 4: Chat with data
>1. Open the resource group **RG_Lab710**, scroll down in the resources and look for a **container app** with the name **`dev-chat-******`**, open it.<br>
!IMAGE[gszpou6l.jpg](instructions281451/gszpou6l.jpg)
>1. Copy the **application URL** and **open** it in a new tab.
>1. Type in your prompt/query in the chatbox and **start chatting** with your data.
For example:<br>
+++Can you generate a New York itinerary for me?+++<br>
+++What do you know about Bainbridge+++<br>
+++Tell me something about India's climate in February+++
>1. Expand the dropdown near the chat prompt and the result to observe how your query is getting processed.<br>
!IMAGE[mz706j2i.jpg](instructions281451/mz706j2i.jpg)


## Conculsion
**Congratulations!** You have completed this exercise. This excercise is built on one of the official [Azure Samples](https://github.com/Azure-Samples/multimodal-rag-code-execution). In the exercise we understood how these intelligent applications are coded, deployed and a sample of how end users can interact with the application. Here are the potential use cases : 
1. Analyze Investment opportunity documents for Private Equity deals
1. Analyze tables from tax documents for audit purposes
1. Analyze financial statements and perform initial computations
1. Analyze and interact with multi-modal Manufacturing documents 
1. Process academic and research papers
1. Ingest and interact with textbooks, manuals and guides
1. Analyze traffic and city planning documents 

## Feedback
Your feedback is valuable.
Open work browser/ work profile on your mobile and please submit your thoughts about today’s experiences by opening this link **techconnect.microsoft.com/evaluations** or try scanning this QR code.<br>
!IMAGE[ztryo4by.jpg](instructions281451/ztryo4by.jpg)


>[+] Processing Steps Detailed Information
>1. The `create_doc_chunks_with_doc_int_markdown` function is integral to the processing of documents, particularly when utilizing the Document Intelligence service. It's designed to handle the markdown conversion of document chunks, ensuring that the extracted data is formatted correctly for further analysis. This function is applicable to various document formats and is capable of processing text, images, and tables, making it versatile in the multimodal information extraction process. Its role is crucial in structuring the raw extracted data into a more accessible and analyzable form.
>1. The `create_image_doc_chunks` function is integral to the processing of image data within multimodal documents. It specifically targets the extraction and organization of image-related content, segmenting each image as a discrete chunk for further analysis. This function is applicable across various document formats that include image data, playing a crucial role in the multimodal extraction pipeline by ensuring that visual information is accurately captured and prepared for subsequent processing steps such as tagging and analysis. It deals exclusively with the image modality, isolating it from text and tables to streamline the handling of visual content.
>1. The `create_pdf_chunks` function is a crucial step in the document ingestion process, particularly for PDF files. It segments the input PDF document into individual chunks, which are then processed separately in subsequent stages of the pipeline. This function is applicable to all modalities within a PDF document, including text, images, and tables, ensuring a comprehensive breakdown of the document's content for detailed analysis and extraction. Its role is foundational, as it sets the stage for the specialized processing of each modality by other functions in the pipeline.
>1. The function `create_table_doc_chunks_markdown` is responsible for processing tables within documents, specifically converting them into Markdown format. It is applicable to `.xlsx` files as part of the `openpyxl` pipeline. This function not only handles the conversion but also manages the chunking of tables when they are too large, ensuring that the Markdown representation is accurate and manageable. It processes the table modality exclusively and is crucial for preserving the structure and data of tables during the document ingestion process.
>1. The `delete_pdf_chunks` function is a crucial step in the document processing pipeline, particularly for PDF files. It is responsible for removing the temporary storage of PDF chunks from memory, ensuring that the system resources are efficiently managed and not overburdened with unnecessary data. This function is applied after the initial extraction of high-resolution images and text from the PDF document, and before any post-processing of images or tables. It is applicable to all modalities—text, images, and tables—since it deals with the cleanup of data extracted from PDF chunks.
>1. The `extract_doc_using_doc_int` function is a key component in the document processing pipeline, specifically tailored for handling `.docx` and `.pdf` files. It leverages the capabilities of Azure's Document Intelligence Service to analyze and extract structured data, including text and tables, from documents. This function is crucial for converting document content into a format that can be further processed for insights and is versatile in dealing with both textual and tabular data modalities.
>1. The `extract_docx_using_py_docx` function is designed to handle the extraction of content from `.docx` files, specifically focusing on text, images, and tables. It utilizes the `python-docx` library to access and extract these elements, ensuring that the data is accurately retrieved and stored in a structured format suitable for further processing. This function is crucial for the initial stage of the ingestion pipeline, setting the foundation for subsequent analysis and processing steps. It is applicable to `.docx` files and is responsible for extracting all three modalities: text, images, and tables, from the document.
>1. The `extract_tables_from_images` function is designed to identify and extract tables from image files within a document. It applies to image modalities, specifically targeting visual data representations such as tables embedded within image files. This function is crucial for converting visual table data into a structured format that can be further processed or analyzed, making it an essential step in multimodal document processing pipelines that deal with both textual and visual information. It is particularly relevant for documents where tabular information is presented in non-textual formats.
>1. The `extract_xlsx_using_openpyxl` function is designed to handle the extraction of data from `.xlsx` files, specifically focusing on the retrieval of tables and their conversion into various formats for further processing. It leverages the `openpyxl` library to access and manipulate Excel files, ensuring that the extracted data is accurately represented in Python-friendly structures such as DataFrames. This function is crucial for parsing spreadsheet data, which is often rich in structured information, making it a key step in the data extraction phase for `.xlsx` files within the ingestion pipeline. It processes the table modality, transforming Excel sheets into Markdown, plain text, and Python scripts, which can then be integrated into the multimodal information extraction framework.
>1. The `generate_analysis_for_text` function is designed to analyze the relationship between a specific text chunk and the overall content of a document. It highlights entity relationships introduced or extended in the text chunk, providing a concise analysis that adds context to the document's topics. This function is applicable to all modalities—text, images, and tables—ensuring a comprehensive understanding of the document's content. It plays a crucial role in enhancing the document's metadata by providing insights into the significance of each section within the larger document structure.
>1. The `generate_document_wide_summary` function is responsible for creating a concise summary of the entire document's content. It extracts key information and presents it in a few paragraphs, ensuring that the essence of the document is captured without unnecessary details. This function is applicable to all document formats, including text, images, and tables, making it a versatile component in the multimodal information extraction pipeline. It plays a crucial role in providing a quick overview of the document, which can be beneficial for both indexing and search purposes.
>1. The `generate_document_wide_tags` function is a crucial component in the document ingestion pipeline, applicable across various document formats including PDF, DOCX, and XLSX. It is responsible for extracting key tags from the entire document, which are essential for enhancing search and retrieval capabilities. This function processes text modality, ensuring that significant entities and topics within the document are captured as tags, aiding in the creation of a searchable index for the ingested content.
>1. The `generate_tags_for_all_chunks` function is integral to the multimodal information extraction process, applicable across various document formats including PDF, DOCX, and XLSX. It operates on all three modalities—text, images, and tables—extracting and optimizing tags for enhanced search and retrieval within a vector store. This function ensures that each chunk of the document, regardless of its content type, is accurately represented by a set of descriptive tags, facilitating efficient indexing and subsequent search operations.
>1. The `pdf_extract_high_res_chunk_images` function is responsible for extracting high-resolution images from each chunk of a PDF document. It plays a crucial role in the initial stages of the document processing pipeline, particularly for PDF formats, ensuring that visual data is captured in detail for subsequent analysis. This function focuses on the image modality, converting document chunks into PNG images at a DPI of 300, which are then used for further image-based processing tasks.
>1. The `pdf_extract_images` function is designed to handle the extraction of images from PDF documents. It is applicable to PDF formats and operates within a multimodal extraction context, where it specifically processes the image modality. This function plays a crucial role in isolating visual content from PDFs, which is essential for subsequent image analysis and understanding in the broader multimodal information extraction process.
>1. The `pdf_extract_text` function is a crucial component in the document processing pipeline, specifically tailored for handling PDF files. It is responsible for extracting textual content from each page of a PDF document, converting it into a machine-readable format. This function is pivotal for subsequent stages that may involve text analysis, search indexing, or further data extraction tasks. It operates solely on the text modality, ensuring that the rich textual information embedded within PDFs is accurately captured and made available for downstream processing.
>1. The `post_process_images` function is integral to refining the output from image extraction operations within the document ingestion process. It specifically handles the enhancement and clarification of images, ensuring that any visual data is accurately represented and usable for subsequent analysis. This function is applicable across various document formats that include image content, playing a pivotal role in multimodal information extraction where visual data is a key component. It is designed to work with images as a modality, complementing other functions that handle text and tables.
>1. The `post_process_tables` function is designed to handle the refinement of table data extracted from documents. It applies to various document formats, including PDFs and images, where tables are present. The function's role is to enhance the quality of the extracted table information, ensuring that it is accurately represented and formatted for further use. It specifically deals with the 'table' modality, focusing on the post-extraction processing of tables to prepare them for integration into a searchable vector index or for analytical computations.

## Thanking you, 
Lab Team



