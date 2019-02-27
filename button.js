import axios from "axios";

export default listEvent = () => {
  const list = document.getElementById("list");
  const button = document.getElementById("button");
  button.addEventListener("click", () => {
    axios
      .get("/list", {
        crossorigin: true,
        headers: {
          "Access-Control-ALlow-Origin": "*"
        }
      })
      .then(res => {
        list.innerHTML = res.body;
      });
  });
};
