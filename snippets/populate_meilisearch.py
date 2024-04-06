import meilisearch
from tqdm import tqdm

from jobs.models import Post
from jobs.utils import get_embedding

client = meilisearch.Client("http://localhost:7700", "NiuZMCgbfbajR-REAxTAnjW2MS2ftJnSWZBy9ChN-WI")

client.delete_index("hnjobs_posts_vectors")
index = client.index("hnjobs_posts_vectors")


def convert_vector(vector):
    return [float(val) for val in vector]


posts = Post.objects.all()
for post in tqdm(posts.iterator(), total=posts.count(), desc="Indexing Posts"):
    if post.vector is not None and len(post.vector) > 0:
        vector = convert_vector(post.vector)
        document_addition_task = index.add_documents(
            [{"id": str(post.id), "description": post.description, "vector": vector}]
        )
        # index.wait_for_task(document_addition_task.task_uid)

index.update_embedders(
    {
        "default": {
            "source": "userProvided",
            "dimensions": 1536,
        }
    }
)


# to search
index.search(
    "",
    opt_params={
        "vector": get_embedding("data centers"),
        "hybrid": {
            "semanticRatio": 0.5,
            "embedder": "default",
        },
    },
)
