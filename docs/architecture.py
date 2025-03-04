from diagrams import Cluster, Diagram
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server

with Diagram("MS Object Detection EDA", show=True, direction="TB"):
    topic = Kafka("Topic: object-detection")

    with Cluster("MS Object Detection"):
        consumer = Server("Consumer : ms-object-detection")
        topic_reponse = Kafka("Topic: object-detection_response")

    topic >> consumer >> topic_reponse
