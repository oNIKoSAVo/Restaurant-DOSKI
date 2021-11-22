const sendMessageTelegramLink = 'https://api.telegram.org/bot2064596905:AAHnSrythz4Iu3zTFSqYQmW0p6PSW9rZZ0Y/sendMessage?chat_id=620304420'

export function sendTelegramMessage(msg){
    fetch(
        `${sendMessageTelegramLink}&text=${msg}`,
        { method: "GET" }
    );
}
