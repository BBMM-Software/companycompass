const ConvertStringToHTML = function (str) {
    let parser = new DOMParser();
    let doc = parser.parseFromString(str, "text/html");
    return doc.body;
};

const server_url = "http://127.0.0.1:1280/ask?";
const company_name = ^company_name^
const company_website = ^company_website_url^

const run = function () {
    const str = `<button
    id="chatButton"
    style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        z-index:99;
        border-radius: 50%;
        background-color: #f2f2f2;
    "
>
    <svg
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
    >
        <path
            opacity="0.5"
            d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 13.5997 2.37562 15.1116 3.04346 16.4525C3.22094 16.8088 3.28001 17.2161 3.17712 17.6006L2.58151 19.8267C2.32295 20.793 3.20701 21.677 4.17335 21.4185L6.39939 20.8229C6.78393 20.72 7.19121 20.7791 7.54753 20.9565C8.88836 21.6244 10.4003 22 12 22Z"
            fill="#1C274C"
        />
        <path
            d="M7.825 12.85C7.36937 12.85 7 13.2194 7 13.675C7 14.1306 7.36937 14.5 7.825 14.5H13.875C14.3306 14.5 14.7 14.1306 14.7 13.675C14.7 13.2194 14.3306 12.85 13.875 12.85H7.825Z"
            fill="#1C274C"
        />
        <path
            d="M7.825 9C7.36937 9 7 9.36937 7 9.825C7 10.2806 7.36937 10.65 7.825 10.65H16.625C17.0806 10.65 17.45 10.2806 17.45 9.825C17.45 9.36937 17.0806 9 16.625 9H7.825Z"
            fill="#1C274C"
        />
    </svg>
</button>
<div
    id="chatDiv"
    style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        border: 2px black solid;
        width: 400px;
        height: 500px;
        z-index:99;
        border-radius: 25px;
        background-color: #f2f2f2;
        display: none;
    "
>
    <div
        style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-right: 20px;
            padding-left: 20px;
            margin: 0;
        "
    >
        <h3>${company_name} served by CompanyCompass</h3>
        <button
            id="closeActionButton"
            style="height: 30px; width: 30px; border-radius: 50%"
        >
            X
        </button>
    </div>
    <div
        id="messagesBody"
        style="
            height: 400px;
            border-top: 1px black solid;
            border-bottom: 1px black solid;
            padding: 10px;
            overflow-y:auto;
        "
    >
</div>
    <div
        id="inputDiv"
        style="position: absolute; bottom: 8px; right: 22px; width: 90%; min-height: 40px"
    >
        <input
            id="inputChat"
            style="
                width: 262px;
                height: 35px;
                border-radius: 15px;
                padding-left: 20px;
                padding-right: 80px;
                box-sizing: content-box;
            "
        />
        <button
            id="sendActionButton"
            style="
                position: absolute;
                bottom: 7px;
                right: 8px;
                background-color: #bebebe;
                border: 0;
                border-radius: 15px;
                height: 27.5px;
                width: 60px;
            "
        >
            Send
        </button>
    </div>
</div>`;
document.body.appendChild(ConvertStringToHTML(str));
var isChatOpen = false;

const button = document.getElementById("chatButton");
const chatDiv = document.getElementById("chatDiv");
const inputChat = document.getElementById("inputChat");
const closeButton = document.getElementById("closeActionButton");
const sendButton = document.getElementById("sendActionButton");
const messageBody = document.getElementById("messagesBody");

button.onclick = () => {
isChatOpen = true;
button.style.display = "none";
chatDiv.style.display = "block";
};

closeButton.onclick = () => {
isChatOpen = false;
button.style.display = "block";
chatDiv.style.display = "none";
};

sendButton.onclick = () => {
const inputChat = document.getElementById("inputChat");
let question = inputChat.value;
inputChat.value = "";
console.log(question);
sendButton.textContent = "Loading";
sendButton.disabled = true;
messageBody.appendChild(
    ConvertStringToHTML(`<div style="width:100%; display:flex; justify-content:end; margin-bottom:10px">
<div style="background-color: #bebebe; max-width: 80%;  padding: 5px; border-radius: 5px;" >${question}</div></div>`)
);
fetch(
    server_url +
        new URLSearchParams({
            company_name: company_name,
            company_site: company_website,
            question: question,
        })
).then(
    (response) => {
        response.text().then((val) => {
            console.log(val);
            sendButton.textContent = "Send";
            sendButton.disabled = false;
            messageBody.appendChild(
                ConvertStringToHTML(`<div style="width:100%; display:flex; justify-content:start; margin-bottom:10px">
        <div style="background-color: #e2e2e2; max-width: 80%;  padding: 5px; border-radius: 5px;" >${val}</div></div>`)
            );
        });
    },
    (rejection) => {
        console.log(response);
        sendButton.textContent = "Send";
        sendButton.disabled = false;
    }
);
};
}


if (document.body !== null) 
    run()
else 
    window.addEventListener("DOMContentLoaded", () => {run()});
