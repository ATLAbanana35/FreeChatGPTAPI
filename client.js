function getMessageText() {
  const messages = document.querySelectorAll(
    "#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.flex-1.overflow-hidden > div > div > div > div > div > div > div.relative.flex.w-full.flex-col.agent-turn > div.flex-col.gap-1.md\\:gap-3"
  );
  let currentMessage = messages[messages.length - 1];
  const a = document.querySelectorAll("#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.flex-1.overflow-hidden > div > div > div > div > div > div > div.relative.flex.w-full.flex-col.agent-turn > div.flex-col.gap-1.md\\:gap-3 > div.flex.flex-grow.flex-col.max-w-full > div > div > pre > div > div.flex.items-center.relative.text-token-text-secondary.bg-token-main-surface-secondary.px-4.py-2.text-xs.font-sans.justify-between.rounded-t-md")
const b = a[a.length-1]
b.innerHTML = "";
    return currentMessage.textContent;
}
function _app(path, type, content, callback) {
  const data = JSON.stringify({ type: type, content: content });
  const XML = new XMLHttpRequest();
  XML.open("POST", "http://localhost:5000" + path);
  XML.onload = () => {
    if (XML.responseText === "Success" || path === "/api/info") {
      console.log(
        "App request sended successfully DATA:" + data + " and PATH: " + path
      );
      callback(XML.responseText);
    } else {
      console.error(
        "An error occurred! : " +
          XML.responseText +
          " INFOS : DATA:" +
          data +
          " and PATH: " +
          path
      );
    }
  };
  XML.send(data);
}
function getIsWriting() {
  const button = document.querySelector(
    "#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.w-full.pt-2.md\\:pt-0.dark\\:border-white\\/20.md\\:border-transparent.md\\:dark\\:border-transparent.md\\:w-\\[calc\\(100\\%-\\.5rem\\)\\] > form > div > div.flex.w-full.items-center > div > button"
  );
  try {
    if (button.ariaLabel === "Stop generating") {
      return true;
    } else {
      return false;
    }
  } catch (e) {
    return true;
  }
}

function sendToChatGPT(text, callback) {
  let resultText =
    text +
    "\n\n***IMPORTANT: ONLY WRITE CODE AS PLAIN TEXT, NOT IN ``` OR OTHER SYNTAX! OR IT WILL CORRUPT THE FILE***\n";
  const startPos = document.querySelector("textarea[data-id]").selectionStart;
  const endPos = document.querySelector("textarea[data-id]").selectionEnd;
  const newText =
    document.querySelector("textarea[data-id]").value.substring(0, startPos) +
    resultText +
    document.querySelector("textarea[data-id]").value.substring(endPos);
  document.querySelector("textarea[data-id]").value = newText;
  document.querySelector("textarea[data-id]").selectionStart =
    startPos + resultText.length;
  document.querySelector("textarea[data-id]").selectionEnd =
    document.querySelector("textarea[data-id]").selectionStart;
  document
    .querySelector("textarea[data-id]")
    .dispatchEvent(new Event("input", { bubbles: true }));
  setTimeout(() => {
    document
      .querySelector(
        "#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.w-full.pt-2.md\\:pt-0.dark\\:border-white\\/20.md\\:border-transparent.md\\:dark\\:border-transparent.md\\:w-\\[calc\\(100\\%-\\.5rem\\)\\] > form > div > div.flex.w-full.items-center > div > button > span"
      )
      .click();
    setTimeout(() => {
      callback();
    }, 1000);
  }, 1000);
}

function getTask() {
  _app("/api/info", "null", "null", (response) => {
    const JSONResponse = JSON.parse(response);
    if (JSONResponse["isActive"] === true) {
      const message = JSONResponse["message"];
      sendToChatGPT(message, () => {
        const i = setInterval(() => {
          _app("/api/set", "first", getMessageText(), () => {
            if (getIsWriting()) {
              _app("/api/set", "update", getMessageText(), () => {});
            } else {
              clearInterval(i);
              setTimeout(() => {
                
                _app("/api/set", "end", getMessageText(), () => {
                  getTask();
                });
              }, 1000);
            }
          });
        }, 500);
      });
    } else {
      setTimeout(() => {
        getTask();
      }, 1000);
    }
  });
}
getTask();
