from therix.core.data_sources import PDFDataSource
from therix.core.embedding_models import AzureOpenAIEmbedding3SmallEmbeddingModel, OpenAITextAdaEmbeddingModel
from therix.core.inference_models import AzureOpenAIGPT3TurboPreviewInferenceModel, GroqMixtral87bInferenceModel, OpenAIGPT4TurboPreviewInferenceModel
from therix.core.inference_models import AzureOpenAIGPT3TurboPreviewInferenceModel, OpenAIGPT4TurboPreviewInferenceModel
from therix.core.embedding_models import BedrockTitanEmbedding, OpenAITextAdaEmbeddingModel
from therix.core.inference_models import BedrockTextExpressV1, OpenAIGPT4TurboPreviewInferenceModel
from therix.core.pii_filter_config import PIIFilterConfig
from therix.core.pipeline import Pipeline
import sys



# TODO: Init therix with DB details, and license key


## Usage:
# python main.py ad11128d-d2ec-4f7c-8d87-15c1a5dfe1a9 "how does it help in reasoning?"

# if args has pipeline_id, then load the pipeline
## else create new pipeline
if len(sys.argv) > 1:
    pipeline = Pipeline.from_id(sys.argv[1])
    question = sys.argv[2]
    ans = pipeline.invoke(question)
    print(ans)
else:
    pipeline = Pipeline(name="My New Published Pipeline")
    (pipeline
    .add(PDFDataSource(config={'files': ['./test-data/Essay-on-Lata-Mangeshkar-final.pdf']}))
    .add(OpenAITextAdaEmbeddingModel(config={'api_key': OPENAI_API_KEY}))
    .add(OpenAIGPT4TurboPreviewInferenceModel(config={'api_key': OPENAI_API_KEY}))
    .add(PIIFilterConfig(config={
        'entities': ['PERSON','PHONE_NUMBER','EMAIL_ADDRESS']
    }))
    .save())

    pipeline.publish()
    pipeline.preprocess_data()
    print(pipeline.id)
    ans = pipeline.invoke("Whom is the data about? And what are their personal details?")

    print(ans)