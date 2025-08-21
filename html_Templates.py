css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 70vh;
    overflow-y: auto;
    padding: 1rem;
    background-color: #1e1e2f;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.chat-message {
    display: flex;
    max-width: 70%;
    padding: 1rem;
    border-radius: 1rem;
    margin-bottom: 0.5rem;
    word-wrap: break-word;
}

.chat-message.user {
    align-self: flex-start; /* linksbündig */
    background-color: #2b313e;
}

.chat-message.bot {
    align-self: flex-end; /* rechtsbündig */
    background-color: #475063;
}

.chat-message .avatar {
    width: 40px;
    height: 40px;
    margin-right: 0.5rem;
}

.chat-message.bot .avatar {
    margin-left: 0.5rem;
    margin-right: 0;
}

.chat-message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    flex: 1;
    padding: 0.5rem 1rem;
    color: #fff;
}
</style>
'''


bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png" alt="User Avatar">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''