""" Ce module contient la classe Rpc qui implemente la methode call"""
import uuid
import pika


class Rpc(object):
    """
    Cette classe gere la communication entre le serveur et notre detecteur via RabbitMQ.
    """

    def __init__(self):
        """
        Cree la connection avec le serveur RabbitMQ
        """
        crds = pika.PlainCredentials("guest", "guest")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", credentials=crds)
        )  # On se connecte au meme serveur RabbitMQ que notre service de detection

        self.channel = self.connection.channel()

        result = self.channel.queue_declare()
        self.callback_queue = result.method.queue
        # On cree une queue sur laquelle le service pourra nous repondre

        self.channel.basic_consume(
            self.on_response, no_ack=True, queue=self.callback_queue
        )  # On specifie a RabbitMQ le callback pour gerer les reponses du service
        self.response = ""
        self.corr_id = ""

    def on_response(self, channel, method, props, body):
        """
        Gere les reponses recues sur la queue de retour.
        Quand une reponse est recue, elle est stockee comme variable de classe
        afin d'etre accessible pour la methode call.
        """
        channel.basic_ack(delivery_tag=method.delivery_tag)
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        """
        Cette methode est la methode utilisee par le serveur pour interagir avec le detecteur.
        """
        self.response = None
        # On reinitialise la variable reponse a chaque appel pour eviter des conflits
        self.corr_id = str(uuid.uuid4())
        # On cree une variable de correlation.
        # Cette variable va nous permettre de nous assurer que le message recu correspond bien
        # a la requete envoyee (cf. if dans on_response).
        self.channel.basic_publish(
            exchange='visage',
            routing_key='visage',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id),
            body=str(message))  # On publie le message
        # On attend la reponse pour pouvoir la retourner des que le resultat est disponible.
        while self.response is None:
            self.connection.process_data_events()
        return self.response
