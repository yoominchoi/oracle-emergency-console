# loadShooterDesc Function


```python
import os

def loadShooterDesc(directory_path):
   shooter_desc = {}
   
   for filename in os.listdir(directory_path):
      if filename.endswith(".txt"):  # assuming shooter_desc are in .txt files
         file_path = os.path.join(directory_path, filename)

         with open(file_path) as f:
            raw_shooter_desc = f.read()

         filename_without_ext = os.path.splitext(filename)[0]  # remove .txt extension
         shooter_desc[filename_without_ext] = [text.strip() for text in raw_shooter_desc.split('=====')]

   return shooter_desc

```


```python
shooter_desc = loadShooterDesc('.')
shooter_desc
```




    {'shooter_desc (4)': ["These are descriptions of a shooter or shooters.\nBlue Cap\nwearing sunglasses\nIt's a guy.\nWearing black jacket\nhas a gun"]}




```python
docs = [{'text': filename + ' | ' + section, 'path': filename} for filename, sections in shooter_desc.items() for section in sections]

# Sample the resulting data
docs[:2]
```




    [{'text': "shooter_desc (4) | These are descriptions of a shooter or shooters.\nBlue Cap\nwearing sunglasses\nIt's a guy.\nWearing black jacket\nhas a gun",
      'path': 'shooter_desc (4)'}]




```python
un = "user1"
pw = "yoominchoi1234A"
cs = "localhost/FREEPDB1"
```


```python
import oracledb
connection = oracledb.connect(user=un, password=pw, dsn=cs)
```


```python
table_name = 'shooter_desc'

with connection.cursor() as cursor:
    # Create the table
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id NUMBER PRIMARY KEY,
            payload CLOB CHECK (payload IS JSON),
            vector VECTOR
        )"""
    try:
        cursor.execute(create_table_sql)
    except oracledb.DatabaseError as e:
        raise

    connection.autocommit = True    
```


```python
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer('all-MiniLM-L12-v2')
```

    INFO:sentence_transformers.SentenceTransformer:Use pytorch device_name: cpu
    INFO:sentence_transformers.SentenceTransformer:Load pretrained SentenceTransformer: all-MiniLM-L12-v2



```python
import array

# Define a list to store the data
data = [
    {"id": idx, "vector_source": row['text'], "payload": row}
    for idx, row in enumerate(docs)
]

# Collect all texts for batch encoding
texts = [f"{row['vector_source']}" for row in data]

# Encode all texts in a batch
embeddings = encoder.encode(texts, batch_size=32, show_progress_bar=True)

# Assign the embeddings back to your data structure
for row, embedding in zip(data, embeddings):
    row['vector'] = array.array("f", embedding)
```


    Batches:   0%|          | 0/1 [00:00<?, ?it/s]



```python
import json

with connection.cursor() as cursor:
    # Truncate the table
    cursor.execute(f"truncate table {table_name}")
    prepared_data = [(row['id'], json.dumps(row['payload']), row['vector']) for row in data]

    # Insert the data
    cursor.executemany(
        f"""INSERT INTO {table_name} (id, payload, vector)
            VALUES (:1, :2, :3)""", prepared_data)
    
    connection.commit()
```


```python
with connection.cursor() as cursor:
    # Define the query to select all rows from a table
    query = f"SELECT * FROM {table_name}"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the rows
    for row in rows[:5]:
        print(row)
```

    (0, {'text': "shooter_desc (4) | These are descriptions of a shooter or shooters.\nBlue Cap\nwearing sunglasses\nIt's a guy.\nWearing black jacket\nhas a gun", 'path': 'shooter_desc (4)'}, array('f', [-0.017141368240118027, 0.04507311433553696, -0.05348360911011696, -0.04635532200336456, 0.11879650503396988, 0.029685821384191513, 0.1721850484609604, -0.008428659290075302, -0.09266557544469833, 0.11536173522472382, 0.03890695050358772, -0.0596795491874218, 0.02103598788380623, -0.051024384796619415, 0.03891414403915405, -0.011247022077441216, -0.026512511074543, -0.01963193342089653, 0.04332781955599785, -0.0716574490070343, -0.07306758314371109, -0.06262847781181335, 0.0029959452804178, -0.05905653536319733, -0.05675629898905754, -0.06291121989488602, 0.049255236983299255, -0.011615409515798092, -0.06431914120912552, 0.06185390055179596, 0.09699669480323792, -0.02571626380085945, -0.012552118860185146, -0.042645640671253204, -0.028517138212919235, -0.031332287937402725, 0.010361681692302227, 0.05637604743242264, -0.07599185407161713, -0.04159996658563614, -0.046176664531230927, -0.012086521834135056, 0.03158631548285484, -0.03157791122794151, 0.04000777378678322, 0.0363001748919487, -0.09535608440637589, 0.005995152052491903, -0.0723581463098526, -0.012403246946632862, -0.07243907451629639, -0.04089215397834778, -0.05850476771593094, -0.07964558899402618, -0.007911624386906624, -0.09303326904773712, -0.03614681586623192, 0.008646657690405846, 0.03864768519997597, -0.0569542720913887, -0.027007052674889565, -0.059938814491033554, 0.019238777458667755, 0.0471101775765419, 0.09216123819351196, 0.06441347301006317, -0.04072003439068794, -0.0041089714504778385, 0.05177907273173332, 0.0549372062087059, -0.012556136585772038, 0.03697243332862854, 0.004321285989135504, 0.02990717440843582, -0.07998870313167572, -0.08456067740917206, 0.016240721568465233, -0.03139428794384003, -0.03477662801742554, 0.04640161246061325, -0.05533870309591293, -0.0562114492058754, -0.00974977482110262, 0.020658254623413086, -0.0020341435447335243, -0.04608051851391792, -0.008469835855066776, -0.06553246825933456, -0.059859875589609146, 0.03627639636397362, -0.1274118572473526, 0.1047077476978302, 0.05153694748878479, -0.0643618032336235, 0.015552687458693981, 0.04711705446243286, 0.002862936118617654, 0.07465460151433945, -0.031776539981365204, 0.07352004945278168, -0.019181910902261734, -0.07649659365415573, 0.06538071483373642, -0.024050720036029816, 0.06636665761470795, -0.01520064938813448, 0.012867907993495464, -0.06752528250217438, -0.02271285280585289, -0.03368605673313141, -0.005473005119711161, 0.1065477654337883, 0.014838095754384995, -0.10030002146959305, 0.018155589699745178, -0.10783965140581131, 0.020542791113257408, 0.015000136569142342, -0.03478509932756424, 0.038812533020973206, 0.009821310639381409, 0.08957468718290329, -0.05825597047805786, 0.02794734761118889, 0.012616600841283798, -0.0029755295254290104, 0.03554774075746536, 0.005036700051277876, 0.10126706957817078, 0.061136312782764435, 0.008876726031303406, 0.04929526895284653, 0.038376763463020325, -0.11580778658390045, -0.036036621779203415, -0.044477518647909164, -0.05856996774673462, 0.032212965190410614, 0.039655156433582306, 0.0014092103810980916, -0.04966987669467926, 0.04583154246211052, 0.07014571875333786, 0.04759565368294716, -0.0100482739508152, 0.07138310372829437, -0.07725484669208527, -0.03546895459294319, 0.024895573034882545, 0.022407496348023415, 0.010039005428552628, 0.015119676478207111, 0.07413351535797119, 0.09143013507127762, -0.07096638530492783, 0.021275894716382027, 0.00492002721875906, 0.05994661897420883, -0.00032530579483136535, -0.013446969911456108, 0.045842546969652176, 0.01103658601641655, 0.07954920828342438, -0.08862940222024918, 0.018065281212329865, -0.04433728754520416, 0.02870345115661621, 0.06379242986440659, -0.012856215238571167, 0.04321850836277008, 0.0246021319180727, 0.03479757159948349, -0.04271735996007919, -0.08323828876018524, -0.06766507029533386, 0.011739320121705532, -0.06384342163801193, -0.04695041850209236, -0.0007800071616657078, -0.007385707926005125, 0.01915983110666275, -0.04825450852513313, -0.0005779483471997082, 0.0016655386425554752, 0.03767276927828789, -0.011704693548381329, -0.040787212550640106, 0.056355252861976624, 0.1317724883556366, 0.0015984352212399244, 0.011834954842925072, 0.0001311637315666303, 0.03272145241498947, 0.020093806087970734, 0.033732324838638306, 0.07006022334098816, 0.08739499002695084, 0.024045368656516075, 0.014189235866069794, 0.09229329973459244, 0.08730033040046692, 0.06624568998813629, -0.028035640716552734, 0.08089037239551544, 0.013722633942961693, 0.016728565096855164, 0.0021825856529176235, -0.04662324860692024, -0.041819099336862564, -0.07826176285743713, -0.021366817876696587, 0.03328786417841911, -0.07383821159601212, -0.05875980854034424, 0.0523030050098896, -0.027165263891220093, -0.0021774324122816324, 0.010741254314780235, 0.0015847506001591682, 0.061216097325086594, -0.06547458469867706, 0.0609813928604126, 0.018424056470394135, 7.275347595590224e-33, 0.044492386281490326, 0.01124608051031828, -0.022606175392866135, -0.023186419159173965, -0.02084190957248211, 0.013651162385940552, 0.0006995236617513001, -0.07723454385995865, 0.12059418112039566, -0.04199359565973282, 0.009439883753657341, 0.0807289406657219, 0.0021646409295499325, -0.001699363230727613, 0.020815813913941383, -0.07836153358221054, -0.10360094904899597, -0.026131564751267433, -0.03937757387757301, 0.0690341591835022, 0.03583142161369324, -0.12469624727964401, 0.02812313847243786, -0.025770442560315132, -0.006293769925832748, 0.04825524613261223, 0.10231614857912064, -0.025098714977502823, -0.03586370870471001, 0.013204488903284073, 0.017554208636283875, -0.06223622336983681, -0.03663827106356621, 0.05100861191749573, -0.0282922200858593, -0.026528580114245415, -0.050160009413957596, -0.08433591574430466, 0.09758157283067703, -0.038099247962236404, -0.042698752135038376, -0.0303926020860672, -0.023205257952213287, 0.04233461618423462, 0.012759821489453316, -0.02133788913488388, 0.031065313145518303, 0.019533388316631317, -0.04186216741800308, 0.01605921983718872, -0.04114331677556038, -0.00631619431078434, -0.04704770818352699, -0.015883084386587143, -0.02820361778140068, -0.06250214576721191, -0.1268557757139206, 0.031064508482813835, -0.00975662562996149, 0.024826306849718094, 0.05134162679314613, -0.015979893505573273, -0.06289597600698471, 0.09889189153909683, -0.0002708239189814776, 0.01884823478758335, -0.07903769612312317, -0.04715842008590698, -0.02861316129565239, 0.005306566599756479, 0.005951653700321913, -0.05013812705874443, 0.05088012292981148, 0.07155103236436844, -0.08944295346736908, -0.03108219802379608, -0.04968256875872612, 0.058430179953575134, 0.07274868339300156, 0.02403322234749794, 0.026085836812853813, -0.014496497809886932, -0.013785146176815033, 0.06317555159330368, 0.01186371874064207, 0.0030777824576944113, 0.0649413987994194, 0.005535986740142107, -0.003071463666856289, -0.038874804973602295, -0.008179524913430214, -0.0014101702254265547, 0.03054128773510456, 0.05677580088376999, -0.05898767337203026, 5.351456840028077e-32, -0.015018217265605927, 0.06510082632303238, -0.021378356963396072, -0.034420911222696304, -0.029360374435782433, 0.09467069059610367, -0.035406067967414856, -0.041826535016298294, 0.03211306035518646, -0.05520344898104668, 0.0016891525592654943, -0.05337154492735863, 0.022355882450938225, -0.003478041384369135, -0.04318343475461006, -0.04658179357647896, -0.02081306092441082, -0.009487387724220753, 0.04805457592010498, -0.038722649216651917, 0.01099520642310381, 0.0340229868888855, 0.015572205185890198, 0.11214664578437805, 0.11340078711509705, 0.03330213576555252, 0.014533703215420246, 0.036805469542741776, 0.005227277521044016, 0.12476581335067749, -0.019117280840873718, 0.062464576214551926, 0.07539138197898865, -0.09318281710147858, 0.05917327105998993, 0.03275423124432564, 0.057845521718263626, 0.02131677232682705, 0.044575586915016174, 0.005628091283142567, -0.012712553143501282, -0.06620318442583084, -0.008943500928580761, -0.009347391314804554, -0.033743154257535934, -0.013123832643032074, 0.04315294325351715, -0.015495850704610348, -0.07268623262643814, 0.009660146199166775, 0.010482661426067352, -0.0029331317637115717, -0.021734237670898438, -0.017067870125174522, 0.0020815925672650337, -0.03438621759414673, 0.008275924250483513, 0.0013178900117054582, -0.04716426134109497, -0.0753057450056076, -0.003313707886263728, -0.03248395770788193, -0.05392751470208168, -0.022781938314437866]))


# Vector retrieval and Large Language Model generation
## 1) Vectorize the "question"


```python
topK = 3

sql = f"""select payload, vector_distance(vector, :vector, COSINE) as score
from {table_name}
order by score
fetch approx first {topK} rows only"""
```


```python
question = 'Make a paragraph of a description of the shooter.'
```


```python
with connection.cursor() as cursor:
    embedding = list(encoder.encode(question))
    vector = array.array("f", embedding)
    
    results  = []
    
    for (info, score, ) in cursor.execute(sql, vector=vector):
        text_content = info.read()
        results.append((score, json.loads(text_content)))
```


    Batches:   0%|          | 0/1 [00:00<?, ?it/s]



```python
import pprint
pprint.pp(results)
```

    [(0.4112406205865029,
      {'text': 'shooter_desc (4) | These are descriptions of a shooter or '
               'shooters.\n'
               'Blue Cap\n'
               'wearing sunglasses\n'
               "It's a guy.\n"
               'Wearing black jacket\n'
               'has a gun',
       'path': 'shooter_desc (4)'})]


## 2) Create the LLM prompt


```python
from transformers import LlamaTokenizerFast
import sys

tokenizer = LlamaTokenizerFast.from_pretrained("hf-internal-testing/llama-tokenizer")
tokenizer.model_max_length = sys.maxsize

def truncate_string(string, max_tokens):
    # Tokenize the text and count the tokens
    tokens = tokenizer.encode(string, add_special_tokens=True) 
    # Truncate the tokens to a maximum length
    truncated_tokens = tokens[:max_tokens]
    # transform the tokens back to text
    truncated_text = tokenizer.decode(truncated_tokens)
    return truncated_text
```


```python
# transform docs into a string array using the "paylod" key
docs_as_one_string = "\n=========\n".join([doc["text"] for doc in docs])
docs_truncated = truncate_string(docs_as_one_string, 1000)
```


```python
prompt = f"""\
    <s>[INST] <<SYS>>
    You are a helpful assistant named Oracle chatbot. 
    USE ONLY the sources below and ABSOLUTELY IGNORE any previous knowledge.
    Use Markdown if appropriate.
    Assume the customer is highly technical.
    <</SYS>> [/INST]

    [INST]
    Respond to PRECISELY to this question: "{question}.",  USING ONLY the following information and IGNORING ANY PREVIOUS KNOWLEDGE.
    Include code snippets and commands where necessary.
    NEVER mention the sources, always respond as if you have that knowledge yourself. Do NOT provide warnings or disclaimers.
    =====
    Sources: {docs_truncated}
    =====
    Answer (Three paragraphs, maximum 1000 words each, 90% spartan):
    [/INST]
    """
```

## 3) Call the Generative AI Service LLM


```python
import oci
from oci.generative_ai_inference.models import LlamaLlmInferenceRequest, GenerateTextDetails, OnDemandServingMode


compartment_id = 'ocid1.tenancy.oc1..aaaaaaaaj4ccqe763dizkrcdbs5x7ufvmmojd24mb6utvkymyo4xwxyv3gfa'
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('config', CONFIG_PROFILE)

# Service endpoint
endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

# GenAI client
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
```


```python
generate_text_request = oci.generative_ai_inference.models.LlamaLlmInferenceRequest()

generate_text_request.prompt = prompt
generate_text_request.is_stream = False #SDK doesn't support streaming responses, feature is under development
generate_text_request.maxx_tokens = 1000
generate_text_request.temperature = 0.3
generate_text_request.top_p = 0.7
generate_text_request.frequency_penalty = 0.0

generate_text_detail = oci.generative_ai_inference.models.GenerateTextDetails()
generate_text_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="meta.llama-2-70b-chat")
generate_text_detail.compartment_id = compartment_id
generate_text_detail.inference_request = generate_text_request
```


```python
generate_text_response = generative_ai_inference_client.generate_text(generate_text_detail)
response = generate_text_response.data.inference_response.choices[0].text

print(response.strip())
```

    Based on the information provided, here is a description of the shooter:


## Debugging


```python
import logging

logging.basicConfig(level=logging.INFO)

try:
    generate_text_response = generative_ai_inference_client.generate_text(generate_text_detail)
    response = generate_text_response.data.inference_response.choices[0].text
    logging.info("Full Response: %s", response.strip())
except Exception as e:
    logging.error("Error occurred: %s", str(e))
```

    INFO:root:Full Response: Based on the information provided, here is a description of the shooter:



```python
if response:
    print("Full Response:")
    print(response.strip())
else:
    print("No response received or response is empty.")

```

    Full Response:
    Based on the information provided, here is a description of the shooter:



```python
response_length = len(response.strip())
print(f"Response Length: {response_length}")
print(response.strip())

```

    Response Length: 72
    Based on the information provided, here is a description of the shooter:



```python

```
