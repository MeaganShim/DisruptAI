let btn = document.querySelector(".button");
const clickHandlerFunction = e => {
  e.target.disabled = true
  e.preventDefault();
  let url = "http://localhost:5000";
  let data = {
    data: document.querySelector("#input-field").value
  };
  return fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      let words = response.json().then((wordJson)=> {
        appendToDom(wordJson.response);
        e.target.disabled = false
      });
      
    })
    .catch(err => console.log(err));
};
btn.addEventListener("click", clickHandlerFunction);

const appendToDom = words => {
  let newDiv = document.createElement("div");
  newDiv.setAttribute("class", "speech-bubble");
  newDiv.innerText = words;
  let speechArea = document.querySelector(".convo-log");
  speechArea.appendChild(newDiv);
  document.getElementById("input-field").setAttribute("value", "");
};
