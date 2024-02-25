// pages/api/rabbitmq.js

import amqp from 'amqplib';

let interestedMerchant = null;

export default async function handler(req, res) {
    const queue = process.env.RABBITMQ_QUEUE;
    const interestedMerchant = req.body.merchant;


    try {
        if (req.method !== "POST") {
            throw Error("Wrong HTTP method");
        }

        const amqpServer = `amqp://${process.env.RABBITMQ_USER}:${process.env.RABBITMQ_PASSWORD}@${process.env.RABBITMQ_HOST}:${process.env.RABBITMQ_PORT}`;
        const connection = await amqp.connect(amqpServer);
        const channel = await connection.createChannel();

        await channel.assertQueue(queue, { durable: true });

        channel.consume(queue, (msg) => {
            if (msg !== null) {
                console.log(msg.content.toString());
                const messageContent = JSON.parse(msg.content.toString());
                if (interestedMerchant && messageContent.companyId === interestedMerchant) {
                    console.log("Relevant message received:", messageContent);
                    // Process the message here
                }
                channel.ack(msg);
            }
        }, { noAck: false });

        res.status(200).json({ message: 'Subscribed to RabbitMQ queue successfully.' });
    } catch (error) {
        res.status(500).json({ message: 'Failed to subscribe to RabbitMQ queue.', error: error.message });
    }
}
