const sendMessageTelegramLink = 'https://api.telegram.org/bot2064596905:AAHnSrythz4Iu3zTFSqYQmW0p6PSW9rZZ0Y/sendMessage?chat_id='

const chatIds = ['620304420', '675831', '154873092']

export function sendTelegramMessage(msg){
    for (const chatId of chatIds){
        fetch(
            `${sendMessageTelegramLink}${chatId}&text=${msg}`,
            { method: "GET" }
        );
    }

}
